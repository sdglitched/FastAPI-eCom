from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.models.order import Order
from fastapi_ecom.database.models.order_details import OrderDetail
from fastapi_ecom.database.models.product import Product
from fastapi_ecom.database.pydantic_schemas.order import (
    OrderCreate,
    OrderManyResult,
    OrderManyResultInternal,
    OrderResult,
    OrderResultInternal,
    OrderView,
    OrderViewInternal,
)
from fastapi_ecom.database.pydantic_schemas.order_details import (
    OrderDetailsView,
    OrderDetailsViewInternal,
)
from fastapi_ecom.utils.auth import verify_cust_cred
from fastapi_ecom.utils.logging_setup import failure, general, warning

router = APIRouter(prefix="/order")

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=OrderResultInternal, tags=["order"])
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db), customer_auth = Depends(verify_cust_cred)) -> OrderResultInternal:
    """
    Endpoint to place an order by the authenticated customer.

    :param order: Input data for placing a new order. Must adhere to the `OrderCreate` schema.
    :param db: Active asynchronous database session dependency.
    :param customer_auth: Authenticated customer object.

    :return: Dictionary containing the action type and the added product data, validated and
             serialized using the `OrderViewInternal` schema.

    :raises HTTPException:
        If database integrity constraints fails, it returns a 500 Internal Server Error.
    """
    new_order = Order(
        user_id = customer_auth.uuid,
        order_date = order.order_date,
        total_price = 0.0,  # Initial total, calculated below
        uuid = uuid4().hex[0:8]  # Assign UUID manually; One UUID per transaction
    )
    db.add(new_order)
    try:
        await db.flush()  # Generate order ID for relations
    except Exception as expt:  #pragma: no cover
        """
        This part of the code cannot be tested as this endpoint performs multiple database
        interactions due to which mocking one part wont produce the desired result. Thus,
        we will keep it uncovered until a alternative can be made for testing this exception block.
        """
        failure(f"Order creation failed with unexpected error for customer: {customer_auth.email}")
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred."
            ) from expt

    # Create OrderDetail entries and calculate the total price
    total_price = 0
    order_items = []
    for item in order.order_items:
        query = select(Product).where(Product.uuid == item.product_id)
        result = await db.execute(query)
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Product with ID: {item.product_id} does not exist."
            )
        total_price += product.price * item.quantity
        order_detail = OrderDetail(
            order_id = new_order.uuid,
            product_id = item.product_id,
            quantity = item.quantity,
            price = product.price,
            uuid = uuid4().hex[0:8]  # Assign UUID manually; One UUID per transaction
        )
        db.add(order_detail)
        order_items.append(order_detail)

    # Update total price of the order
    new_order.total_price = total_price
    try:
        await db.flush()
    except Exception as expt:  #pragma: no cover
        """
        This part of the code cannot be tested as this endpoint performs multiple database
        interactions due to which mocking one part wont produce the desired result. Thus,
        we will keep it uncovered until a alternative can be made for testing this exception block.
        """
        failure(f"Order creation failed with unexpected error for customer: {customer_auth.email}")
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred."
            ) from expt
    new_order.order_items = order_items
    return {
        "action": "post",
        "order": OrderViewInternal.model_validate(new_order).model_dump()
    }

