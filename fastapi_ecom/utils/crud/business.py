import bcrypt

from sqlalchemy.orm import Session
from fastapi_ecom.database.models.business import Business
from fastapi_ecom.database.pydantic_schemas.business import BusinessCreate


def create_business(db: Session, business: BusinessCreate):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(business.password.encode('utf-8'), salt)
    print('Encoded pwd:',business.password.encode('utf-8'),'Hashed pwd:',hashed_password,'Hashed decoded pwd:',hashed_password.decode('utf-8'))
    db_business = Business(email=business.email,
                           password=hashed_password.decode('utf-8'),
                           name=business.name,
                           addr_line_1=business.addr_line_1,
                           addr_line_2=business.addr_line_2,
                           city=business.city,
                           state=business.state)
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business

def get_business(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Business).offset(skip).limit(limit).all()

def get_business_by_email(db: Session, email: str):
    return db.query(Business).filter(Business.email == email).first()

def get_business_by_uuid(db: Session, uuid: str):
    return db.query(Business).filter(Business.uuid == uuid).first()

def delete_business(db: Session, uuid: str):
    business_to_delete = get_business_by_uuid(db=db, uuid=uuid)
    db.delete(business_to_delete)
    db.commit()
    return business_to_delete
