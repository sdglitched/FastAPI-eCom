from typing import Dict

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "payload, type",
    [
        pytest.param(
            {
                "email": "update_business@example.com",
                "name": "update_business",
                "addr_line_1": "abc",
                "addr_line_2": "xyz",
                "city": "aaa",
                "state": "bbb",
                "password": "update_business"
            },
            "update",
            id="BUSINESS PUT Endpoint - Updates currently authenticated business",
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
            id="BUSINESS PUT Endpoint - 409 Conflict",
        )
    ]
)
async def test_update_business(client: AsyncClient, payload: Dict[str, str], type: str) -> None:
    """
    Test the `put` endpoint for updating the currently authenticated business of the Business API.

    :param client: The test client to send HTTP requests.

    :return:
    """
    """
    Perform the action of visiting the endpoint
    """
    response = await client.put("/api/v1/business/update/me", json = payload)

    """
    Test the response
    """
    if type == "update":
        assert response.status_code == 202
        assert response.json() == {
            "action": "put",
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
