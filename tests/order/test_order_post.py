from datetime import datetime
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.security import HTTPBasicCredentials
from httpx import AsyncClient
from pytest_mock import MockerFixture

from fastapi_ecom.utils.basic_auth import security


@pytest.mark.parametrize(
    "payload, present",
    [
        pytest.param(
            {
                "order_date": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "order_items": [{"product_id": "3250fcbe", "quantity": 5}],
            },
            True,
            id="ORDER Post Endpoint - 201 Created",
        ),
        pytest.param(
            {
                "order_date": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "order_items": [{"product_id": "xxxxxxx", "quantity": 5}],
            },
            False,
            id="ORDER Post Endpoint - Fail to place order for product which doesn't exist",
        ),
    ],
)
async def test_create_order(
    test_app: FastAPI,
    client: AsyncClient,
    db_test_create: None,
    db_test_data: None,
    apply_security_override: None,
    mocker: MockerFixture,
    payload: dict,
    present: bool,
) -> None:
    """
    Test the `create` endpoint of the Order API.

    :param test_app: The fixture which returns the FastAPI app instance.
    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param mocker: The mocker fixture of `pytest_mock`.
    :param payload: A dictionary containing the data for order creation.
    :param present: A boolean indicating presence of product.

    :return:
    """
    """
    Mock `uuid4` and `HTTPBasic.__call__`; Override the `security` dependency
    """
    mock_credentials = HTTPBasicCredentials(username="test_customer@example.com", password="test_customer")
    mocker.patch("fastapi.security.http.HTTPBasic.__call__", return_value=mock_credentials)
    test_app.dependency_overrides[security] = lambda: mock_credentials
    mocker.patch("fastapi_ecom.router.order.uuid4", return_value=UUID("abcd1234abcd1234abcd1234abcd1234"))

    """
    Perform the action of visiting the endpoint
    """
    response = await client.post("/api/v1/order/create", json=payload)

    """
    Test the response
    """
    if present:
        assert response.status_code == 201
        assert response.json() == {
            "action": "post",
            "order": {
                "order_date": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "uuid": "abcd1234",
                "total_price": payload["order_items"][0]["quantity"] * 100.0,  # Price from product test data
                "user_id": "2c92f0e8",  # UUID from customer test data
                "order_items": [
                    {
                        "product_id": payload["order_items"][0]["product_id"],
                        "quantity": payload["order_items"][0]["quantity"],
                        "price": 100.0,  # Price from product test data
                        "uuid": "abcd1234",
                    }
                ],
            },
        }
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == f"Product with ID: {payload['order_items'][0]['product_id']} does not exist."
