from abc import ABC
from datetime import datetime
from typing import List, Optional

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


class BusinessUpdate(BaseModel):
    email: Optional[str] = ""
    name: Optional[str] = ""
    addr_line_1: Optional[str] = ""
    addr_line_2: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    password: Optional[str] = ""


class BusinessInternal(BusinessCreate):
    id: int
    uuid: str
    is_verified: bool = False
    creation_date: datetime


class BusinessResult(APIResult):
    business: BusinessView


class BusinessManyResult(APIResult):
    businesses: List[BusinessView] = []
