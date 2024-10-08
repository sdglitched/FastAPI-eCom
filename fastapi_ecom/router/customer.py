from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.pydantic_schemas.customer import CustomerCreate, CustomerUpdate, CustomerInternal, CustomerResult, CustomerManyResult
from fastapi_ecom.utils.crud.customer import create_customer, get_customers, delete_customer, modify_customer
from fastapi_ecom.utils.auth import verify_cust_cred


router = APIRouter(prefix="/customer")

@router.post("", response_model=CustomerResult, status_code=201, tags=["customer"])
async def create_new_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    new_customer = await create_customer(db=db, customer=customer)
    return {
        "action": "post",
        "customer": new_customer
    }

@router.get("/me", tags=["customer"])
async def read_customer_me(customer_auth: CustomerInternal = Depends(verify_cust_cred)):
    return {
        "action": "get",
        "email": customer_auth.email
    }

@router.get("", response_model=CustomerManyResult, tags=["customer"])
async def read_customers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    customers = await get_customers(db, skip=skip, limit=limit)
    return {
        "action": "get",
        "customers": customers
    }

@router.delete("/delete/me", response_model=CustomerResult, tags=["customer"])
async def dlt_customer(db: AsyncSession = Depends(get_db), customer_auth: CustomerInternal = Depends(verify_cust_cred)):
    customer_to_delete = await delete_customer(db=db, uuid=customer_auth.uuid)
    return {
        "action": "delete",
        "customer": customer_to_delete
    }

@router.put("/update/me", response_model=CustomerResult, tags=["customer"])
async def updt_customer(customer: CustomerUpdate, db: AsyncSession = Depends(get_db), customer_auth: CustomerInternal = Depends(verify_cust_cred)):
    customer_to_update = await modify_customer(db=db, customer=customer, uuid=customer_auth.uuid)
    return {
        "action": "put",
        "customer": customer_to_update
    }
