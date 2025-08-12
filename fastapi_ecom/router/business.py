from datetime import datetime, timezone
from uuid import uuid4

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.models.business import Business
from fastapi_ecom.database.pydantic_schemas.business import (
    BusinessCreate,
    BusinessManyResult,
    BusinessResult,
    BusinessUpdate,
    BusinessView,
)
from fastapi_ecom.utils.auth import verify_business_cred
from fastapi_ecom.utils.logging_setup import failure, general, success, warning

router = APIRouter(prefix="/business")

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=BusinessResult, tags=["business"])
async def create_business(business: BusinessCreate, db: AsyncSession = Depends(get_db)) -> BusinessResult:
    """
    Endpoint to create a new business.

    :param business: Input data for creating a new business. Must adhere to the `BusinessCreate`
                     schema.
    :param db: Active asynchronous database session dependency.

    :return: Dictionary containing the action type and the created business data, validated and
             serialized using the `BusinessView` schema.

    :raises HTTPException:
        - If a uniqueness constraint fails, it returns a 409 Conflict status.
        - If there are other database errors, it returns a 500 Internal Server Error.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(business.password.strip().encode('utf-8'), salt)
    db_business = Business(
        email=business.email.strip(),
        password=hashed_password.decode('utf-8'),
        name=business.name.strip(),
        addr_line_1=business.addr_line_1.strip(),
        addr_line_2=business.addr_line_2.strip(),
        city=business.city.strip(),
        state=business.state.strip(),
        uuid=uuid4().hex[0:8]  # Assign UUID manually; One UUID per transaction
    )
    general(f"Adding account for business in database: {business.email}")
    db.add(db_business)
    try:
        await db.flush()
    except IntegrityError as expt:
        failure(f"Business account creation failed - Uniqueness constraint violation for email: {business.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Uniqueness constraint failed - Please try again"
        ) from expt
    except Exception as expt:
        failure(f"Business account creation failed with unexpected error for email: {business.email}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error occurred."
        ) from expt
    success(f"Business account created successfully with email: {business.email}")
    return {
        "action": "post",
        "business": BusinessView.model_validate(db_business).model_dump()
    }

@router.get("/me", status_code=status.HTTP_200_OK, tags=["business"])
async def get_business_me(business_auth = Depends(verify_business_cred)) -> dict[str, str]:
    """
    Endpoint to fetch the email of the currently authenticated business.

    :param business_auth: Authenticated business object.

    :return: Dictionary containing the action type and the authenticated business's email.
    """
    general(f"Business authentication successful for: {business_auth.email}")
    return {
        "action": "get",
        "email": business_auth.email
    }

@router.get("/search", status_code=status.HTTP_200_OK, response_model=BusinessManyResult, tags=["business"])
async def get_businesses(
    skip: int = Query(0, ge=0, description="Number of records to skip (must be between 0 and int64)"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return (must be between 1 and 100)"),
    db: AsyncSession = Depends(get_db)
) -> BusinessManyResult:
    """
    Endpoint fetches a paginated list of businesses from the database.

    :param skip: Number of records to skip. Must be between 0 and int64.
    :param limit: Maximum number of records to return. Must be between 1 and 100.
    :param db: Active asynchronous database session dependency.

    :return: Dictionary containing the action type and a list of businesses, validated and
             serialized using the `BusinessView` schema.

    :raises HTTPException:
        - If no business exist in the database, it raises 404 Not Found.
    """
    general(f"Searching businesses with skip={skip}, limit={limit}")
    query = select(Business).options(selectinload("*")).offset(skip).limit(limit)
    result = await db.execute(query)
    businesses = result.scalars().all()
    if not businesses:
        warning("No businesses found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No business present in database"
        )
    success(f"Found {len(businesses)} businesses")
    return {
        "action": "get",
        "businesses": [BusinessView.model_validate(business).model_dump() for business in businesses]
    }

@router.delete("/delete/me", status_code=status.HTTP_202_ACCEPTED, response_model=BusinessResult, tags=["business"])
async def delete_business(db: AsyncSession = Depends(get_db), business_auth = Depends(verify_business_cred)) -> BusinessResult:
    """
    Endpoint for an authenticated business to delete its own record.

    :param db: Active asynchronous database session dependency.
    :param business_auth: Authenticated business object.

    :return: Dictionary containing the action type and the deleted business's data, validated and
             serialized using the `BusinessView` schema.

    :raises HTTPException:
        - If a uniqueness constraint fails, it returns a 409 Conflict status.
        - If there are other database errors, it returns a 500 Internal Server Error.
    """
    general(f"Deleting business account: {business_auth.email}")
    query = select(Business).where(Business.uuid == business_auth.uuid).options(selectinload("*"))
    result = await db.execute(query)
    business_to_delete = result.scalar_one_or_none()
    query = delete(Business).where(Business.uuid == business_auth.uuid)
    await db.execute(query)
    try:
        await db.flush()
    except Exception as expt:  #pragma: no cover
        """
        This part of the code cannot be tested as this endpoint performs multiple database
        interactions due to which mocking one part wont produce the desired result. Thus,
        we will keep it uncovered until a alternative can be made for testing this exception block.
        """
        failure(f"Business account deletion failed for: {business_auth.email}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error occurred."
        ) from expt
    success(f"Business account deleted successfully: {business_auth.email}")
    return {
        "action": "delete",
        "business": BusinessView.model_validate(business_to_delete).model_dump()
    }

@router.put("/update/me", status_code=status.HTTP_202_ACCEPTED, response_model=BusinessResult, tags=["business"])
async def update_business(
    business: BusinessUpdate,
    db: AsyncSession = Depends(get_db),
    business_auth = Depends(verify_business_cred)
) -> BusinessResult:
    """
    Endpoint for an authenticated business to update its own record.

    :param business: Input data for updating business. Must adhere to the `BusinessUpdate` schema.
    :param db: Active asynchronous database session dependency.
    :param business_auth: Authenticated business object.

    :return: Dictionary containing the action type and the updated business's data, validated and
             serialized using the `BusinessView` schema.

    :raises HTTPException:
        - If a uniqueness constraint fails, it returns a 409 Conflict status.
        - If there are other database errors, it returns a 500 Internal Server Error.
    """
    business_email = business_auth.email  # Capture email before potential database errors
    general(f"Updating details of business: {business_email}")
    query = select(Business).where(Business.uuid == business_auth.uuid).options(selectinload("*"))
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
            failure(f"Business update failed - Uniqueness constraint violation for: {business_email}")
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
            failure(f"Business update failed with unexpected error for: {business_email}")
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected database error occurred."
                ) from expt
    success(f"Business details updated successfully: {business_email}")
    return {
        "action": "put",
        "business": BusinessView.model_validate(business_to_update).model_dump()
    }
