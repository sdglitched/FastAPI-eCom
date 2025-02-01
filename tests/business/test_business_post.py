from typing import Dict

import pytest
from fastapi import HTTPException, status
from httpx import AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy import URL


@pytest.mark.parametrize(
    "payload, type",
    [
        pytest.param(
            {
                "email": "test_busi@example.com",
                "name": "test_busi",
                "addr_line_1": "abc",
                "addr_line_2": "xyz",
                "city": "aaa",
                "state": "bbb",
                "password": "test_busi"
            },
            "create",
            id="BUSINESS Post Endpoint - 201 Created",
        ),
        pytest.param(
            {
                "email": "duplicate_business@example.com",
                "name": "duplicate_business",
                "addr_line_1": "abc",
                "addr_line_2": "xyz",
                "city": "aaa",
                "state": "bbb",
                "password": "duplicate_business"
            },
            "duplicate",
            id="BUSINESS Post Endpoint - 409 Conflict",
        )
    ]
)
async def test_create_business(
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        payload: Dict[str, str],
        type: str
) -> None:
    """
    Test the `create` endpoint of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param payload: A dictionary containing the data for business creation.
    :param type: A string indicating the type of test data.

    :return:

    :raises AssertionError: If the response does not match the expected status or data.
    """
    """
    Perform the action of visiting the endpoint
    """
    response = await client.post("/api/v1/business/create", json = payload)

    """
    Test the response
    """
    if type == "create":
        assert response.status_code == 201
        assert response.json() == {
            "action": "post",
            "business": {
                "email": payload["email"],
                "name": payload["name"],
                "addr_line_1": payload["addr_line_1"],
                "addr_line_2": payload["addr_line_2"],
                "city": payload["city"],
                "state": payload["state"]
            }
        }
    else:
        assert response.status_code == 409
        assert response.json()["detail"] == "Uniqueness constraint failed - Please try again"

@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {
                "email": "test_busi@example.com",
                "name": "test_busi",
                "addr_line_1": "abc",
                "addr_line_2": "xyz",
                "city": "aaa",
                "state": "bbb",
                "password": "test_busi"
            },
            id="BUSINESS Post Endpoint - 500 Internal Server Error")
    ]
)
async def test_create_business_fail(
    client: AsyncClient,
    get_test_database_url: URL,
    mocker: MockerFixture,
    payload: Dict[str, str]
) -> None:
    """
    Test the `create` endpoint of the Business API for HTTP_500_INTERNAL_SERVER_ERROR.

    :param client: The test client to send HTTP requests.
    :param get_test_database_url: The fixture which generates test database URL.
    :param mocker: Mock fixture to be used for mocking desired functionality.
    :param payload: A dictionary containing the data for business creation.

    :return:

    :raises AssertionError: If the response does not match the expected status or data.
    """
    """
    Create a mock database session and configure the `flush` method to raise an HTTPException.
    """
    mock_db = mocker.AsyncMock()
    mock_db.flush.side_effect = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected database error occurred."
    )
    mocker.patch("fastapi_ecom.router.business.get_db", return_value=mock_db)

    """
    Perform the action of visiting the endpoint
    """
    response = await client.post("/api/v1/business/create", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "An unexpected database error occurred."
