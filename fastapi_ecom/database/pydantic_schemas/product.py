from abc import ABC
from datetime import datetime
from typing import List, Optional

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


class ProductViewInternal(ProductView):
    uuid: str
    business_id: str


class ProductCreate(ProductView):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = ""
    description: Optional[str] = ""
    category: Optional[str] = ""
    mfg_date: Optional[datetime] = "1900-01-01T00:00:00.000Z"
    exp_date: Optional[datetime] = "1900-01-01T00:00:00.000Z"
    price: Optional[float] = 0.0


class ProductInternal(ProductCreate):
    id: int
    uuid: str
    business_id: str


class ProductResult(APIResult):
    product: ProductView


class ProductResultInternal(APIResult):
    product: ProductViewInternal


class ProductManyResult(APIResult):
    products: List[ProductView] = []


class ProductManyResultInternal(APIResult):
    products: List[ProductViewInternal] = []
