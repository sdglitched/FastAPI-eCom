from uuid import uuid4

from fastapi import HTTPException, status

from sqlalchemy import delete, or_, and_
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi_ecom.database.models.product import Product
from fastapi_ecom.database.pydantic_schemas.product import ProductCreate, ProductUpdate, ProductView, ProductViewInternal, ProductInternal


async def add_product(db: AsyncSession, product: ProductCreate, business_id: str):
    db_product = Product(name = product.name,
                         description = product.description,
                         category = product.category,
                         mfg_date = product.mfg_date,
                         exp_date = product.exp_date,
                         price = product.price,
                         business_id = business_id,
                         uuid=uuid4().hex[0:8])
    db.add(db_product)
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while commiting"
        )
    return ProductViewInternal.model_validate(db_product).model_dump()

async def get_all_products(db: AsyncSession):
    query = select(Product).options(selectinload("*"))
    result = await db.execute(query)
    products = result.scalars().all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No product in database"
        )
    return [ProductView.model_validate(product).model_dump() for product in products]

async def get_product_by_text(db: AsyncSession, text: str):
    query = select(Product).where(or_(Product.name.ilike(f"%{text}%".lower()), Product.description.like(f"%{text}%".lower()))).options(selectinload("*"))
    result = await db.execute(query)
    products = result.scalars().all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No product in database"
        )
    return [ProductView.model_validate(product).model_dump() for product in products]

async def get_all_products_internal(db: AsyncSession, business_id: str):
    query = select(Product).where(Product.business_id == business_id).options(selectinload("*"))
    result = await db.execute(query)
    products = result.scalars().all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No product in database"
        )
    return [ProductViewInternal.model_validate(product).model_dump() for product in products]

async def get_product_by_uuid(db: AsyncSession, uuid: str):
    query = select(Product).where(Product.uuid == uuid).options(selectinload("*"))
    result = await db.execute(query)
    product_by_uuid = result.scalar_one_or_none()
    if product_by_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not present in database"
        )
    return ProductViewInternal.model_validate(product_by_uuid)

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
    return ProductViewInternal.model_validate(product_to_delete).model_dump()

async def modify_product(db: AsyncSession, product: ProductUpdate, uuid: str, business_id: str):
    query = select(Product).where(and_(Product.uuid == uuid, Product.business_id == business_id)).options(selectinload("*"))
    result = await db.execute(query)
    product_to_update = result.scalar_one_or_none()
    if product_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not present in database"
        )
    if product.name != "":
        product_to_update.name = product.name
    if product.description != "":
        product_to_update.description = product.description
    if product.category != "":
        product_to_update.category = product.category
    if str(product.mfg_date) != "1900-01-01 00:00:00+00:00":
        product_to_update.mfg_date = product.mfg_date
    if str(product.exp_date) != "1900-01-01 00:00:00+00:00":
        product_to_update.exp_date = product.exp_date
    if product.price != 0.0:
        product_to_update.price = product.price
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while modifying"
        )
    return ProductViewInternal.model_validate(product_to_update).model_dump()