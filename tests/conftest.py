from typing import AsyncGenerator, Callable

import pytest
from alembic import command, config
from fastapi import FastAPI
from fastapi.security import HTTPBasicCredentials
from httpx import ASGITransport, AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastapi_ecom.app import app
from fastapi_ecom.database import baseobjc, migrpath
from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.utils.auth import security
from tests import _alempath
from tests.business import _test_data_business


@pytest.fixture
async def test_app() -> FastAPI:
    """
    Fixture to provide the FastAPI app instance for testing.

    :return: FastAPI app instance.
    """
    return app

@pytest.fixture
async def client(test_app) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture to provide a test client for the FastAPI app.

    :param test_app: The FastAPI app instance.

    :return: An instance of `AsyncClient` for testing HTTP endpoints.
    """
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
async def get_test_database_url() -> str:
    """
    Fixture to provide the database URL for testing.

    :return: URL string for the in-memory SQLite test database.
    """
    TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    return TEST_DATABASE_URL

@pytest.fixture
async def get_test_engine(get_test_database_url: str) -> AsyncEngine:
    """
    Fixture to create an asynchronous SQLAlchemy engine for testing.

    :param get_test_database_url: URL string for the test database.

    :return: An instance of `AsyncEngine` bound to the test database.
    """
    return create_async_engine(url=get_test_database_url, echo=False)

@pytest.fixture
async def get_test_session(get_test_engine: AsyncEngine) -> async_sessionmaker:
    """
    Fixture to create an asynchronous session factory for testing.

    :param get_test_engine: The SQLAlchemy engine for the test database.

    :return: A session factory for creating asynchronous database sessions.
    """
    return async_sessionmaker(bind=get_test_engine, expire_on_commit=False)

@pytest.fixture
async def make_test_database(get_test_engine: AsyncEngine, get_test_database_url: str):
    """
    Fixture to initialize the test database and apply migrations.

    :param get_test_engine: The SQLAlchemy engine for the test database.
    :param get_test_database_url: URL string for the test database.

    :return:
    """
    async with get_test_engine.begin() as conn:
        await conn.run_sync(baseobjc.metadata.create_all)

    # Set up Alembic configuration for migration management.
    alembic_config = config.Config(_alempath())
    alembic_config.set_main_option("script_location", migrpath)
    alembic_config.set_main_option("sqlalchemy.url", get_test_database_url)

    # Mark the database at the latest migration head.
    command.stamp(alembic_config, "head")

@pytest.fixture
async def db_test_data(get_test_session: async_sessionmaker):
    """
    Fixture to populate the test database with initial test data.

    :param get_test_session: A session factory for creating asynchronous database sessions.

    :return:
    """
    db = get_test_session()
    for data in _test_data_business().values():
        db.add(data)
        await db.commit()

@pytest.fixture
async def override_get_db(make_test_database, db_test_data, get_test_session: async_sessionmaker) -> Callable[[], AsyncGenerator[AsyncSession, None]]:
    """
    Fixture to override the `get_db` dependency for tests to use the test database.

    :param make_test_database: Ensures the test database is initialized.
    :param db_test_data: Populates the test database with data.
    :param get_test_session: A session factory for creating database sessions.

    :return: A callable that yields an asynchronous database session.
    """
    async def _get_db() -> AsyncGenerator[AsyncSession, None]:
        db = get_test_session()
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()
    return _get_db

@pytest.fixture(autouse=True)
async def apply_db_override(test_app, override_get_db):
    """
    Automatically applies the `override_get_db` fixture for all tests.

    :param test_app: The FastAPI app instance.
    :param override_get_db: The overridden `get_db` dependency.

    :return:
    """
    test_app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def override_security(mocker: MockerFixture):
    """
    Fixture to override the `security` dependency.
    """
    mock_credentials = HTTPBasicCredentials(username="delete@example.com", password="delete")
    mocker.patch("fastapi.security.http.HTTPBasic.__call__", return_value=mock_credentials)
    return lambda: mock_credentials

@pytest.fixture(autouse=True)
async def apply_security_override(test_app, override_security):
    """
    Setup test client with dependency override for `security`.
    """
    test_app.dependency_overrides[security] = override_security
