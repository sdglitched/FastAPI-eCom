from collections.abc import AsyncGenerator

from alembic import command, config
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ecom.database import (  # noqa: F401
    alempath,
    baseobjc,
    get_async_session,
    get_database_url,
    get_engine,
    migrpath,
    models,
)
from fastapi_ecom.utils.logging_setup import general, success


def make_database() -> None:
    """
    Initializes the database and creates all the models.

    This function performs the following:
    - Creates all tables defined in the `baseobjc` ORM models.
    - Configures Alembic with the database connection URL.
    - Marks the database as being at the latest migration version.
    """
    # Use the synchronous engine to create the database schema.
    general("Creating database schema with synchronous engine")
    sync_engine = get_engine(engine="sync")
    baseobjc.metadata.create_all(bind=sync_engine)
    success("Database schema created successfully")

    # Set up Alembic configuration for migration management.
    general("Setting up Alembic configuration")
    alembic_config = config.Config(alempath)
    alembic_config.set_main_option("script_location", migrpath)
    alembic_config.set_main_option("sqlalchemy.url", get_database_url().render_as_string(hide_password=False))

    # Mark the database at the latest migration head.
    general("Marking database at latest migration head")
    command.stamp(alembic_config, "head")
    success("Database marked at migration head successfully")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
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
    db = get_async_session()()  # Initialize a new database session.
    try:
        yield db
        await db.commit()  # Commit changes to the database if no exception occurs.
    except Exception:
        await db.rollback()  # Roll back changes if an exception occurs.
        raise
    finally:
        await db.close()  # Ensure the session is closed after use.
