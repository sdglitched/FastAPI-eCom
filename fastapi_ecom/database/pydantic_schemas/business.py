from abc import ABC
from datetime import datetime
from typing import List

from pydantic import BaseModel

from fastapi_ecom.database.pydantic_schemas.util import APIResult


class BusinessBase(BaseModel, ABC):
    """
    Base: Business
    """

    class Config:
        from_attributes = True


class BusinessView(BusinessBase):
    email: str
    name: str
    addr_line_1: str
    addr_line_2: str
    city: str
    state: str


class BusinessCreate(BusinessView):
    password: str


class BusinessUpdate(BusinessCreate):
    pass


class BusinessInternal(BusinessUpdate):
    id: int
    uuid: str
    is_verified: bool = False
    creation_date: datetime


class BusinessResult(APIResult):
    business: BusinessView


class BusinessManyResult(APIResult):
    businesses: List[BusinessView] = []
