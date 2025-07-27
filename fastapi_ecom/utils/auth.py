from typing import Optional

from fastapi import Depends, HTTPException, status

from fastapi_ecom.database.models.business import Business
from fastapi_ecom.database.models.customer import Customer
from fastapi_ecom.utils.basic_auth import verify_basic_business_cred, verify_basic_customer_cred
from fastapi_ecom.utils.oauth import verify_oauth_business_cred, verify_oauth_customer_cred


async def verify_cust_cred(
    basic_customer: Optional[Customer] = Depends(verify_basic_customer_cred),
    oauth_customer: Optional[Customer] = Depends(verify_oauth_customer_cred)
) -> Customer:
    """
    Verify customer credentials using either HTTP Basic Authentication or OAuth.

    This function attempts to authenticate a customer using multiple authentication
    methods. It first tries HTTP Basic Authentication, then falls back to OAuth
    authentication if basic auth is not provided or fails.

    :param basic_customer: Customer object from HTTP Basic Authentication or None.
    :param oauth_customer: Customer object from OAuth authentication or None.

    :return: The authenticated customer object.

    :raises HTTPException: If neither authentication method succeeds.
    """
    if basic_customer:
        return basic_customer

    if oauth_customer:
        return oauth_customer

    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Not Authenticated",
    )

async def verify_business_cred(
    basic_business: Optional[Business] = Depends(verify_basic_business_cred),
    oauth_business: Optional[Business] = Depends(verify_oauth_business_cred)
) -> Business:
    """
    Verify business credentials using either HTTP Basic Authentication or OAuth.

    This function attempts to authenticate a business using multiple authentication
    methods. It first tries HTTP Basic Authentication, then falls back to OAuth
    authentication if basic auth is not provided or fails.

    :param basic_business: Business object from HTTP Basic Authentication or None.
    :param oauth_business: Business object from OAuth authentication or None.

    :return: The authenticated business object.

    :raises HTTPException: If neither authentication method succeeds.
    """
    if basic_business:
        return basic_business

    if oauth_business:
        return oauth_business

    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Not Authenticated",
    )
