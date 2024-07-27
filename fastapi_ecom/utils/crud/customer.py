import bcrypt

from sqlalchemy.orm import Session
from fastapi_ecom.database.models.customer import Customer
from fastapi_ecom.database.pydantic_schemas.customer import CustomerCreate


def create_customer(db: Session, customer: CustomerCreate):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(customer.password.encode('utf-8'), salt)
    print('Encoded pwd:',customer.password.encode('utf-8'),'Hashed pwd:',hashed_password,'Hashed decoded pwd:',hashed_password.decode('utf-8'))
    db_customer = Customer(email=customer.email,
                           password=hashed_password.decode('utf-8'),
                           name=customer.name,
                           addr_line_1=customer.addr_line_1,
                           addr_line_2=customer.addr_line_2,
                           city=customer.city,
                           state=customer.state)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()

def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()
