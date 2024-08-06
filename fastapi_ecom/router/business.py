from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.pydantic_schemas.business import BusinessCreate, BusinessUpdate, BusinessInternal, BusinessResult, BusinessManyResult
from fastapi_ecom.utils.crud.business import create_business, get_businesses, delete_business, modify_business
from fastapi_ecom.utils.auth import verify_business_cred


router = APIRouter(prefix="/business")

@router.post("", response_model=BusinessResult, status_code=201, tags=["business"])
async def create_new_business(business: BusinessCreate, db: AsyncSession = Depends(get_db)):
    new_business = await create_business(db=db, business=business)
    return {
        "action": "post",
        "business": new_business
    }

@router.get("/me", tags=["business"])
async def read_business_me(business_auth: BusinessInternal = Depends(verify_business_cred)):
    return {
        "action": "get",
        "email": business_auth.email
    }

@router.get("", response_model=BusinessManyResult, tags=["business"])
async def read_businesses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    businesses = await get_businesses(db, skip=skip, limit=limit)
    return {
        "action": "get",
        "businesses": businesses
    }

@router.delete("/delete/me", response_model=BusinessResult, tags=["business"])
async def dlt_business(db: AsyncSession = Depends(get_db), business_auth: BusinessInternal = Depends(verify_business_cred)):
    business_to_delete = await delete_business(db=db, uuid=business_auth.uuid)
    return {
        "action": "delete",
        "business": business_to_delete
    }

@router.put("/update/me", response_model=BusinessResult, tags=["business"])
async def updt_business(business: BusinessUpdate, db: AsyncSession = Depends(get_db), business_auth: BusinessInternal = Depends(verify_business_cred)):
    business_to_update = await modify_business(db=db, business=business, uuid=business_auth.uuid)
    return {
        "action": "put",
        "business": business_to_update
    }
