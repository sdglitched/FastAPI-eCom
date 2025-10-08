from datetime import datetime

from pydantic import BaseModel

from fastapi_ecom.database.pydantic_schemas.util import APIResult


class ProductBase(BaseModel):
    """
    Base model for product-related schemas, providing shared configurations.
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


class ProductView(ProductBase):
    """
    Schema for viewing product information.

    :ivar name: Name of the product.
    :ivar description: Description of the product.
    :ivar category: Category to which the product belongs.
    :ivar mfg_date: Manufacturing date of the product.
    :ivar exp_date: Expiration date of the product.
    :ivar price: Price of the product.
    """

    name: str
    description: str
    category: str
    mfg_date: datetime
    exp_date: datetime
    price: float


class ProductViewInternal(ProductView):
    """
    Internal schema for viewing product information, including additional identifiers.
    This schema inherits from `ProductView` to include common product view attributes.

    :ivar uuid: Unique identifier for the product.
    :ivar business_id: Identifier for the business associated with the product.
    """

    uuid: str
    business_id: str


class ProductCreate(ProductView):
    """
    Schema for creating a new product, inheriting from ProductView to require standard attributes.
    """

    pass


class ProductUpdate(BaseModel):
    """
    Schema for updating product information, with all fields optional.

    :ivar name: Updated name of the product.
    :ivar description: Updated description of the product.
    :ivar category: Updated category of the product.
    :ivar mfg_date: Updated manufacturing date, defaults to "1900-01-01".
    :ivar exp_date: Updated expiration date, defaults to "1900-01-01".
    :ivar price: Updated price of the product, defaults to 0.0.
    """

    name: str | None = ""
    description: str | None = ""
    category: str | None = ""
    mfg_date: datetime | None = "1900-01-01T00:00:00.000Z"
    exp_date: datetime | None = "1900-01-01T00:00:00.000Z"
    price: float | None = 0.0


class ProductInternal(ProductCreate):
    """
    Internal schema for product data, including additional internal details.
    This schema inherits from `ProductCreate` to include common product create attributes.

    :ivar id: Unique identifier for the product.
    :ivar uuid: Short UUID for uniquely identifying the product.
    :ivar business_id: ID of the business which is associated with this product.
    """

    id: int
    uuid: str
    business_id: str


class ProductResult(APIResult):
    """
    Schema for a single product result in API responses.

    :ivar product: Contains detailed information about a single product.
    """

    product: ProductView


class ProductResultInternal(APIResult):
    """
    Schema for a single product result in API responses, including additional internal details.

    :ivar product: Contains detailed information about a single product, including internal details.
    """

    product: ProductViewInternal


class ProductManyResult(APIResult):
    """
    Schema for a list of products in API responses.

    :ivar products: List of products with detailed information.
    """

    products: list[ProductView] = []


class ProductManyResultInternal(APIResult):
    """
    Schema for a list of products in API responses, including additional internal details.

    :ivar products: List of products with detailed internal information.
    """

    products: list[ProductViewInternal] = []
