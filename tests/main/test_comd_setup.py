from pathlib import PosixPath

import pytest
from click.testing import CliRunner
from sqlalchemy import URL

from fastapi_ecom.database.db_setup import make_database
from fastapi_ecom.main import main


@pytest.mark.parametrize(
    "cmd, code",
    [
        pytest.param("setup", 0, id="MAIN Function - SETUP - Setup the database")
    ]
)
def test_comd_setup(runner: CliRunner, tmp_path: PosixPath, mocker, cmd: str, code: int) -> None:
    """
    Test the functionality cli `setup` command.

    :param runner: Fixture to invoke CLI commands programmatically.
    :param tmp_path: Inbuilt fixture which provides temporary directory.
    :param cmd: The command to test.
    :param code: Expected exit code.

    :return:
    """
    SQLALCHEMY_DATABASE_URL = URL.create(
        drivername="sqlite",
        database=f"{tmp_path.as_posix()}/eCom.db",
    )

    mocker.patch("fastapi_ecom.database.db_setup.get_database_url", return_value=SQLALCHEMY_DATABASE_URL)
    mocker.patch("fastapi_ecom.database.baseobjc.metadata.create_all")  # Mock the unwanted creation of tables in test database

    make_database()

    """
    Perform the action of invoking CLI command
    """
    result = runner.invoke(main, cmd)

    """
    Test the response of the CLI
    """
    assert result.exit_code == code
