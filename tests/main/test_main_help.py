import pytest
from click.testing import CliRunner

from fastapi_ecom.main import main


@pytest.mark.parametrize(
    "cmd, code, output",
    [
        pytest.param(
            "--help",
            0,
            [
                "Usage: fastapi_ecom [OPTIONS] COMMAND [ARGS]...",
                "E-Commerce API for businesses and end users using FastAPI.",
                "Options:",
                "--help  Show this message and exit.",
                "Commands:",
                "create-migration  Create a new migration script",
                "db-version        Show the current database version",
                "downgrade-db      Downgrade the database to a specific version",
                "setup             Setup the database schema",
                "start             Start the FastAPI eComm application",
                "upgrade-db        Upgrade the database to a specific version",
            ],
            id="MAIN Function - Basic Help",
        ),
        pytest.param(
            "start --help",
            0,
            ["Usage: fastapi_ecom start [OPTIONS]", "Start the FastAPI eComm application", "Options:", "--help  Show this message and exit."],
            id="MAIN Function - START - Basic Help",
        ),
        pytest.param(
            "setup --help",
            0,
            ["Usage: fastapi_ecom setup [OPTIONS]", "Setup the database schema", "Options:", "--help  Show this message and exit."],
            id="MAIN Function - SETUP - Basic Help",
        ),
        pytest.param(
            "create-migration --help",
            0,
            [
                "Usage: fastapi_ecom create-migration [OPTIONS] COMMENT",
                "Create a new migration script",
                "Options:",
                "--autogenerate  Automatically generate the migration",
                "--help          Show this message and exit.",
            ],
            id="MAIN Function - CREATE-MIGRATION - Basic Help",
        ),
        pytest.param(
            "db-version --help",
            0,
            ["Usage: fastapi_ecom db-version [OPTIONS]", "Show the current database version", "Options:", "--help  Show this message and exit."],
            id="MAIN Function - DB-VERSION - Basic Help",
        ),
        pytest.param(
            "upgrade-db --help",
            0,
            [
                "Usage: fastapi_ecom upgrade-db [OPTIONS] [VERSION]",
                "Upgrade the database to a specific version",
                "Options:",
                "--help  Show this message and exit.",
            ],
            id="MAIN Function - UPGRADE-DB - Basic Help",
        ),
        pytest.param(
            "downgrade-db --help",
            0,
            [
                "Usage: fastapi_ecom downgrade-db [OPTIONS] VERSION",
                "Downgrade the database to a specific version",
                "Options:",
                "--help  Show this message and exit.",
            ],
            id="MAIN Function - DOWNGRAD-DB - Basic Help",
        ),
    ],
)
def test_main_help(runner: CliRunner, cmd: str, code: int, output: list[str]) -> None:
    """
    Test the basic cli help functionality.

    :param runner: Fixture to invoke CLI commands programmatically.
    :param cmd: The command to test.
    :param code: Expected exit code.
    :param output: Expected output.

    :return:
    """
    """
    Perform the action of invoking CLI command
    """
    result = runner.invoke(main, cmd)

    """
    Test the response of the CLI
    """
    assert result.exit_code == code
    for indx in output:
        assert indx in result.output
