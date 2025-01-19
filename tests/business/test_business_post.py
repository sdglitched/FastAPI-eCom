from typing import AsyncGenerator, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


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
        db_test_data: AsyncGenerator[AsyncSession, None],
        payload: Dict[str, str],
        type: str
) -> None:
    """
    Test the `create` endpoint of the Business API.

    :param client: The test client to send HTTP requests.
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
