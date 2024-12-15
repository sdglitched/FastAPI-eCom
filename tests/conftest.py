from pathlib import PosixPath
from typing import AsyncGenerator, Callable
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner
from fastapi import FastAPI
from fastapi.security import HTTPBasicCredentials
from httpx import ASGITransport, AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy import URL

from fastapi_ecom.app import app
from fastapi_ecom.config import config as cnfg
from fastapi_ecom.database import baseobjc, get_async_session, get_engine
from fastapi_ecom.utils.auth import security
from tests.business import _test_data_business
from tests.customer import _test_data_customer
from tests.order import _test_data_order_details, _test_data_orders
from tests.product import _test_data_product


@pytest.fixture
def runner() -> CliRunner:
    """
    Fixture for Click's CLI Runner.

    :return: Click's CLI Runner.
    """
    return CliRunner()

@pytest.fixture
async def test_app() -> FastAPI:
    """
    Fixture to provide the FastAPI app instance for testing.

    :return: FastAPI app instance.
    """
    return app

@pytest.fixture
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture to provide a test client for the FastAPI app.

    :param test_app: The fixture which provides FastAPI app instance.

    :return: An instance of `AsyncClient` for testing HTTP endpoints.
    """
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
async def get_test_database_url(tmp_path: PosixPath, mocker: MockerFixture) -> URL:
    """
    Fixture to provide the database URL for testing and setting the echo for sqlalchemy.

    :param tmp_path: Inbuilt fixture which provides temporary directory.
    :param mocker: Mock fixture to be used for mocking desired functionality.

    :return: URL string for the SQLite test database.
    """
    SQLALCHEMY_DATABASE_URL = URL.create(
        drivername="sqlite+aiosqlite",
        database=f"{tmp_path.as_posix()}/eCom.db",
    )
    mocker.patch.object(URL, "create", return_value=SQLALCHEMY_DATABASE_URL)
    cnfg.confecho = False
    return SQLALCHEMY_DATABASE_URL

@pytest.fixture(autouse=True)
async def db_test_data(get_test_database_url: MagicMock) -> None:
    """
    Fixture to populate the test database with initial test data.

    :param get_test_database_url: The fixture which generates test database URL.

    :return:
    """
    async_engine = get_engine()

    async with async_engine.begin() as conn:
        await conn.run_sync(baseobjc.metadata.drop_all)  # Ensure no old tables persist
        await conn.run_sync(baseobjc.metadata.create_all)

    db = get_async_session()()
    for data in _test_data_business().values():
        db.add(data)
    for data in _test_data_customer().values():
        db.add(data)
    for data in _test_data_product().values():
        db.add(data)
    for data in _test_data_orders().values():
        db.add(data)
    for data in _test_data_order_details().values():
        db.add(data)

    await db.commit()

@pytest.fixture
async def override_security(mocker: MockerFixture) -> Callable[[], HTTPBasicCredentials]:
    """
    Fixture to override the `security` dependency.

    :param mocker: Mock fixture to be used for mocking desired functionality

    :return: Instance of `HTTPBasicCredentials` with provided security credentials.
    """
    mock_credentials = HTTPBasicCredentials(username="delete@example.com", password="delete")
    mocker.patch("fastapi.security.http.HTTPBasic.__call__", return_value=mock_credentials)
    return lambda: mock_credentials

@pytest.fixture(autouse=True)
async def apply_security_override(test_app, override_security):
    """
    Setup test client with dependency override for `security`.

    :param test_app: The fixture which provides FastAPI app instance.
    :param override_security: The fixture which provides security credentials.

    :return:
    """
    test_app.dependency_overrides[security] = override_security
