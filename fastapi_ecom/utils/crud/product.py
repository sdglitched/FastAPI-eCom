from fastapi import HTTPException, status

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi_ecom.database.models.product import Product
from fastapi_ecom.database.pydantic_schemas.product import ProductCreate, ProductUpdate, ProductView, ProductInternal


async def add_product(db: AsyncSession, product: ProductCreate, business_id: str):
    db_product = Product(name = product.name,
                         description = product.description,
                         category = product.category,
                         mfg_date = product.mfg_date,
                         exp_date = product.exp_date,
                         price = product.price,
                         business_id = business_id)
    db.add(db_product)
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while commiting"
        )
    return ProductView.from_orm(db_product).dict()

async def get_all_products(db: AsyncSession):
    query = select(Product).options(selectinload("*"))
    result = await db.execute(query)
    products = result.scalars().all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No product in database"
        )
    return [ProductView.from_orm(product).dict() for product in products]

async def get_product_by_uuid(db: AsyncSession, uuid: str):
    query = select(Product).where(Product.uuid == uuid).options(selectinload("*"))
    result = await db.execute(query)
    product_by_uuid = result.scalar_one_or_none()
    if product_by_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not present in database"
        )
    return ProductInternal.from_orm(product_by_uuid)

async def delete_product(db: AsyncSession, uuid: str):
    product_to_delete = await get_product_by_uuid(db=db, uuid=uuid)
    query = delete(Product).filter_by(uuid=uuid)
    await db.execute(query)
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while deleting"
        )
    return ProductView.from_orm(product_to_delete).dict()

async def modify_product(db: AsyncSession, product: ProductUpdate, uuid: str):
    query = select(Product).where(Product.uuid == uuid).options(selectinload("*"))
    result = await db.execute(query)
    product_to_update = result.scalar_one_or_none()
    if product_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not present in database"
        )
    product_to_update.name = product.name
    product_to_update.description = product.description
    product_to_update.category = product.category
    product_to_update.mfg_date = product.mfg_date
    product_to_update.exp_date = product.exp_date
    product_to_update.price = product.price
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while modifying"
        )
    return ProductView.from_orm(product_to_update).dict()