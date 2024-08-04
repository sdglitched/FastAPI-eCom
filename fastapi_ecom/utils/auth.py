import bcrypt

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.orm import Session

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.utils.crud.customer import get_customer_by_email
from fastapi_ecom.utils.crud.business import get_business_by_email

# Initialize HTTP Basic Authentication
security = HTTPBasic()

def verify_cust_cred(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    customer = get_customer_by_email(db, credentials.username)
    if not customer:
         print("No customer present")
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

def verify_business_cred(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    business = get_business_by_email(db, credentials.username)
    if not business:
         print("No business present")
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
        return business.email
