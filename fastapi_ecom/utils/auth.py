import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.models.business import Business
from fastapi_ecom.database.models.customer import Customer

# Initialize HTTP Basic Authentication.
# This will prompt users for a username and password when accessing secured endpoints.
security = HTTPBasic()

async def verify_cust_cred(credentials: HTTPBasicCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> Customer:
    """
    Verify customer credentials using HTTP Basic Authentication.
    This function retrieves the customer record from the database using the provided username
    (email address) and verifies the provided password against the stored hashed password.

    :param credentials: HTTPBasicCredentials containing the username and password.
    :param db: Database session to query customer data.

    :return: The customer object if authentication is successful.

    :raises HTTPException: If the username or password is incorrect.
    """
    query = select(Customer).where(Customer.email == credentials.username).options(selectinload("*"))
    result = await db.execute(query)
    customer_by_email = result.scalar_one_or_none()
    if not customer_by_email or not bcrypt.checkpw(credentials.password.encode('utf-8'), customer_by_email.password.encode('utf-8')):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid authentication credentials",
            headers = {"WWW-Authenticate": "Basic"},
        )
    else:
        return customer_by_email

async def verify_business_cred(credentials: HTTPBasicCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> Business:
    """
    Verify business credentials using HTTP Basic Authentication.
    This function retrieves the business record from the database using the provided username
    (email address) and verifies the provided password against the stored hashed password.

    :param credentials: HTTPBasicCredentials containing the username and password.
    :param db: Database session to query business data.

    :return: The business object if authentication is successful.

    :raises HTTPException: If the username or password is incorrect.
    """
    query = select(Business).where(Business.email == credentials.username).options(selectinload("*"))
    result = await db.execute(query)
    business_by_email = result.scalar_one_or_none()
    if not business_by_email or not bcrypt.checkpw(credentials.password.encode('utf-8'), business_by_email.password.encode('utf-8')):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid authentication credentials",
            headers = {"WWW-Authenticate": "Basic"},
        )
    else:
        return business_by_email
