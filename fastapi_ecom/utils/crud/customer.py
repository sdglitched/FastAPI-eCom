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
    hashed_password = bcrypt.hashpw(customer.password.encode('utf-8'), salt)
    db_customer = Customer(email=customer.email,
                           password=hashed_password.decode('utf-8'),
                           name=customer.name,
                           addr_line_1=customer.addr_line_1,
                           addr_line_2=customer.addr_line_2,
                           city=customer.city,
                           state=customer.state,
                           uuid=uuid4().hex[0:8])
    db.add(db_customer)
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Uniqueness constraint failed - Please try again"
        )
    return CustomerView.from_orm(db_customer).dict()

async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Customer).options(selectinload("*"))
    result = await db.execute(query)
    customers = result.scalars().all()
    return [CustomerView.from_orm(customer).dict() for customer in customers]

async def get_customer_by_email(db: AsyncSession, email: str):
    query = select(Customer).where(Customer.email == email).options(selectinload("*"))
    result = await db.execute(query)
    customer_by_email = result.scalar_one_or_none()
    if customer_by_email is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not present in database"
        )
    return CustomerInternal.from_orm(customer_by_email)

async def get_customer_by_uuid(db: AsyncSession, uuid: str):
    query = select(Customer).where(Customer.uuid == uuid).options(selectinload("*"))
    result = await db.execute(query)
    customer_by_uuid = result.scalar_one_or_none()
    if customer_by_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not present in database"
        )
    return CustomerInternal.from_orm(customer_by_uuid)

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
    return CustomerView.from_orm(customer_to_delete).dict()

async def modify_customer(db: AsyncSession, customer: CustomerUpdate, uuid: str):
    query = select(Customer).where(Customer.uuid == uuid).options(selectinload("*"))
    result = await db.execute(query)
    customer_to_update = result.scalar_one_or_none()
    if customer.email != "":
        customer_to_update.email = customer.email
    if customer.name != "":
        customer_to_update.name = customer.name
    if customer.addr_line_1 != "":
        customer_to_update.addr_line_1 = customer.addr_line_1
    if customer.addr_line_2 != "":
        customer_to_update.addr_line_2 = customer.addr_line_2
    if customer.city != "":
        customer_to_update.city = customer.city
    if customer.state != "":
        customer_to_update.state = customer.state
    if customer.password != "":
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(customer.password.encode('utf-8'), salt)
        customer_to_update.password = hashed_password.decode('utf-8')
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Uniqueness constraint failed - Please try again"
        )
    return CustomerView.from_orm(customer_to_update).dict()
