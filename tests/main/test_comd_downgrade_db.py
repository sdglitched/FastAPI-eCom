import pytest
from alembic import command, config
from click.testing import CliRunner
from sqlalchemy import URL

from fastapi_ecom.main import main
from tests import _alempath


@pytest.mark.parametrize(
    "cmd, revision, code",
    [
        pytest.param("downgrade-db", "base", 0, id="MAIN Function - DOWNGRADE-DB - Downgrade the database to the base revision"),
        pytest.param("downgrade-db", "306d801996a6", 0, id="MAIN Function - DOWNGRADE-DB - Downgrade the database to the same revision")
    ]
)
def test_comd_downgrade_db(runner: CliRunner, cmd: str, revision: str, code: int, get_test_database_url: URL) -> None:
    """
    Test the functionality cli `downgrade-db` command.

    :param runner: Fixture to invoke CLI commands programmatically.
    :param cmd: The command to test.
    :param revision: The target database version to downgrade to.
    :param code: Expected exit code.
    :param get_test_database_url: The fixture which generates test database URL.

    :return:
    """
    """
    Perform the action to setup the `alembic_version` table
    """
    # Set up Alembic configuration for migration management.
    alembic_config = config.Config(_alempath()[1])
    alembic_config.set_main_option("script_location", _alempath()[0])
    alembic_config.set_main_option("sqlalchemy.url", get_test_database_url.render_as_string())

    # Mark the database at the first migration as sqlite database does not support `ALTER COLUMN`.
    command.stamp(alembic_config, "306d801996a6")

    """
    Perform the action of invoking CLI command
    """
    result = runner.invoke(main, [cmd, revision])

    """
    Test the response of the CLI
    """
    assert result.exit_code == code
    if revision == "base":
        assert "base" in result.output
    else:
        assert "There is nothing to downgrade." in result.output
