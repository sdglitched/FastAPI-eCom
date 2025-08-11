from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.security import HTTPBasicCredentials
from httpx import AsyncClient
from pytest_mock import MockerFixture

from fastapi_ecom.utils.basic_auth import security


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {
                "name": "test_prod",
                "description": "test_prod",
                "category": "test",
                "mfg_date": "1900-01-01T00:00:00",
                "exp_date": "1900-01-01T00:00:00",
                "price": 150.05
            },
            id="PRODUCT Post Endpoint - 201 Created",
        )
    ]
)
async def test_create_product(
        test_app: FastAPI,
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        apply_security_override: None,
        mocker: MockerFixture,
        payload: dict[str, str]
) -> None:
    """
    Test the `create` endpoint of the Product API.

    :param test_app: The fixture which returns the FastAPI app instance.
    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param mocker: The mocker fixture of `pytest_mock`.
    :param payload: A dictionary containing the data for product creation.

    :return:
    """
    """
    Mock `uuid4` and `HTTPBasic.__call__`; Override the `security` dependency
    """
    mock_credentials = HTTPBasicCredentials(username="test_business@example.com", password="test_business")
    mocker.patch("fastapi.security.http.HTTPBasic.__call__", return_value=mock_credentials)
    test_app.dependency_overrides[security] = lambda: mock_credentials
    mocker.patch("fastapi_ecom.router.product.uuid4", return_value=UUID("abcd1234abcd1234abcd1234abcd1234"))

    """
    Perform the action of visiting the endpoint
    """
    response = await client.post("/api/v1/product/create", json = payload)

    """
    Test the response
    """
    assert response.status_code == 201
    assert response.json() == {
        "action": "post",
        "product": {
            "name": payload["name"],
            "description": payload["description"],
            "category": payload["category"],
            "mfg_date": payload["mfg_date"],
            "exp_date": payload["exp_date"],
            "price": payload["price"],
            "uuid": "abcd1234",
            "business_id": "d76a11f2"
        }
    }
