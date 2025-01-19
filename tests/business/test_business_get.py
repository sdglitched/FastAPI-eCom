from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from tests.business import _test_data_business


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="BUSINESS GET Endpoint - Fetch email of the authenticated business")
    ]
)
async def test_get_business_me(
        client: AsyncClient,
        db_test_data: AsyncGenerator[AsyncSession, None],
        apply_security_override,
        _: None
) -> None:
    """
    Test the `get` endpoint for the currently authenticated business of the Business API.

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
    response = await client.get("/api/v1/business/me")

    """
    Test the response
    """
    assert response.status_code == 200
    assert response.json() == {
        "action": "get",
        "email": data["delete_business"].email  #The override for the authentication uses this email
    }

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="BUSINESS GET Endpoint - Fail authentication for business")
    ]
)
async def test_get_business_me_fail(
        client: AsyncClient,
        db_test_data: AsyncGenerator[AsyncSession, None],
        apply_security_override,
        mocker: MockerFixture,
        _: None
) -> None:
    """
    Test the `get` endpoint for the incorrectly authenticated business of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param mocker: Mock fixture to be used for mocking desired functionality.

    :return:
    """
    """
    Mock the password check
    """
    mocker.patch("bcrypt.checkpw", return_value=False)

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/business/me")

    """
    Test the response
    """
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="BUSINESS GET Endpoint - Fetch all the businesses")
    ]
)
async def test_get_businesses(
        client: AsyncClient,
        db_test_data: AsyncGenerator[AsyncSession, None],
        _: None
) -> None:
    """
    Test the `get` endpoint for fetching all the businesses of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_data: Fixture to populate the test database with initial test data.

    :return:
    """
    """
    Get the data for testing
    """
    data = _test_data_business()
    businesses = [
        {
            "email": business.email,
            "name": business.name,
            "addr_line_1": business.addr_line_1,
            "addr_line_2": business.addr_line_2,
            "city": business.city,
            "state": business.state
        } for business in data.values()
    ]

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/business/search")

    """
    Test the response
    """
    assert response.status_code == 200
    assert response.json() == {
        "action": "get",
        "businesses": businesses
    }

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="BUSINESS GET Endpoint - Fail to fetch business")
    ]
)
async def test_get_businesses_fail(_: None) -> None:
    """
    TODO: Test the `get` endpoint for fething no records from database of the Business API.

    :return:
    """
    pass
