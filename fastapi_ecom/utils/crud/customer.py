from datetime import datetime, timezone
import bcrypt

from uuid import uuid4

from fastapi import HTTPException, status

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi_ecom.database.models.customer import Customer
from fastapi_ecom.database.pydantic_schemas.customer import CustomerCreate, CustomerUpdate, CustomerView, CustomerInternal


async def create_customer(db: AsyncSession, customer: CustomerCreate):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(customer.password.strip().encode('utf-8'), salt)
    db_customer = Customer(email=customer.email.strip(),
                           password=hashed_password.decode('utf-8'),
                           name=customer.name.strip(),
                           addr_line_1=customer.addr_line_1.strip(),
                           addr_line_2=customer.addr_line_2.strip(),
                           city=customer.city.strip(),
                           state=customer.state.strip(),
                           uuid=uuid4().hex[0:8])
    db.add(db_customer)
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Uniqueness constraint failed - Please try again"
        )
    return CustomerView.model_validate(db_customer).model_dump()

async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Customer).options(selectinload("*"))
    result = await db.execute(query)
    customers = result.scalars().all()
    return [CustomerView.model_validate(customer).model_dump() for customer in customers]

async def get_customer_by_email(db: AsyncSession, email: str):
    query = select(Customer).where(Customer.email == email).options(selectinload("*"))
    result = await db.execute(query)
    customer_by_email = result.scalar_one_or_none()
    if customer_by_email is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not present in database"
        )
    return CustomerInternal.model_validate(customer_by_email)

async def get_customer_by_uuid(db: AsyncSession, uuid: str):
    query = select(Customer).where(Customer.uuid == uuid).options(selectinload("*"))
    result = await db.execute(query)
    customer_by_uuid = result.scalar_one_or_none()
    if customer_by_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not present in database"
        )
    return CustomerInternal.model_validate(customer_by_uuid)

async def delete_customer(db: AsyncSession, uuid: str):
    customer_to_delete = await get_customer_by_uuid(db=db, uuid=uuid)
    query = delete(Customer).filter_by(uuid=uuid)
    await db.execute(query)
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while deleting"
        )
    return CustomerView.model_validate(customer_to_delete).model_dump()

async def modify_customer(db: AsyncSession, customer: CustomerUpdate, uuid: str):
    query = select(Customer).where(Customer.uuid == uuid).options(selectinload("*"))
    result = await db.execute(query)
    customer_to_update = result.scalar_one_or_none()
    is_updated = False
    cus_cols = ["email", "name", "addr_line_1", "addr_line_2", "city", "state"]
    for item in cus_cols:
      if getattr(customer, item) != "":
        setattr(customer_to_update, item, getattr(customer, item).strip())
        is_updated = True
    if customer.password != "":
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(customer.password.encode('utf-8'), salt)
        customer_to_update.password = hashed_password.decode('utf-8')
        is_updated = True
    if is_updated:
        customer_to_update.update_date = datetime.now(timezone.utc)
        try:
            await db.flush()
        except IntegrityError as expt:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Uniqueness constraint failed - Please try again"
        )
    return CustomerView.model_validate(customer_to_update).model_dump()
