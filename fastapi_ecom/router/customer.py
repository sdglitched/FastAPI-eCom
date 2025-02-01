from datetime import datetime, timezone
from typing import Dict
from uuid import uuid4

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.models.customer import Customer
from fastapi_ecom.database.pydantic_schemas.customer import (
    CustomerCreate,
    CustomerManyResult,
    CustomerResult,
    CustomerUpdate,
    CustomerView,
)
from fastapi_ecom.utils.auth import verify_cust_cred

router = APIRouter(prefix="/customer")

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=CustomerResult, tags=["customer"])
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)) -> CustomerResult:
    """
    Endpoint to create a new customer.

    :param customer: Input data for creating a new customer. Must adhere to the `CustomerCreate`
                     schema.
    :param db: Active asynchronous database session dependency.

    :raises HTTPException:
        - If a uniqueness constraint fails, it returns a 409 Conflict status.
        - If there are other database errors, it returns a 500 Internal Server Error.

    :return: Dictionary containing the action type and the created customer data, validated and
             serialized using the `BusinessView` schema.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(customer.password.strip().encode('utf-8'), salt)
    db_customer = Customer(
        email = customer.email.strip(),
        password = hashed_password.decode('utf-8'),
        name = customer.name.strip(),
        addr_line_1 = customer.addr_line_1.strip(),
        addr_line_2 = customer.addr_line_2.strip(),
        city = customer.city.strip(),
        state = customer.state.strip(),
        uuid = uuid4().hex[0:8]  # Assign UUID manually; One UUID per transaction
    )
    db.add(db_customer)
    try:
        await db.flush()
    except IntegrityError as expt:
       raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Uniqueness constraint failed - Please try again"
            ) from expt
    except Exception as expt:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred."
            ) from expt
    return {
        "action": "post",
        "customer": CustomerView.model_validate(db_customer).model_dump()
    }

@router.get("/me", status_code=status.HTTP_200_OK, tags=["customer"])
async def get_customer_me(customer_auth = Depends(verify_cust_cred)) -> Dict[str, str]:
    """
    Endpoint to fetch the email of the currently authenticated customer.

    :param customer_auth: Authenticated customer object.

    :return: Dictionary containing the action type and the authenticated customer's email.
    """
    return {
        "action": "get",
        "email": customer_auth.email
    }

@router.get("/search", status_code=status.HTTP_200_OK, response_model=CustomerManyResult, tags=["customer"])
async def get_customers(
    skip: int = Query(0, ge=0, description="Number of records to skip (must be between 0 and int64)"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return (must be between 1 and 100)"),
    db: AsyncSession = Depends(get_db)
) -> CustomerManyResult:
    """
    Endpoint fetches a paginated list of customers from the database.

    :param skip: Number of records to skip. Must be between 0 and int64.
    :param limit: Maximum number of records to return. Must be between 1 and 100.
    :param db: Active asynchronous database session dependency.

    :return: Dictionary containing the action type and a list of customers, validated and
             serialized using the `CustomerView` schema.

    :raises HTTPException:
        - If no customer exist in the database, it raises 404 Not Found.
    """
    query = select(Customer).options(selectinload("*")).offset(skip).limit(limit)
    result = await db.execute(query)
    customers = result.scalars().all()
    if not customers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No customer present in database"
        )
    return {
        "action": "get",
        "customers": [CustomerView.model_validate(customer).model_dump() for customer in customers]
    }

@router.delete("/delete/me", status_code=status.HTTP_202_ACCEPTED, response_model=CustomerResult, tags=["customer"])
async def delete_customer(db: AsyncSession = Depends(get_db), customer_auth = Depends(verify_cust_cred)) -> CustomerResult:
    """
    Endpoint for an authenticated customer to delete its own record.

    :param db: Active asynchronous database session dependency.
    :param customer_auth: Authenticated customer object.

    :return: Dictionary containing the action type and the deleted customer's data.

    :raises HTTPException:
        - If a uniqueness constraint fails, it returns a 409 Conflict status.
        - If there are other database errors, it returns a 500 Internal Server Error.
    """
    query = select(Customer).where(Customer.uuid == customer_auth.uuid).options(selectinload("*"))
    result = await db.execute(query)
    customer_to_delete = result.scalar_one_or_none()
    query = delete(Customer).where(Customer.uuid == customer_auth.uuid)
    await db.execute(query)
    try:
        await db.flush()
    except Exception as expt:  #pragma: no cover
        """
        This part of the code cannot be tested as this endpoint performs multiple database
        interactions due to which mocking one part wont produce the desired result. Thus,
        we will keep it uncovered until a alternative can be made for testing this exception block.
        """
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred."
            ) from expt
    return {
        "action": "delete",
        "customer": CustomerView.model_validate(customer_to_delete).model_dump()
    }

@router.put("/update/me", status_code=status.HTTP_202_ACCEPTED, response_model=CustomerResult, tags=["customer"])
async def update_customer(customer: CustomerUpdate, db: AsyncSession = Depends(get_db), customer_auth = Depends(verify_cust_cred)) -> CustomerResult:
    """
    Endpoint for an authenticated customer to update its own record.

    :param customer: Input data for updating customer. Must adhere to the `BusinessUpdate` schema.
    :param db: Active asynchronous database session dependency.
    :param customer_auth: Authenticated customer object.

    :return: Dictionary containing the action type and the updated customer's data.

    :raises HTTPException:
        - If a uniqueness constraint fails, it returns a 409 Conflict status.
        - If there are other database errors, it returns a 500 Internal Server Error.
    """
    query = select(Customer).where(Customer.uuid == customer_auth.uuid).options(selectinload("*"))
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
                ) from expt
        except Exception as expt:  #pragma: no cover
            """
            This part of the code cannot be tested as this endpoint performs multiple database
            interactions due to which mocking one part wont produce the desired result. Thus,
            we will keep it uncovered until a alternative can be made for testing this exception block.
            """
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected database error occurred."
                ) from expt
    return {
        "action": "put",
        "customer": CustomerView.model_validate(customer_to_update).model_dump()
    }
