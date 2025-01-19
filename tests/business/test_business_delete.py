from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.business import _test_data_business


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="BUSINESS DELETE Endpoint - Deletes currently authenticated business")
    ]
)
async def test_delete_business(
        client: AsyncClient,
        db_test_data: AsyncGenerator[AsyncSession, None],
        apply_security_override,
        _: None
) -> None:
    """
    Test the `delete` endpoint for deleting the currently authenticated business of the Business
    API.

    :param client: The test client to send HTTP requests.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.

    :return:
    """
    """
    Get the data for testing
    """
    data = _test_data_business()

    """
    Perform the action of visiting the endpoint
    """
    response = await client.delete("/api/v1/business/delete/me")

    """
    Test the response
    """
    assert response.status_code == 202
    assert response.json() == {
        "action": "delete",
        "business": {
            "email": data["delete_business"].email,
            "name": data["delete_business"].name,
            "addr_line_1": data["delete_business"].addr_line_1,
            "addr_line_2": data["delete_business"].addr_line_2,
            "city": data["delete_business"].city,
            "state": data["delete_business"].state
        }
    }
