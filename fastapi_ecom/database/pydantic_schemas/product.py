from abc import ABC
from datetime import datetime
from typing import List

from pydantic import BaseModel

from fastapi_ecom.database.pydantic_schemas.util import APIResult


class ProductBase(BaseModel, ABC):
    """
    Base: Product
    """

    class Config:
        from_attributes = True


class ProductView(ProductBase):
    name: str
    description: str
    category: str
    mfg_date: datetime
    exp_date: datetime
    price: float


class ProductCreate(ProductView):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductInternal(ProductUpdate):
    id: int
    uuid: str
    business_id: str


class ProductResult(APIResult):
    product: ProductView


class ProductManyResult(APIResult):
    products: List[ProductView] = []
