
import pytest
from fastapi import FastAPI
from fastapi.security import HTTPBasicCredentials
from httpx import AsyncClient
from pytest_mock import MockerFixture

from fastapi_ecom.utils.auth import security
from tests.product import _test_data_product


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="PRODUCT GET Endpoint - Fetch all the products")
    ]
)
async def test_get_products(
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        _: None
) -> None:
    """
    Test the `get` endpoint for fetching all the products of the Product API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.

    :return:
    """
    """
    Get the data for assertion
    """
    data = _test_data_product()
    products = [
        {
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "mfg_date": product.mfg_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
            "exp_date": product.exp_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
            "price": product.price,
        } for product in data.values()
    ]

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/product/search")

    """
    Test the response
    """
    assert response.status_code == 200
    assert response.json() == {
        "action": "get",
        "products": products
    }

@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="CUSTOMER GET Endpoint - Fail to fetch product")
    ]
)
async def test_get_products_fail(
    client: AsyncClient,
    db_test_create: None,
    _: None,
) -> None:
    """
    Test the `get` endpoint for fetching no records from database of the Customer API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.

    :return:
    """

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/product/search")

    assert response.status_code == 404
    assert response.json()["detail"] == "No product present in database"

@pytest.mark.parametrize(
    "text, present",
    [
        pytest.param("Second", True, id="PRODUCT GET Endpoint - Fetch single matching product"),
        pytest.param("Product", True, id="PRODUCT GET Endpoint - Fetch all the matching products"),
        pytest.param("xxxxyyyy", False, id="PRODUCT GET Endpoint - Fail to fetch any matching products"),
    ]
)
async def test_get_product_by_text(
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        text: str,
        present: bool
) -> None:
    """
    Test the `get` endpoint for fetching a single or all the matching products of the Product API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param text: The search string used to match product name or description of products.
    :param present: Whether the product associated with the business exists.

    :return:
    """
    """
    Get the data for assertion
    """
    data = _test_data_product()
    products = [
        {
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "mfg_date": product.mfg_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
            "exp_date": product.exp_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
            "price": product.price,
        } for product in data.values()
        if (text.lower() in product.name.lower()) or (text.lower() in product.description.lower())
    ]

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get(f"/api/v1/product/search/name/{text}")

    """
    Test the response
    """
    if present:
        assert response.status_code == 200
        assert response.json() == {
            "action": "get",
            "products": products
        }
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "No such product present in database"

@pytest.mark.parametrize(
    "business_id, present",
    [
        pytest.param("d76a11f2", True, id="PRODUCT GET Endpoint - Fetch all the products associated with the authenticated business"),
        pytest.param("fd4a8cac", False, id="PRODUCT GET Endpoint - Fetch all the products associated with the authenticated business")
    ]
)
async def test_get_products_internal(
        test_app: FastAPI,
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        apply_security_override: None,
        mocker: MockerFixture,
        business_id: str,
        present: bool
) -> None:
    """
    Test the `get` endpoint for fetching all the products associated with the authenticated
    business of the Product API.

    :param test_app: The fixture which returns the FastAPI app instance.
    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param mocker: The mocker fixture of pytest-mock.
    :param business_id: UUID of business to fetch product from.
    :param present: Whether the product associated with the business exists.

    :return:
    """
    """
    Get the data for assertion
    """
    data = _test_data_product()
    products = [
        {
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "mfg_date": product.mfg_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
            "exp_date": product.exp_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
            "price": product.price,
            "uuid": product.uuid,
            "business_id": product.business_id
        } for product in data.values()
        if product.business_id == business_id  #uuid of the authenticated business
    ]

    """
    Mock `HTTPBasic.__call__` and override the `security` dependency
    """
    if present:
        mock_credentials = HTTPBasicCredentials(username="test_business@example.com", password="test_business")
    else:
        mock_credentials = HTTPBasicCredentials(username="duplicate_business@example.com", password="duplicate_business")

    mocker.patch("fastapi.security.http.HTTPBasic.__call__", return_value=mock_credentials)
    test_app.dependency_overrides[security] = lambda: mock_credentials

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get("/api/v1/product/search/internal")

    """
    Test the response
    """
    if present:
        assert response.status_code == 200
        assert response.json() == {
            "action": "get",
            "products": products
        }
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "No product present in database"

@pytest.mark.parametrize(
    "business_id, product_id, present",
    [
        pytest.param(
            "d76a11f2", "3250fcbe", True,
            id="PRODUCT GET Endpoint - Fetch specific product by its UUID which is associated with the authenticated business"
        ),
        pytest.param(
            "d76a11f2", "xxxxyyyy", False,
            id="PRODUCT GET Endpoint - Fail to fetch specific product by its UUID which is associated with the authenticated business"
        )
    ]
)
async def test_get_product_by_uuid(
        test_app: FastAPI,
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        apply_security_override: None,
        mocker: MockerFixture,
        business_id: str,
        product_id: str,
        present: bool
) -> None:
    """
    Test the `get` endpoint for fetching the specific product associated with the authenticated
    business of the Product API.

    :param test_app: The fixture which returns the FastAPI app instance.
    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param mocker: The mocker fixture of pytest-mock.
    :param business_id: UUID of business to fetch product from.
    :param product_id: UUID of the product associated with the business.
    :param present: Whether the product associated with the business exists.

    :return:
    """
    """
    Get the data for assertion
    """
    data = _test_data_product()
    for prod in data.values():
        if prod.business_id == business_id and prod.uuid == product_id:  #uuid of authenticated business; uuid of one of their products
            product = {
                "name": prod.name,
                "description": prod.description,
                "category": prod.category,
                "mfg_date": prod.mfg_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "exp_date": prod.exp_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "price": prod.price,
                "uuid": prod.uuid,
                "business_id": prod.business_id
            }

    """
    Mock `HTTPBasic.__call__` and override the `security` dependency
    """
    mock_credentials = HTTPBasicCredentials(username="test_business@example.com", password="test_business")
    mocker.patch("fastapi.security.http.HTTPBasic.__call__", return_value=mock_credentials)
    test_app.dependency_overrides[security] = lambda: mock_credentials

    """
    Perform the action of visiting the endpoint
    """
    response = await client.get(f"/api/v1/product/search/uuid/{product_id}")

    """
    Test the response
    """
    if present:
        assert response.status_code == 200
        assert response.json() == {
            "action": "get",
            "product": product
        }
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not present in database"
