import os

import pytest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.main import app

TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/test"

test_async_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

TestAsyncSessionLocal = async_sessionmaker(test_async_engine, expire_on_commit=False)


@pytest.fixture()
async def test_app():
    """
    Fixture to provide the FastAPI app instance for testing.
    """
    return app

@pytest.fixture
async def client(test_app):
    """
    Provide a test client for the FastAPI app.
    """
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="session")
async def setup_test_database():
    """
    Set up the test database with Alembic migrations.
    This fixture runs once per test session.
    """
    # Set the environment variable for Alembic
    os.environ["TEST_DATABASE_URL"] = TEST_DATABASE_URL

    # Configure Alembic to use the test database
    alembic_config = Config(os.path.join(os.getcwd(),"fastapi_ecom/alembic.ini"))
    alembic_config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    alembic_config.set_main_option("script_location", os.path.join(os.getcwd(),"fastapi_ecom/migrations/"))
    
    # Apply migrations
    command.upgrade(alembic_config, "head")

    yield  # Test database setup is complete

    # Teardown: Drop all tables after tests
    command.downgrade(alembic_config, "base")

    # Cleanup connections and dispose of the engine
    await test_async_engine.dispose()

@pytest.fixture(scope="function")
async def override_get_db(setup_test_database):
    """
    Override the `get_db` dependency to use the test database session.
    """
    async def _get_db():
        db = TestAsyncSessionLocal()
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
    Automatically apply the `override_get_db` fixture for all tests.
    """
    test_app.dependency_overrides[get_db] = override_get_db
