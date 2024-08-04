import bcrypt

from fastapi import HTTPException, status

from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi_ecom.database.models.business import Business
from fastapi_ecom.database.pydantic_schemas.business import BusinessCreate, BusinessUpdate, BusinessView, BusinessInternal


def create_business(db: Session, business: BusinessCreate):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(business.password.encode('utf-8'), salt)
    db_business = Business(email=business.email,
                           password=hashed_password.decode('utf-8'),
                           name=business.name,
                           addr_line_1=business.addr_line_1,
                           addr_line_2=business.addr_line_2,
                           city=business.city,
                           state=business.state)
    db.add(db_business)
    try:
        db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Uniqueness constraint failed - Please try again"
        )
    return BusinessView.from_orm(db_business).dict()

def get_businesses(db: Session, skip: int = 0, limit: int = 100):
    businesses = db.query(Business).offset(skip).limit(limit).all()
    for business in businesses:
        print(business)
    return [BusinessView.from_orm(business).dict() for business in businesses]

def get_business_by_email(db: Session, email: str):
    business_by_email = db.query(Business).filter(Business.email == email).first()
    if business_by_email is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not present in database"
        )
    return BusinessInternal.from_orm(business_by_email)

def get_business_by_uuid(db: Session, uuid: str):
    business_by_uuid = db.query(Business).filter(Business.uuid == uuid).first()
    if business_by_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not present in database"
        )
    return BusinessInternal.from_orm(business_by_uuid)

def delete_business(db: Session, uuid: str):
    business_to_delete = get_business_by_uuid(db=db, uuid=uuid)
    query = delete(Business).filter_by(uuid=uuid)
    db.execute(query)
    try:
        db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while deleting"
        )
    return BusinessView.from_orm(business_to_delete).dict()

def modify_business(db: Session, business: BusinessUpdate, uuid: str):
    business_to_update = db.query(Business).filter(Business.uuid == uuid).first()
    business_to_update.email = business.email
    business_to_update.name = business.name
    business_to_update.addr_line_1 = business.addr_line_1
    business_to_update.addr_line_2 = business.addr_line_2
    business_to_update.city = business.city
    business_to_update.state = business.state
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(business.password.encode('utf-8'), salt)
    business_to_update.password = hashed_password.decode('utf-8')
    try:
        db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while updating"
        )
    return BusinessView.from_orm(business_to_update).dict()