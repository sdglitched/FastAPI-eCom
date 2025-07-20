from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from fastapi_ecom.database.pydantic_schemas.util import APIResult


class CustomerBase(BaseModel):
    """
    Base model for customer-related schemas, providing shared configurations.
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


class CustomerView(CustomerBase):
    """
    Schema for viewing customer information.

    :ivar email: Email address of the customer.
    :ivar name: Full name of the customer.
    :ivar addr_line_1: Primary address line of the customer.
    :ivar addr_line_2: Secondary address line of the customer, optional.
    :ivar city: City in which the customer resides.
    :ivar state: State in which the customer resides.
    """
    email: EmailStr
    name: str
    addr_line_1: str
    addr_line_2: str
    city: str
    state: str


class CustomerCreate(CustomerView):
    """
    Schema for creating a new customer.
    This schema inherits from `CustomerView` to include common customer view attributes.

    :ivar password: Password for the customer account.
    """
    password: str


class CustomerUpdate(BaseModel):
    """
    Schema for updating existing customer information, with all fields optional.

    :ivar email: Updated email address of the customer, optional.
    :ivar name: Updated name of the customer, optional.
    :ivar addr_line_1: Updated primary address line, optional.
    :ivar addr_line_2: Updated secondary address line, optional.
    :ivar city: Updated city of the customer, optional.
    :ivar state: Updated state of the customer, optional.
    :ivar password: Updated password for the customer account, optional.
    """
    email: Optional[EmailStr] = ""
    name: Optional[str] = ""
    addr_line_1: Optional[str] = ""
    addr_line_2: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    password: Optional[str] = ""


class CustomerInternal(CustomerCreate):
    """
    Internal schema for customer data, including additional internal details.
    This schema inherits from `CustomerCreate` to include common customer create attributes.

    :ivar id: Unique identifier for the customer.
    :ivar uuid: Short UUID for uniquely identifying the customer.
    :ivar is_verified: Indicates whether the customer has been verified, defaults to False.
    :ivar creation_datetime: Timestamp of when the customer was created.
    """
    id: int
    uuid: str
    is_verified: bool = False
    creation_date: datetime


class CustomerResult(APIResult):
    """
    Schema for a single customer result in API responses.

    :ivar customer: Contains details of a single customer.
    """
    customer: CustomerView


class CustomerManyResult(APIResult):
    """
    Schema for a list of customer results in API responses.

    :ivar customers: List of customer details.
    """
    customers: list[CustomerView] = []
