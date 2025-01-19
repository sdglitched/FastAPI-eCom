from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from fastapi.security import HTTPBasicCredentials
from httpx import AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ecom.utils.auth import security
from tests.order import _test_data_order_details, _test_data_orders


@pytest.mark.parametrize(
    "customer_id, present",
    [
        pytest.param("2b203687", True, id="ORDER GET Endpoint - Fetch all the orders of authenticated customer"),
        pytest.param("b73a7a28", False, id="ORDER GET Endpoint - Fail to fetch orders of authenticated customer")
    ]
)
async def test_get_orders(
        test_app: FastAPI,
        client: AsyncClient,
        db_test_data: AsyncGenerator[AsyncSession, None],
        apply_security_override,
        mocker: MockerFixture,
        customer_id: str,
        present: str
) -> None:
    """
    Test the `get` endpoint for fetching all the order of the authenticated customer of the Order
    API.

    :param test_app: The fixture which returns the FastAPI app instance.
    :param client: The test client to send HTTP requests.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param mocker: The mocker fixture of `pytest_mock`.
    :param customer_id: The UUID of customer to fetch the orders from.
    :param present: A boolean indicating presence of orders for the authenticated customer.

    :return:
    """
    """
    Get the data for assertion
    """
    ords = _test_data_orders()
    order_details = _test_data_order_details()
    orders = []
    for ord in ords.values():
        if ord.user_id == customer_id:  #UUID of the default customer account which is used for testing
            order_items = [
                {
                    "product_id": detail.product_id,
                    "quantity": detail.quantity,
                    "price": detail.price
                } for detail in order_details.values()
                if detail.order_id == ord.uuid
            ]
            total_price = sum(item["quantity"] * item["price"] for item in order_items)
            order_view_data = {
                "uuid": ord.uuid,
                "order_date": ord.order_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "total_price": total_price,
                "order_items": order_items
            }
            orders.append(order_view_data)

    """
    Mock `HTTPBasic.__call__` and override the `security` dependency
    """
    if not present:
        mock_credentials = HTTPBasicCredentials(username="duplicate_customer@example.com", password="duplicate_customer")
        mocker.patch("fastapi.security.http.HTTPBasic.__call__", return_value=mock_credentials)
        test_app.dependency_overrides[security] = lambda: mock_credentials

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/order/search")

    """
    Test the response
    """
    if present:
        assert response.status_code == 200
        assert response.json() == {
            "action": "get",
            "orders": orders
        }
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "No orders in database"

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="ORDER GET Endpoint - Fetch all the orders")
    ]
)
async def test_get_orders_internal(
        client: AsyncClient,
        db_test_data: AsyncGenerator[AsyncSession, None],
        _: None
) -> None:
    """
    Test the `get` endpoint for fetching all the orders of the Order API.

    :param client: The test client to send HTTP requests.
    :param db_test_data: Fixture to populate the test database with initial test data.

    :return:
    """
    """
    Get the data for assertion
    """
    ords = _test_data_orders()
    order_details = _test_data_order_details()
    orders = []
    for ord in ords.values():
        order_items = [
            {
                "uuid": detail.uuid,
                "product_id": detail.product_id,
                "quantity": detail.quantity,
                "price": detail.price
            } for detail in order_details.values()
            if detail.order_id == ord.uuid
        ]
        total_price = sum(item["quantity"] * item["price"] for item in order_items)
        order_view_data = {
            "uuid": ord.uuid,
            "user_id": ord.user_id,
            "order_date": ord.order_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
            "total_price": total_price,
            "order_items": order_items
        }
        orders.append(order_view_data)

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/order/search/internal")

    """
    Test the response
    """
    assert response.status_code == 200
    assert response.json() == {
        "action": "get",
        "orders": orders
    }

@pytest.mark.parametrize(
    "order_id, present",
    [
        pytest.param("375339b1", True, id="ORDER GET Endpoint - Fetch the specified order of the authenticated customer"),
        pytest.param("xxxx1111", False, id="ORDER GET Endpoint - Fail to fetch the specified order of the authenticated customer")
    ]
)
async def test_get_order_by_uuid(
        client: AsyncClient,
        db_test_data: AsyncGenerator[AsyncSession, None],
        apply_security_override,
        order_id: str,
        present: str
) -> None:
    """
    Test the `get` endpoint for fetching all the orders of the Order API.

    :param client: The test client to send HTTP requests.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param order_id: The UUID of the specific order.
    :param present: A boolean indicating presence of orders for the authenticated customer.

    :return:
    """
    """
    Get the data for assertion
    """
    ords = _test_data_orders()
    order_details = _test_data_order_details()
    for ord in ords.values():
        if ord.uuid == order_id:
            order_items = [
                {
                    "product_id": detail.product_id,
                    "quantity": detail.quantity,
                    "price": detail.price
                } for detail in order_details.values()
                if detail.order_id == ord.uuid
            ]
            total_price = sum(item["quantity"] * item["price"] for item in order_items)
            order = {
                "uuid": ord.uuid,
                "order_date": ord.order_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "total_price": total_price,
                "order_items": order_items
            }

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get(f"/api/v1/order/search/uuid/{order_id}")

    """
    Test the response
    """
    if present:
        assert response.status_code == 200
        assert response.json() == {
            "action": "get",
            "order": order
        }
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Order not present in database"
