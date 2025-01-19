from typing import AsyncGenerator

import pytest
from alembic import command, config
from click.testing import CliRunner
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ecom.main import main
from tests import _alempath


@pytest.mark.parametrize(
    "cmd, code",
    [
        pytest.param("db-version", 0, id="MAIN Function - DB-VERSION - Check the current revision of the database schema")
    ]
)
def test_comd_db_version(
        runner: CliRunner,
        db_test_data: AsyncGenerator[AsyncSession, None],
        get_test_database_url: URL,
        cmd: str,
        code: int
) -> None:
    """
    Test the functionality cli `db-version` command.

    :param runner: Fixture to invoke CLI commands programmatically.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param get_test_database_url: The fixture which generates test database URL.
    :param cmd: The command to test.
    :param code: Expected exit code.

    :return:
    """
    """
    Perform the action to setup the `alembic_version` table
    """
    # Set up Alembic configuration for migration management.
    alembic_config = config.Config(_alempath()[1])
    alembic_config.set_main_option("script_location", _alempath()[0])
    alembic_config.set_main_option("sqlalchemy.url", get_test_database_url.render_as_string())

    # Mark the database at the latest migration head.
    command.stamp(alembic_config, "head")

    """
    Perform the action of invoking CLI command
    """
    result = runner.invoke(main, cmd)

    """
    Test the response of the CLI
    """
    assert result.exit_code == code
    assert "head" in result.output
