from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.pydantic_schemas.product import ProductCreate, ProductUpdate, ProductResultInternal, ProductManyResult, ProductManyResultInternal
from fastapi_ecom.utils.crud.product import add_product, get_all_products, get_product_by_text, get_all_products_internal, get_product_by_uuid, delete_product, modify_product
from fastapi_ecom.database.pydantic_schemas.business import BusinessInternal
from fastapi_ecom.utils.auth import verify_business_cred


router = APIRouter(prefix="/product")

@router.post("", response_model=ProductResultInternal, status_code=201, tags=["product"])
async def add_new_product(product: ProductCreate, db: AsyncSession = Depends(get_db), business_auth: BusinessInternal = Depends(verify_business_cred)):
    new_product = await add_product(db=db, product=product, business_id = business_auth.uuid)
    return {
        "action": "post",
        "product": new_product
    }

@router.get("", response_model=ProductManyResult, tags=["product"])
async def read_all_products(db: AsyncSession = Depends(get_db)):
    products = await get_all_products(db)
    return {
        "action": "get",
        "products": products
    }

@router.get("/search/name/{text}", response_model=ProductManyResult, tags=["product"])
async def read_all_products_by_text(text: str, db: AsyncSession = Depends(get_db)):
    products = await get_product_by_text(db, text)
    return {
        "action": "get",
        "products": products
    }

@router.get("/search/internal", response_model=ProductManyResultInternal, tags=["product"])
async def read_all_products_internal(db: AsyncSession = Depends(get_db), business_auth: BusinessInternal = Depends(verify_business_cred)):
    products = await get_all_products_internal(db, business_id = business_auth.uuid)
    return {
        "action": "get",
        "products": products
    }

@router.get("/search/uuid/{uuid}", response_model=ProductResultInternal, tags=["product"])
async def read_product_by_uuid(uuid: str, db: AsyncSession = Depends(get_db), business_auth: BusinessInternal = Depends(verify_business_cred)):
    product = await get_product_by_uuid(db, uuid = uuid)
    return {
        "action": "get",
        "product": product
    }

@router.delete("/delete/uuid/{uuid}", response_model=ProductResultInternal, tags=["product"])
async def dlt_product(uuid: str, db: AsyncSession = Depends(get_db), business_auth: BusinessInternal = Depends(verify_business_cred)):
    product_to_delete = await delete_product(db=db, uuid=uuid)
    return {
        "action": "delete",
        "product": product_to_delete
    }

@router.put("/update/uuid/{uuid}", response_model=ProductResultInternal, tags=["product"])
async def updt_product(uuid: str, product: ProductUpdate, db: AsyncSession = Depends(get_db), business_auth: BusinessInternal = Depends(verify_business_cred)):
    product_to_update = await modify_product(db=db, product=product, uuid=uuid, business_id = business_auth.uuid)
    return {
        "action": "put",
        "product": product_to_update
    }
