from pathlib import Path
from typing import Union

from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from fastapi_ecom.config import config

# Base class for ORM models, to be used with SQLAlchemy's declarative system.
baseobjc = declarative_base()

# Migration path for alembic configuration
migrpath = str(Path(str(Path(__file__).parent.resolve().parent.resolve()),"migrations").resolve())


def get_database_url(engine: str = "async") -> URL:
    """
    Construct the database URL based on the provided engine type.

    :param engine: Specifies the type of database engine ("async" or "sync"). Daults to "async".

    :return: The constructed SQLAlchemy database URL.
    """
    if engine == "sync":
        SQLALCHEMY_DATABASE_URL = URL.create(
            drivername = "postgresql+psycopg2",
            username = config.username,
            password = config.password,
            host = config.dtbsbhost,
            port = config.dtbsbport,
            database = config.database,
        )
        return SQLALCHEMY_DATABASE_URL

    SQLALCHEMY_DATABASE_URL = URL.create(
        drivername = config.dtbsdriver,
        username = config.username,
        password = config.password,
        host = config.dtbsbhost,
        port = config.dtbsbport,
        database = config.database,
    )
    return SQLALCHEMY_DATABASE_URL

def get_engine(engine: str = "async") -> Union[Engine, AsyncEngine]:
    """
    Create a session engine based on the specified engine type.

    :param engine: Specifies the type of database engine ("async" or "sync"). Defaults to "async".

    :return: An SQLAlchemy engine instance, either synchronous or asynchronous.
    """
    if engine == "sync":
        SQLALCHEMY_DATABASE_URL = get_database_url(engine = "sync")
        # `echo=True` enables logging of all SQL statements for debugging purposes.
        sync_engine = create_engine(url=SQLALCHEMY_DATABASE_URL, echo=True)
        return sync_engine

    SQLALCHEMY_DATABASE_URL = get_database_url()
    # `echo=True` enables logging of all SQL statements for debugging purposes.
    async_engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL, echo=True)
    return async_engine

def get_async_session() -> async_sessionmaker:
    """
    Create an asynchronous session factory for handling database sessions.

    This factory binds to the asynchronous engine created using the configuration from
    `get_engine()`.

    :return: An asynchronous session factory.
    """
    async_engine = get_engine()
    async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    return async_session
