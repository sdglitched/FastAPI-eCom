from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from typing import List

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.pydantic_schemas.customer import Customer, CustomerCreate
from fastapi_ecom.utils.crud.customer import create_customer, get_customers ,get_customer_by_email
from fastapi_ecom.utils.auth import verify_cust_cred


router = APIRouter()

@router.post("/customer", response_model=Customer, status_code=201)
async def create_new_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = get_customer_by_email(db=db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Try a new Email! Email is already registered")
    return create_customer(db=db, customer=customer)

@router.get("/customer/me")#, response_model=Customer)
async def read_customer_me(email: str = Depends(verify_cust_cred)):
    return {"email": email}

@router.get("/customer", response_model=List[Customer])
async def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = get_customers(db, skip=skip, limit=limit)
    return customers
