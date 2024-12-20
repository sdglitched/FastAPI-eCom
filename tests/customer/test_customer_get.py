import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from tests.customer import _test_data_customer


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="CUSTOMER GET Endpoint - Fetch email of the authenticated customer")
    ]
)
async def test_get_customer_me(client: AsyncClient, _: None) -> None:
    """
    Test the `get` endpoint for the currently authenticated customer of the Customer API.

    :param client: The test client to send HTTP requests.

    :return:
    """
    """
    Get the data for testing
    """
    data = _test_data_customer()

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/customer/me")

    """
    Test the response
    """
    assert response.status_code == 200
    assert response.json() == {
        "action": "get",
        "email": data["delete_customer"].email  #The override for the authentication uses this email
    }

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="CUSTOMER GET Endpoint - Fail authentication for customer")
    ]
)
async def test_get_customer_me_fail(client: AsyncClient, mocker: MockerFixture, _: None) -> None:
    """
    Test the `get` endpoint for the incorrectly authenticated customer of the Customer API.

    :param client: The test client to send HTTP requests.
    :param mocker: Mock fixture to be used for mocking desired functionality

    :return:
    """
    """
    Mock the password check
    """
    mocker.patch("bcrypt.checkpw", return_value=False)

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/customer/me")

    """
    Test the response
    """
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="CUSTOMER GET Endpoint - Fetch all the customers")
    ]
)
async def test_get_customers(client: AsyncClient, _: None) -> None:
    """
    Test the `get` endpoint for fetching all the customers of the Customer API.

    :param client: The test client to send HTTP requests.

    :return:
    """
    """
    Get the data for testing
    """
    data = _test_data_customer()
    customers = [
        {
            "email": customer.email,
            "name": customer.name,
            "addr_line_1": customer.addr_line_1,
            "addr_line_2": customer.addr_line_2,
            "city": customer.city,
            "state": customer.state
        } for customer in data.values()
    ]

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/customer/search")

    """
    Test the response
    """
    assert response.status_code == 200
    assert response.json() == {
        "action": "get",
        "customers": customers
    }

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="CUSTOMER GET Endpoint - Fail to fetch customer")
    ]
)
async def test_get_customers_fail(_: None) -> None:
    """
    TODO: Test the `get` endpoint for fetching no records from database of the Customer API.

    :return:
    """
    pass
