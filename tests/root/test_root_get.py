import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="ROOT GET Endpoint - Fetch the root endpoint of this application")
    ]
)
async def test_root(
    client: AsyncClient,
    _: None
) -> None:
    """
    Test the root ('/') endpoint.

    :param client: The test client to send HTTP requests.

    :return:
    """
    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/")

    """
    Test the response
    """
    assert response.status_code == 200
    assert response.json() == {
        "title": "FastAPI ECOM",
        "description": "E-Commerce API for businesses and end users using FastAPI.",
        "version": "0.1.0"
    }
