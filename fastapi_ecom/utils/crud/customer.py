import bcrypt

from fastapi import HTTPException

from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi_ecom.database.models.customer import Customer
from fastapi_ecom.database.pydantic_schemas.customer import CustomerCreate, CustomerUpdate, CustomerView, CustomerInternal


def create_customer(db: Session, customer: CustomerCreate):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(customer.password.encode('utf-8'), salt)
    db_customer = Customer(email=customer.email,
                           password=hashed_password.decode('utf-8'),
                           name=customer.name,
                           addr_line_1=customer.addr_line_1,
                           addr_line_2=customer.addr_line_2,
                           city=customer.city,
                           state=customer.state)
    db.add(db_customer)
    try:
        db.flush()
    except IntegrityError as expt:
        raise HTTPException(status_code=409, detail="Uniqueness constraint failed - Please try again")
    return CustomerView.from_orm(db_customer).dict()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return [CustomerView.from_orm(cust).dict() for cust in customers]

def get_customer_by_email(db: Session, email: str):
    customer_by_email = db.query(Customer).filter(Customer.email == email).first()
    if customer_by_email is None:
        raise HTTPException(status_code=404, detail="Customer not present in database")
    return CustomerInternal.from_orm(customer_by_email)

def get_customer_by_uuid(db: Session, uuid: str):
    customer_by_uuid = db.query(Customer).filter(Customer.uuid == uuid).first()
    if customer_by_uuid is None:
        raise HTTPException(status_code=404, detail="Customer not present in database")
    return CustomerInternal.from_orm(customer_by_uuid)

def delete_customer(db: Session, uuid: str):
    customer_to_delete = get_customer_by_uuid(db=db, uuid=uuid)
    query = delete(Customer).filter_by(uuid=uuid)
    db.execute(query)
    try:
        db.flush()
    except IntegrityError as expt:
        raise HTTPException(status_code=400, detail="Failed while deleting")
    return CustomerView.from_orm(customer_to_delete).dict()

def modify_customer(db: Session, customer: CustomerUpdate, uuid: str):
    customer_to_update = db.query(Customer).filter(Customer.uuid == uuid).first()
    customer_to_update.email = customer.email
    customer_to_update.name = customer.name
    customer_to_update.addr_line_1 = customer.addr_line_1
    customer_to_update.addr_line_2 = customer.addr_line_2
    customer_to_update.city = customer.city
    customer_to_update.state = customer.state
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(customer.password.encode('utf-8'), salt)
    customer_to_update.password = hashed_password.decode('utf-8')
    try:
        db.flush()
    except IntegrityError as expt:
        raise HTTPException(status_code=400, detail="Failed while updating")
    return CustomerView.from_orm(customer_to_update).dict()
