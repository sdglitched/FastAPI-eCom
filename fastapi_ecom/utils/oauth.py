from datetime import datetime, timezone
from uuid import uuid4

from authlib.integrations.starlette_client import OAuth
from authlib.oidc.core import UserInfo
from fastapi import Depends, HTTPException, status
from fastapi.security import OpenIdConnect
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from fastapi_ecom.config import config
from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.models.business import Business
from fastapi_ecom.database.models.customer import Customer
from fastapi_ecom.utils.logging_setup import failure, general, success, warning

server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

oidc = OpenIdConnect(openIdConnectUrl=server_metadata_url, scheme_name="OpenID Connect", auto_error=False)

oauth = OAuth()

oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    server_metadata_url=server_metadata_url,
    client_kwargs={"scope": "openid email profile"},
)


class OIDCUser(BaseModel):
    """
    Pydantic model representing an authenticated OIDC user.

    This model is used to validate and structure user information received from
    OpenID Connect providers like Google OAuth.

    :cvar email: Email address of the authenticated user.
    :cvar name: Full name of the authenticated user.
    :cvar sub: Subject identifier from the OIDC provider.
    """

    email: str
    name: str | None = None
    sub: str

    @classmethod
    def from_userinfo(cls, userinfo: UserInfo) -> "OIDCUser":
        fields = {field: userinfo[field] for field in cls.model_fields if field in userinfo}
        return cls(**fields)


async def current_user(token: str = Depends(oidc)) -> OIDCUser | None:
    """
    Extract and validate the current authenticated user from OIDC token.

    This function processes the Bearer token from the Authorization header, validates it with
    the Google OAuth provider, and returns the authenticated user information.

    :param token: Bearer token containing the OIDC access token.

    :return: The authenticated OIDC user object or None if authentication fails.
    """
    if not token:
        return None
    try:
        token_type, token = token.split(" ", 1)
    except ValueError:
        warning("Invalid OAuth token - Token Issue")
        return None
    if token_type.lower() != "bearer":
        warning("Invalid OAuth token - Non Bearer")
        return None
    try:
        userinfo = await oauth.google.userinfo(token={"access_token": token})
        success(f"OAuth token validated successfully for user: {userinfo.get('email')}")
    except Exception:
        warning("OAuth token validation failed")
        return None
    return OIDCUser.from_userinfo(userinfo)


async def verify_oauth_customer_cred(oidc: OIDCUser = Depends(current_user), db: AsyncSession = Depends(get_db)) -> Customer:
    """
    Verify OAuth customer credentials and retrieve or create customer record.

    This function first checks if a customer with the OAuth email exists in the
    regular email column (basic auth users). If found, it updates that record with
    OAuth information. If not found, it checks for existing OAuth users, and finally
    creates a new customer record if none exists.

    :param oidc: Authenticated OIDC user object containing user information.
    :param db: Database session to query and create customer data.

    :return: The customer object if authentication is successful.

    :raises HTTPException: If database operations fail.
    """
    if not oidc:
        return None

    query = select(Customer).where(Customer.email == oidc.email).options(selectinload("*"))
    result = await db.execute(query)
    customer_by_email = result.scalar_one_or_none()
    if customer_by_email:
        general(f"Updating existing customer with OAuth info: {oidc.email}")
        customer_by_email.oauth_provider = "google"
        customer_by_email.oauth_id = oidc.sub
        customer_by_email.oauth_email = oidc.email
        customer_by_email.is_verified = True
        customer_by_email.update_date = datetime.now(timezone.utc)
        db.add(customer_by_email)
        try:
            await db.flush()
        except Exception as expt:  # pragma: no cover
            # HTTP status code 500 is already tested in other parts of the codebase
            failure("Failed to update customer details in database due to unexpected error")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected database error occurred.") from expt
    else:
        query = select(Customer).where(Customer.oauth_email == oidc.email).options(selectinload("*"))
        result = await db.execute(query)
        customer_by_email = result.scalar_one_or_none()
        if not customer_by_email:
            general(f"Creating new customer via OAuth: {oidc.email}")
            customer_by_email = Customer(
                email=oidc.email,
                name=oidc.name,
                uuid=uuid4().hex[0:8],
                is_verified=True,  # OAuth emails are pre-verified
                oauth_provider="google",
                oauth_id=oidc.sub,
                oauth_email=oidc.email,
                created_via_oauth=True,
            )
            db.add(customer_by_email)
            try:
                await db.flush()
            except Exception as expt:  # pragma: no cover
                # HTTP status code 500 is already tested in other parts of the codebase
                failure("Failed to create customer account in database due to unexpected error")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected database error occurred.") from expt
    success(f"Customer OAuth authentication successful: {oidc.email}")
    return customer_by_email


async def verify_oauth_business_cred(oidc: OIDCUser = Depends(current_user), db: AsyncSession = Depends(get_db)) -> Business:
    """
    Verify OAuth business credentials and retrieve or create business record.

    This function first checks if a business with the OAuth email exists in the
    regular email column (basic auth users). If found, it updates that record with
    OAuth information. If not found, it checks for existing OAuth users, and finally
    creates a new business record if none exists.

    :param oidc: Authenticated OIDC user object containing user information.
    :param db: Database session to query and create business data.

    :return: The business object if authentication is successful.

    :raises HTTPException: If database operations fail.
    """
    if not oidc:
        return None

    query = select(Business).where(Business.email == oidc.email).options(selectinload("*"))
    result = await db.execute(query)
    business_by_email = result.scalar_one_or_none()
    if business_by_email:
        general(f"Updating existing business with OAuth info: {oidc.email}")
        business_by_email.oauth_provider = "google"
        business_by_email.oauth_id = oidc.sub
        business_by_email.oauth_email = oidc.email
        business_by_email.is_verified = True
        business_by_email.update_date = datetime.now(timezone.utc)
        db.add(business_by_email)
        try:
            await db.flush()
        except Exception as expt:  # pragma: no cover
            # HTTP status code 500 is already tested in other parts of the codebase
            failure("Failed to update business details in database due to unexpected error")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected database error occurred.") from expt
    else:
        query = select(Business).where(Business.oauth_email == oidc.email).options(selectinload("*"))
        result = await db.execute(query)
        business_by_email = result.scalar_one_or_none()
        if not business_by_email:
            general(f"Creating new business via OAuth: {oidc.email}")
            business_by_email = Business(
                email=oidc.email,
                name=oidc.name,
                uuid=uuid4().hex[0:8],
                is_verified=True,  # OAuth emails are pre-verified
                oauth_provider="google",
                oauth_id=oidc.sub,
                oauth_email=oidc.email,
                created_via_oauth=True,
            )
            db.add(business_by_email)
            try:
                await db.flush()
            except Exception as expt:  # pragma: no cover
                # HTTP status code 500 is already tested in other parts of the codebase
                failure("Failed to create business account in database due to unexpected error")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected database error occurred.") from expt
    success(f"Business OAuth authentication successful: {oidc.email}")
    return business_by_email
