from datetime import datetime, timezone
import bcrypt

from uuid import uuid4

from fastapi import HTTPException, status

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi_ecom.database.models.business import Business
from fastapi_ecom.database.pydantic_schemas.business import BusinessCreate, BusinessUpdate, BusinessView, BusinessInternal


async def create_business(db: AsyncSession, business: BusinessCreate):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(business.password.strip().encode('utf-8'), salt)
    db_business = Business(email=business.email.strip(),
                           password=hashed_password.decode('utf-8'),
                           name=business.name.strip(),
                           addr_line_1=business.addr_line_1.strip(),
                           addr_line_2=business.addr_line_2.strip(),
                           city=business.city.strip(),
                           state=business.state.strip(),
                           uuid=uuid4().hex[0:8])
    db.add(db_business)
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Uniqueness constraint failed - Please try again"
        )
    return BusinessView.model_validate(db_business).model_dump()

async def get_businesses(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Business).options(selectinload("*"))
    result = await db.execute(query)
    businesses = result.scalars().all()
    return [BusinessView.model_validate(business).model_dump() for business in businesses]

async def get_business_by_email(db: AsyncSession, email: str):
    query = select(Business).where(Business.email == email).options(selectinload("*"))
    result = await db.execute(query)
    business_by_email = result.scalar_one_or_none()
    if business_by_email is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not present in database"
        )
    return BusinessInternal.model_validate(business_by_email)

async def get_business_by_uuid(db: AsyncSession, uuid: str):
    query = select(Business).where(Business.uuid == uuid).options(selectinload("*"))
    result = await db.execute(query)
    business_by_uuid = result.scalar_one_or_none()
    if business_by_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not present in database"
        )
    return BusinessInternal.model_validate(business_by_uuid)

async def delete_business(db: AsyncSession, uuid: str):
    business_to_delete = await get_business_by_uuid(db=db, uuid=uuid)
    query = delete(Business).filter_by(uuid=uuid)
    await db.execute(query)
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while deleting"
        )
    return BusinessView.model_validate(business_to_delete).model_dump()

async def modify_business(db: AsyncSession, business: BusinessUpdate, uuid: str):
    query = select(Business).where(Business.uuid == uuid).options(selectinload("*"))
    result = await db.execute(query)
    business_to_update = result.scalar_one_or_none()
    is_updated = False
    bus_cols = ["email", "name", "addr_line_1", "addr_line_2", "city", "state"]
    for item in bus_cols:
      if getattr(business, item) != "":
        setattr(business_to_update, item, getattr(business, item).strip())
        is_updated = True
    if business.password != "":
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(business.password.encode('utf-8'), salt)
        business_to_update.password = hashed_password.decode('utf-8')
        is_updated = True
    if is_updated:
        business_to_update.update_date = datetime.now(timezone.utc)
        try:
            await db.flush()
        except IntegrityError as expt:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Uniqueness constraint failed - Please try again"
            )
    return BusinessView.model_validate(business_to_update).model_dump()
