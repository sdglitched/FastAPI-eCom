from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from fastapi_ecom import db_creds as dbc

# Construct the database URL using credentials from the `db_creds` module.
# This assumes a PostgreSQL database with the `asyncpg` driver.
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{dbc.user}:{dbc.password}@{dbc.host}:{dbc.port}/{dbc.name}"

# Create an asynchronous SQLAlchemy engine for database communication.
# `echo=True` enables logging of all SQL statements for debugging purposes.
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create an asynchronous session factory for handling database sessions.
# `expire_on_commit=False` ensures that objects remain usable after a session commit.
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

# Base class for ORM models, to be used with SQLAlchemy's declarative system.
Base = declarative_base()

async def get_db():
    """
    Dependency function to provide a database session for FastAPI routes.

    This function -
        - Yields a database session for use within the route ensuring auto resource cleanup along
          with compatibility of FastAPI dependency injection.
        - Commits the session upon successful execution.
        - Rolls back the session if an exception occurs to maintain database integrity.
        - Closes the session after the request is completed, regardless of outcome.

    :yield: An instance of the asynchronous SQLAlchemy session.

    :raises exception: Re-raises any exception encountered during the session lifecycle.
    """
    db = AsyncSessionLocal()  # Initialize a new database session.
    try:
        yield db
        await db.commit()  # Commit changes to the database if no exception occurs.
    except Exception:
        await db.rollback()  # Roll back changes if an exception occurs.
        raise
    finally:
        await db.close()  # Ensure the session is closed after use.
