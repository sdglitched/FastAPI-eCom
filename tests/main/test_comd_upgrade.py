
import pytest
from alembic import command, config
from click.testing import CliRunner
from sqlalchemy import URL

from fastapi_ecom.main import main
from tests import _alempath


@pytest.mark.parametrize(
    "cmd, revision, code",
    [
        pytest.param("upgrade-db", "306d801996a6", 0, id="MAIN Function - UPGRADE-DB - Upgrade the database to the certain revision")
    ]
)
def test_comd_upgrade_db(
        runner: CliRunner,
        db_test_create: None,
        get_test_database_url: URL,
        cmd: str,
        revision: str,
        code: int
) -> None:
    """
    Test the functionality cli `upgrade-db` command.

    :param runner: Fixture to invoke CLI commands programmatically.
    :param db_test_create: Fixture which creates a test database.
    :param get_test_database_url: The fixture which generates test database URL.
    :param cmd: The command to test.
    :param revision: The target database version to upgrade to.
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

    # Mark the database at the one of the revisions.
    command.stamp(alembic_config, "head")

    """
    Perform the action of invoking CLI command
    """
    result = runner.invoke(main, [cmd, revision])

    """
    Test the response of the CLI
    """
    assert result.exit_code == code
    assert "There is nothing to upgrade." in result.output
