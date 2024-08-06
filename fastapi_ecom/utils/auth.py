import bcrypt

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.utils.crud.customer import get_customer_by_email
from fastapi_ecom.utils.crud.business import get_business_by_email

# Initialize HTTP Basic Authentication
security = HTTPBasic()

async def verify_cust_cred(credentials: HTTPBasicCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    customer = await get_customer_by_email(db, credentials.username)
    if not customer:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    elif not bcrypt.checkpw(credentials.password.encode('utf-8'), customer.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        return customer

async def verify_business_cred(credentials: HTTPBasicCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    business = await get_business_by_email(db, credentials.username)
    if not business:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    elif not bcrypt.checkpw(credentials.password.encode('utf-8'), business.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        return business
