import bcrypt

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.orm import Session

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.utils.crud.customer import get_customer_by_email

# Initialize HTTP Basic Authentication
security = HTTPBasic()

def verify_cust_cred(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    customer = get_customer_by_email(db, credentials.username)
    print(bcrypt.checkpw(credentials.password.encode('utf-8'), customer.password.decode('utf-8')))
    if not customer or bcrypt.checkpw(credentials.password.encode('utf-8'), customer.password.decode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return customer.email#credentials.username