from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from fastapi_ecom.database.pydantic_schemas.util import APIResult


class BusinessBase(BaseModel):
    """
    Base model for business-related schemas, providing shared configurations.
    """
    class Config:
        """
        This class enables attribute mapping from database model instances to Pydantic models
        automatically using the `from_attributes` setting.

        :cvar from_attributes: Flag that enables Pydantic to handle attribute assignment from
                               input data directly (i.e., allow assigning to the model attributes
                               directly without validation).
        """
        from_attributes = True


class BusinessView(BusinessBase):
    """
    Schema for viewing business information.

    :ivar email: Email address of the business.
    :ivar name: Name of the business.
    :ivar addr_line_1: Primary address line of the business.
    :ivar addr_line_2: Secondary address line of the business, optional.
    :ivar city: City in which the business is located.
    :ivar state: State in which the business is located.
    """
    email: EmailStr
    name: str
    addr_line_1: Optional[str]
    addr_line_2: Optional[str]
    city: Optional[str]
    state: Optional[str]


class BusinessCreate(BusinessView):
    """
    Schema for creating a new business.
    This schema inherits from `BusinessView` to include common business view attributes.

    :ivar password: Password for the business account.
    """
    password: str


class BusinessUpdate(BaseModel):
    """
    Schema for updating existing business information, with all fields optional.

    :ivar email: Updated email address of the business, optional.
    :ivar name: Updated name of the business, optional.
    :ivar addr_line_1: Updated primary address line, optional.
    :ivar addr_line_2: Updated secondary address line, optional.
    :ivar city: Updated city of the business, optional.
    :ivar state: Updated state of the business, optional.
    :ivar password: Updated password for the business account, optional.
    """
    email: Optional[EmailStr] = ""
    name: Optional[str] = ""
    addr_line_1: Optional[str] = ""
    addr_line_2: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    password: Optional[str] = ""


class BusinessInternal(BusinessCreate):
    """
    Internal schema for business data, including additional internal details.
    This schema inherits from `BusinessCreate` to include common business create attributes.

    :ivar id: Unique identifier for the business.
    :ivar uuid: Short UUID for uniquely identifying the business.
    :ivar is_verified: Indicates whether the business has been verified, defaults to False.
    :ivar creation_date: Timestamp of when the business was created.
    """
    id: int
    uuid: str
    is_verified: bool = False
    creation_date: datetime


class BusinessResult(APIResult):
    """
    Schema for a single business result in API responses.

    :ivar business: Contains details of a single business.
    """
    business: BusinessView


class BusinessManyResult(APIResult):
    """
    Schema for a list of business results in API responses.

    :ivar businesses: List of businesses with their details.
    """
    businesses: list[BusinessView] = []
