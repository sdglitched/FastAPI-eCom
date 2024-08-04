from abc import ABC
from datetime import datetime
from typing import List

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


class CustomerUpdate(CustomerCreate):
    pass


class CustomerInternal(CustomerUpdate):
    id: int
    uuid: str
    is_verified: bool = False
    creation_date: datetime


class CustomerResult(APIResult):
    customer: CustomerView


class CustomerManyResult(APIResult):
    customers: List[CustomerView] = []
