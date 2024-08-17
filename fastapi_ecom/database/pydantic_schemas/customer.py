from abc import ABC
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from fastapi_ecom.database.pydantic_schemas.util import APIResult


class CustomerBase(BaseModel, ABC):
    """
    Base: Customer
    """

    class Config:
        from_attributes = True


class CustomerView(CustomerBase):
    email: str
    name: str
    addr_line_1: str
    addr_line_2: str
    city: str
    state: str


class CustomerCreate(CustomerView):
    password: str


class CustomerUpdate(BaseModel):
    email: Optional[str] = ""
    name: Optional[str] = ""
    addr_line_1: Optional[str] = ""
    addr_line_2: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    password: Optional[str] = ""


class CustomerInternal(CustomerCreate):
    id: int
    uuid: str
    is_verified: bool = False
    creation_date: datetime


class CustomerResult(APIResult):
    customer: CustomerView


class CustomerManyResult(APIResult):
    customers: List[CustomerView] = []
