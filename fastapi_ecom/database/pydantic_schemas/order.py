from datetime import datetime

from pydantic import BaseModel

from fastapi_ecom.database.pydantic_schemas.order_details import (
    OrderDetailsCreate,
    OrderDetailsView,
    OrderDetailsViewInternal,
)
from fastapi_ecom.database.pydantic_schemas.util import APIResult


class OrderBase(BaseModel):
    """
    Base model for order-related schemas, providing shared configurations.
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


class OrderCreate(OrderBase):
    """
    Schema for creating a new order, including order date and associated order items.

    :ivar order_date: Date and time when the order was placed.
    :ivar order_items: List of order details, including product information and quantity.
    """
    order_date: datetime
    order_items: list[OrderDetailsCreate]


class OrderView(OrderCreate):
    """
    Schema for viewing an order, including additional details such as total price and order UUID.
    This schema inherits from `OrderCreate` to include common order create attributes.

    :ivar uuid: Unique identifier for the order.
    :ivar total_price: Total price of all items in the order.
    :ivar order_items: Detailed information about the items in the order.
    """
    uuid: str
    total_price: float
    order_items: list[OrderDetailsView]


class OrderViewInternal(OrderView):
    """
    Internal schema for viewing order details, including user information and internal details.
    This schema inherits from `OrderView` to include common order view attributes.

    :ivar user_id: UUID of the user who placed the order.
    :ivar order_items: Detailed information about the items in the order, including internal
                       identifiers.
    """
    user_id: str
    order_items: list[OrderDetailsViewInternal]


# class OrderUpdate(BaseModel):
#     order_items: Optional[list[OrderDetailsUpdate]]


class OrderResult(APIResult):
    """
    Schema for a single order result in API responses.

    :ivar order: Contains detailed information about a single order.
    """
    order: OrderView


class OrderResultInternal(APIResult):
    """
    Schema for a single order result in API responses, including unique identifiers.

    :ivar order: Contains detailed information about a single order, including internal details.
    """
    order: OrderViewInternal


class OrderManyResult(APIResult):
    """
    Schema for a list of orders in API responses.

    :ivar orders: List of orders with detailed information.
    """
    orders: list[OrderView] = []


class OrderManyResultInternal(APIResult):
    """
    Schema for a list of internal orders in API responses, including unique identifiers.

    :ivar orders: List of orders with detailed internal information.
    """
    orders: list[OrderViewInternal] = []
