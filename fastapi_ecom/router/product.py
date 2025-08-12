from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, delete, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.models.product import Product
from fastapi_ecom.database.pydantic_schemas.product import (
    ProductCreate,
    ProductManyResult,
    ProductManyResultInternal,
    ProductResultInternal,
    ProductUpdate,
    ProductView,
    ProductViewInternal,
)
from fastapi_ecom.utils.auth import verify_business_cred
from fastapi_ecom.utils.logging_setup import failure, general, success, warning

router = APIRouter(prefix="/product")

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProductResultInternal, tags=["product"])
async def add_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    business_auth = Depends(verify_business_cred)
) -> ProductResultInternal:
    """
    Endpoint to add a new product by currently authenticated business.

    :param product: Input data for adding a new product. Must adhere to the `ProductCreate` schema.
    :param db: Active asynchronous database session dependency.
    :param business_auth: Authenticated business object.

    :return: Dictionary containing the action type and the added product data, validated and
             serialized using the `ProductViewInternal` schema.

    :raises HTTPException:
        - If a uniqueness constraint fails, it returns a 409 Conflict status.
        - If there are other database errors, it returns a 500 Internal Server Error.
    """
    db_product = Product(
        name = product.name.strip(),
        description = product.description.strip(),
        category = product.category.strip(),
        mfg_date = product.mfg_date,
        exp_date = product.exp_date,
        price = product.price,
        business_id = business_auth.uuid,
        uuid=uuid4().hex[0:8]  # Assign UUID manually; One UUID per transaction
    )
    general(f"Adding product '{product.name}' to database by {business_auth.email}")
    db.add(db_product)
    try:
        await db.flush()
    except IntegrityError as expt:  #pragma: no cover
        """
        This part of the code cannot be tested as this endpoint performs multiple database
        interactions due to which mocking one part wont produce the desired result. Thus,
        we will keep it uncovered until a alternative can be made for testing this exception block.
        """
        failure(f"Product creation failed for '{product.name}' with unexpected error")
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred."
            ) from expt
    success(f"Product '{product.name}' created successfully by business: {business_auth.uuid}")
    return {
        "action": "post",
        "product": ProductViewInternal.model_validate(db_product).model_dump()
    }

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ProductManyResult, tags=["product"])
async def get_products(
    skip: int = Query(0, ge=0, description="Number of records to skip (must be between 0 and int64)"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return (must be between 1 and 100)"),
    db: AsyncSession = Depends(get_db)
) -> ProductManyResult:
    """
    Endpoint fetches a paginated list of products.

    :param skip: Number of records to skip. Must be between 0 and int64.
    :param limit: Maximum number of records to return. Must be between 1 and 100.
    :param db: Active asynchronous database session dependency.

    :return: Dictionary containing the action type and a list of products, validated and
             serialized using the `ProductView` schema.

    :raises HTTPException:
        - If no products for the currently authenticated business exists in the database, it raises
          404 Not Found.
    """
    general(f"Searching all products with skip={skip}, limit={limit}")
    query = select(Product).options(selectinload("*")).offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    if not products:
        warning("No products found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No product present in database"
        )
    success(f"Found {len(products)} products")
    return {
        "action": "get",
        "products": [ProductView.model_validate(product).model_dump() for product in products]
    }

@router.get("/search/name/{text}", status_code=status.HTTP_200_OK, response_model=ProductManyResult, tags=["product"])
async def get_product_by_text(
    text: str,
    skip: int = Query(0, ge=0, description="Number of records to skip (must be between 0 and int64)"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return (must be between 1 and 100)"),
    db: AsyncSession = Depends(get_db)
) -> ProductManyResult:
    """
    Endpoint fetches a paginated list of products by name or description.

    :param text: The search string used to match product names or descriptions.
    :param skip: Number of records to skip. Must be between 0 and int64.
    :param limit: Maximum number of records to return. Must be between 1 and 100.
    :param db: Active asynchronous database session dependency.

    :return: Dictionary containing the action type and a list of products, validated and
             serialized using the `ProductView` schema.

    :raises HTTPException:
        If no matching products exists in the database, it raises 404 Not Found.
    """
    general(f"Searching products by text '{text}' with skip={skip}, limit={limit}")
    query = select(Product).where(
        or_(Product.name.ilike(f"%{text}%"), Product.description.ilike(f"%{text}%"))
    ).options(selectinload("*")).offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    if not products:
        warning(f"No products found matching text '{text}'")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such product present in database"
        )
    success(f"Found {len(products)} products matching text '{text}'")
    return {
        "action": "get",
        "products": [ProductView.model_validate(product).model_dump() for product in products]
    }

@router.get("/search/internal", status_code=status.HTTP_200_OK, response_model=ProductManyResultInternal, tags=["product"])
async def get_products_internal(
    skip: int = Query(0, ge=0, description="Number of records to skip (must be between 0 and int64)"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return (must be between 1 and 100)"),
    db: AsyncSession = Depends(get_db),
    business_auth = Depends(verify_business_cred)
) -> ProductManyResultInternal:
    """
    Endpoint fetches a paginated list of products associated with the authenticated business.

    :param skip: Number of records to skip. Must be between 0 and int64.
    :param limit: Maximum number of records to return. Must be between 1 and 100.
    :param db: Active asynchronous database session dependency.
    :param business_auth: Authenticated business object.

    :return: Dictionary containing the action type and a list of products, validated and
             serialized using the `ProductViewInternal` schema.

    :raises HTTPException:
        If no products are associated with the authenticated business, it raises 404 Not Found.
    """
    general(f"Searching products for business {business_auth.uuid} with skip={skip}, limit={limit}")
    query = select(Product).where(Product.business_id == business_auth.uuid).options(selectinload("*")).offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    if not products:
        warning(f"No products found for business {business_auth.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No product present in database"
        )
    success(f"Found {len(products)} products for business {business_auth.email}")
    return {
        "action": "get",
        "products": [ProductViewInternal.model_validate(product).model_dump() for product in products]
    }

@router.get("/search/uuid/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResultInternal, tags=["product"])
async def get_product_by_uuid(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    business_auth = Depends(verify_business_cred)
) -> ProductResultInternal:
    """
    Endpoint fetches a specific product by its UUID associated with the authenticated business.

    :param product_id: The UUID of the product to retrieve.
    :param db: Active asynchronous database session dependency.
    :param business_auth: Authenticated business object.

    :return: Dictionary containing the action type and product details, validated and
             serialized using the `ProductViewInternal` schema.

    :raises HTTPException:
        If no products with the given UUID is associated with the authenticated business, it raises
        404 Not Found.
    """
    general(f"Searching for product {product_id} for business {business_auth.uuid}")
    query = select(Product).where(and_(Product.uuid == product_id, Product.business_id == business_auth.uuid)).options(selectinload("*"))
    result = await db.execute(query)
    product_by_uuid = result.scalar_one_or_none()
    if not product_by_uuid:
        warning(f"Product {product_id} not found for business {business_auth.uuid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not present in database"
        )
    success(f"Found product {product_id} for business {business_auth.uuid}")
    return {
        "action": "get",
        "product": ProductViewInternal.model_validate(product_by_uuid)
    }

@router.delete("/delete/uuid/{product_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ProductResultInternal, tags=["product"])
async def delete_product(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    business_auth = Depends(verify_business_cred)
) -> ProductResultInternal:
    """
    Endpoint to delete a product by its UUID associated for an authenticated business.

    :param product_id: The UUID of the product to retrieve.
    :param db: Active asynchronous database session dependency.
    :param business_auth: Authenticated business object.

    :return: Dictionary containing the action type and the deleted product's data, validated and
             serialized using the `ProductViewInternal` schema.

    :raises HTTPException:
        - If no products with the given UUID is associated with the authenticated business, it
          raises 404 Not Found.
        - If there are other database errors, it returns a 500 Internal Server Error.
    """
    general(f"Deleting product {product_id} for business {business_auth.uuid}")
    query = select(Product).where(and_(Product.uuid == product_id, Product.business_id == business_auth.uuid)).options(selectinload("*"))
    result = await db.execute(query)
    product_to_delete = result.scalar_one_or_none()
    if not product_to_delete:
        warning(f"Product {product_id} not found for deletion for business {business_auth.uuid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not present in database"
        )
    query = delete(Product).where(and_(Product.uuid == product_id, Product.business_id == business_auth.uuid))
    await db.execute(query)
    try:
        await db.flush()
    except Exception as expt:  #pragma: no cover
        """
        This part of the code cannot be tested as this endpoint performs multiple database
        interactions due to which mocking one part wont produce the desired result. Thus,
        we will keep it uncovered until a alternative can be made for testing this exception block.
        """
        failure(f"Product deletion failed for {product_id} for business {business_auth.uuid}")
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred."
            ) from expt
    success(f"Product {product_id} deleted successfully for business {business_auth.uuid}")
    return {
        "action": "delete",
        "product": ProductViewInternal.model_validate(product_to_delete).model_dump()
    }

@router.put("/update/uuid/{product_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ProductResultInternal, tags=["product"])
async def update_product(
    product_id: str,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    business_auth = Depends(verify_business_cred)
) -> ProductResultInternal:
    """
    Endpoint to update a product by its UUID associated for an authenticated business.

    :param product_id: The UUID of the product to retrieve.
    :param db: Active asynchronous database session dependency.
    :param business_auth: Authenticated business object.

    :return: Dictionary containing the action type and the updated product's data, validated and
             serialized using the `ProductViewInternal` schema.

    :raises HTTPException:
        - If no products with the given UUID is associated with the authenticated business, it
          raises 404 Not Found.
        - If there are other database errors, it returns a 500 Internal Server Error.
    """
    general(f"Updating product {product_id} for business {business_auth.uuid}")
    query = select(Product).where(and_(Product.uuid == product_id, Product.business_id == business_auth.uuid)).options(selectinload("*"))
    result = await db.execute(query)
    product_to_update = result.scalar_one_or_none()
    if not product_to_update:
        warning(f"Product {product_id} not found for update for business {business_auth.uuid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not present in database"
        )
    is_updated = False
    if product.name != "":
        product_to_update.name = product.name
        is_updated = True
    if product.description != "":
        product_to_update.description = product.description
        is_updated = True
    if product.category != "":
        product_to_update.category = product.category
        is_updated = True
    if str(product.mfg_date) != "1900-01-01 00:00:00+00:00":
        product_to_update.mfg_date = product.mfg_date
        is_updated = True
    if str(product.exp_date) != "1900-01-01 00:00:00+00:00":
        product_to_update.exp_date = product.exp_date
        is_updated = True
    if product.price != 0.0:
        product_to_update.price = product.price
        is_updated = True
    if is_updated:
        product_to_update.update_date = datetime.now(timezone.utc)
        try:
            await db.flush()
        except Exception as expt:  #pragma: no cover
            """
            This part of the code cannot be tested as this endpoint performs multiple database
            interactions due to which mocking one part wont produce the desired result. Thus,
            we will keep it uncovered until a alternative can be made for testing this exception block.
            """
            failure(f"Product update failed for {product_id} for business {business_auth.uuid} with unexpected error")
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected database error occurred."
                ) from expt
    success(f"Product {product_id} updated successfully for business {business_auth.uuid}")
    return {
        "action": "put",
        "product": ProductViewInternal.model_validate(product_to_update).model_dump()
    }
