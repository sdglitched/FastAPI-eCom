from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from typing import List

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.pydantic_schemas.business import Business, BusinessCreate
from fastapi_ecom.utils.crud.business import create_business, get_business, get_business_by_email, delete_business
from fastapi_ecom.utils.auth import verify_business_cred


router = APIRouter()

@router.post("/business", response_model=Business, status_code=201)
async def create_new_business(business: BusinessCreate, db: Session = Depends(get_db)):
    db_business = get_business_by_email(db=db, email=business.email)
    if db_business:
        raise HTTPException(status_code=400, detail="Try a new Email! Email is already registered")
    return create_business(db=db, business=business)

@router.get("/business/me")
async def read_business_me(email: str = Depends(verify_business_cred)):
    return {"email": email}

@router.get("/business", response_model=List[Business])
async def read_businesss(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    businesss = get_business(db, skip=skip, limit=limit)
    return businesss

@router.delete("/business/delete/me")
async def dlt_business(db: Session = Depends(get_db), email: str = Depends(verify_business_cred)):
    db_business = get_business_by_email(db=db, email=email)
    if db_business is None:
        raise HTTPException(status_code=404, detail="Business not present in database")
    business_to_delete = delete_business(db=db, uuid=db_business.uuid)
    return business_to_delete