@router.get("/search", status_code=status.HTTP_200_OK, response_model=OrderManyResult, tags=["order"])
async def get_orders(
    skip: int = Query(0, ge=0, description="Number of records to skip (must be between 0 and int64)"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return (must be between 1 and 100)"),
    db: AsyncSession = Depends(get_db),
    customer_auth = Depends(verify_cust_cred)
) -> OrderManyResult:
    """
    Endpoint fetches a paginated list of orders and its details associated with the authenticated
    customer.

    This endpoint handles nested relationships between orders and their order details manually, as
    automatic validation using `model_validate` may fail for deeply nested SQLAlchemy relationships.

    As per some articles: In practice, especially with ORM models from SQLAlchemy, Pydantic sometimes
    struggles with deep nested relationshsips (like order_items in Order). This often occurs because
    SQLAlchemy relationships, loaded with .options(selectinload()), aren't automatically parsed as
    lists of model objects. When using SQLAlchemy relationships, Pydantic might misinterpret the
    fields or miss data if any nested models aren't explicitly prepared.

    :param skip: Number of records to skip. Must be between 0 and int64.
    :param limit: Maximum number of records to return. Must be between 1 and 100.
    :param db: Active asynchronous database session dependency.
    :param customer_auth: Authenticated customer object.

    :return: Dictionary containing the action type and the list of orders with their details.

    :raises HTTPException:
        If no products are associated with the authenticated customer, it raises 404 Not Found.
    """
    general(f"Searching orders for customer {customer_auth.email} with skip={skip}, limit={limit}")
    query = select(Order).where(Order.user_id == customer_auth.uuid).options(selectinload(Order.order_details)).offset(skip).limit(limit)
    result = await db.execute(query)
    orders = result.scalars().unique().all()
    if not orders:
        warning(f"No order found in database for customer {customer_auth.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No orders in database"
        )
    order_views = []
    for order in orders:
        order_items = [
            OrderDetailsView(
                product_id = detail.product_id,
                quantity = detail.quantity,
                price = detail.price
            )
            for detail in order.order_details
        ]
        order_view_data = OrderView(
            uuid = order.uuid,
            order_date = order.order_date,
            total_price = order.total_price,
            order_items = order_items
        )
        order_views.append(order_view_data.model_dump())
    return {
        "action": "get",
        "orders": order_views
    }

@router.get("/search/internal", status_code=status.HTTP_200_OK, response_model=OrderManyResultInternal, tags=["order"])
async def get_orders_internal(
    skip: int = Query(0, ge=0, description="Number of records to skip (must be between 0 and int64)"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return (must be between 1 and 100)"),
    db: AsyncSession = Depends(get_db)
) -> OrderManyResultInternal:
    """
    Endpoint fetches a paginated list of orders and its details.

    This endpoint handles nested relationships between orders and their order details manually, as
    automatic validation using `model_validate` may fail for deeply nested SQLAlchemy relationships.

    As per some articles: In practice, especially with ORM models from SQLAlchemy, Pydantic sometimes
    struggles with deep nested relationshsips (like order_items in Order). This often occurs because
    SQLAlchemy relationships, loaded with .options(selectinload()), aren't automatically parsed as
    lists of model objects. When using SQLAlchemy relationships, Pydantic might misinterpret the
    fields or miss data if any nested models aren't explicitly prepared.

    :param skip: Number of records to skip. Must be between 0 and int64.
    :param limit: Maximum number of records to return. Must be between 1 and 100.
    :param db: Active asynchronous database session dependency.

    :return: Dictionary containing the action type and the list of orders with their details.

    :raises HTTPException:
        If no products are associated with the authenticated customer, it raises 404 Not Found.
    """
    query = select(Order).options(selectinload(Order.order_details)).offset(skip).limit(limit)
    result = await db.execute(query)
    orders = result.scalars().unique().all()
    if not orders:
        warning("No order found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No orders in database"
        )
    order_views = []
    for order in orders:
        order_items = [
            OrderDetailsViewInternal(
                product_id = detail.product_id,
                quantity = detail.quantity,
                price = detail.price,
                uuid = detail.uuid
            )
            for detail in order.order_details
        ]
        order_view_data = OrderViewInternal(
            uuid = order.uuid,
            user_id = order.user_id,
            order_date = order.order_date,
            total_price = order.total_price,
            order_items = order_items
        )
        order_views.append(order_view_data.model_dump())
    return {
        "action": "get",
        "orders": order_views
    }

@router.get("/search/uuid/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResult, tags=["order"])
async def get_order_by_uuid(order_id: str, db: AsyncSession = Depends(get_db), customer_auth = Depends(verify_cust_cred)):
    """
    Endpoint fetches a specific order and its details by its UUID associated with the authenticated
    customer.

    :param order_id: The UUID of the order to retrieve.
    :param db: Active asynchronous database session dependency.
    :param customer_auth: Authenticated customer object.

    :return: Dictionary containing the action type and order details, validated and
             serialized using the `OrderView` schema.

    :raises HTTPException:
        If no products are associated with the authenticated customer, it raises 404 Not Found.
    """
    query = select(Order).where(and_(Order.user_id == customer_auth.uuid, Order.uuid == order_id)).options(selectinload(Order.order_details))
    result = await db.execute(query)
    order = result.scalar_one_or_none()
    if not order:
        warning(f"Order {order_id} no present in database")
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Order not present in database"
        )
    order_items = [
        OrderDetailsView(
            product_id = detail.product_id,
            quantity = detail.quantity,
            price = detail.price
        )
        for detail in order.order_details
    ]
    order_view = OrderView(
        uuid = order.uuid,
        order_date = order.order_date,
        total_price = order.total_price,
        order_items = order_items
    )
    return {
        "action": "get",
        "order": OrderView.model_validate(order_view).model_dump()
    }

# @router.put("/update/uuid/{order_id}", response_model=OrderResult, tags=["order"])
# async def update_order():
#       """
#       TODO: Update endpoint will be made available one the carting system is implemented
#       """

@router.delete("/delete/uuid/{order_id}", status_code=status.HTTP_202_ACCEPTED, response_model=OrderResult, tags=["order"])
async def delete_order(order_id: str, db: AsyncSession = Depends(get_db), customer_auth = Depends(verify_cust_cred)) -> OrderResult:
    """
    Endpoint to delete a order by its UUID associated for an authenticated customer.

    :param order_id: The UUID of the order to retrieve.
    :param db: Active asynchronous database session dependency.
    :param customer_auth: Authenticated customer object.

    :return: Dictionary containing the action type and order details, validated and serialized
             using the `OrderView` schema.

    :raises HTTPException:
        - If no order with the given UUID is associated with the authenticated customer, it
          raises 404 Not Found.
        - If there are other database errors, it returns a 500 Internal Server Error.
    """
    query = select(Order).where(and_(Order.user_id == customer_auth.uuid, Order.uuid == order_id)).options(selectinload(Order.order_details))
    result = await db.execute(query)
    order_to_delete = result.scalar_one_or_none()
    if not order_to_delete:
        warning(f"Order {order_id} no present in database")
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Order not present in database"
        )
    order_items = [
        OrderDetailsView(
            product_id = detail.product_id,
            quantity = detail.quantity,
            price = detail.price
        )
        for detail in order_to_delete.order_details
    ]
    order_view = OrderView(
        uuid = order_to_delete.uuid,
        order_date = order_to_delete.order_date,
        total_price = order_to_delete.total_price,
        order_items = order_items
    )
    query = delete(Order).where(and_(Order.user_id == customer_auth.uuid, Order.uuid == order_id))
    await db.execute(query)
    try:
        await db.flush()
    except Exception as expt:  #pragma: no cover
        """
        This part of the code cannot be tested as this endpoint performs multiple database
        interactions due to which mocking one part wont produce the desired result. Thus,
        we will keep it uncovered until a alternative can be made for testing this exception block.
        """
        failure(f"Order deletion failed with unexpected error for customer: {customer_auth.email}")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Failed while deleting"
        ) from expt
    return {
        "action": "delete",
        "order": OrderView.model_validate(order_view)
    }
