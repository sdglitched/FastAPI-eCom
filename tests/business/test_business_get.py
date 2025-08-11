
import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from tests.business import _test_data_business


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="BUSINESS GET Endpoint - Fetch email of the authenticated business")
    ]
)
async def test_get_business_me(
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        apply_security_override: None,
        _: None
) -> None:
    """
    Test the `get` endpoint for the currently authenticated business of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
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
        pytest.param(None, id="BUSINESS GET Endpoint - Fail authentication for business with incorrect password")
    ]
)
async def test_get_business_me_fail_pwd(
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        apply_security_override: None,
        mocker: MockerFixture,
        _: None
) -> None:
    """
    Test the `get` endpoint for the incorrectly authenticated business of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
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
    assert response.json()["detail"] == "Not Authenticated"

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="BUSINESS GET Endpoint - Fail authentication for business with no user")
    ]
)
async def test_get_business_me_fail_no_user(
        client: AsyncClient,
        db_test_create: None,
        apply_security_override: None,
        _: None
) -> None:
    """
    Test the `get` endpoint for the incorrectly authenticated business of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.

    :return:
    """

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/business/me")

    """
    Test the response
    """
    assert response.status_code == 401
    assert response.json()["detail"] == "Not Authenticated"

@pytest.mark.parametrize(
    "mock_oidc_user",
    [
        pytest.param(
            {
                "email": "dummy_user@example.com",
                "name": "dummy user",
                "sub": "dummy_user_sub"
            },
            id="BUSINESS GET Endpoint - Fetch email of the `dummy` authenticated business with oidc"
        ),
        pytest.param(
            {
                "email": "delete@example.com",
                "name": "delete user",
                "sub": "delete_sub"
            },
            id="BUSINESS GET Endpoint - Fetch email of the `delete` authenticated business with oidc"
        )
    ]
)
async def test_get_business_me_oauth(
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        mock_oidc_user: dict,
        mocker: MockerFixture,
) -> None:
    """
    Test the `get` endpoint for the currently authenticated business of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param mock_oidc_user: Dictonary with dummy odic user details.
    :param mocker: Mock fixture to be used for mocking desired functionality.

    :return:
    """
    """
    Mock the password check for failing basic auth
    """
    mocker.patch("bcrypt.checkpw", return_value=False)

    """
    Use dummy user and mock the oidc implementation
    """
    mocker.patch("fastapi_ecom.utils.oauth.oauth.google.userinfo", return_value=mock_oidc_user)

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/business/me", headers={"Authorization": "Bearer dummy-token"})

    """
    Test the response
    """
    assert response.status_code == 200
    assert response.json() == {
        "action": "get",
        "email": f"{mock_oidc_user["email"]}"
    }

@pytest.mark.parametrize(
    "token",
    [
        pytest.param("Bearer", id="BUSINESS GET Endpoint - Invalid Bearer token length"),
        pytest.param("Dummy token", id="BUSINESS GET Endpoint - Dummy Bearer token")
    ]
)
async def test_get_business_me_oauth_token_issue(
        client: AsyncClient,
        db_test_create: None,
        token: str,
        mocker: MockerFixture,
) -> None:
    """
    Test the `get` endpoint for the currently authenticated business of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param token: Dummy bearer token.
    :param mocker: Mock fixture to be used for mocking desired functionality.

    :return:
    """
    """
    Mock the password check for failing basic auth
    """
    mocker.patch("bcrypt.checkpw", return_value=False)

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/business/me", headers={"Authorization": token})

    """
    Test the response
    """
    assert response.status_code == 401
    assert response.json()["detail"] == "Not Authenticated"

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="CUSTOMER GET Endpoint - Fail to get user info from oauth provider")
    ]
)
async def test_get_business_me_oauth_fail(
        client: AsyncClient,
        db_test_create: None,
        mocker: MockerFixture,
        _,
) -> None:
    """
    Test the `get` endpoint for the currently authenticated business of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param mocker: Mock fixture to be used for mocking desired functionality.

    :return:
    """
    """
    Mock the password check for failing basic auth
    """
    mocker.patch("bcrypt.checkpw", return_value=False)

    """
    Mock `userinfo` to induce side effect while fetching oauth details
    """
    mocker.patch("fastapi_ecom.utils.oauth.oauth.google.userinfo", side_effect=Exception)

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/business/me", headers={"Authorization": "Bearer dummy-token"})

    """
    Test the response
    """
    assert response.status_code == 401
    assert response.json()["detail"] == "Not Authenticated"

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="BUSINESS GET Endpoint - Fetch all the businesses")
    ]
)
async def test_get_businesses(
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        _: None
) -> None:
    """
    Test the `get` endpoint for fetching all the businesses of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
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
async def test_get_businesses_fail(
    client: AsyncClient,
    db_test_create: None,
    _: None,
) -> None:
    """
    Test the `get` endpoint for fetching no records from database of the Business API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.

    :return:
    """

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/business/search")

    assert response.status_code == 404
    assert response.json()["detail"] == "No business present in database"
