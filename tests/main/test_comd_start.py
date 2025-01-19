
import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from fastapi_ecom.config import config
from fastapi_ecom.main import main


@pytest.mark.parametrize(
    "cmd, code",
    [
        pytest.param("start", 0, id="MAIN Function - START - Start FastAPI server")
    ]
)
def test_comd_start(
        runner: CliRunner,
        mocker: MockerFixture,
        cmd: str,
        code: int
) -> None:
    """
    Test the functionality cli `start` command.

    :param runner: Fixture to invoke CLI commands programmatically.
    :param mocker: Mock fixture to be used for mocking desired functionality.
    :param cmd: The command to test.
    :param code: Expected exit code.

    :return:
    """
    """
    Mock `uvicorn.run` to prevent starting the server
    """
    mock_run = mocker.patch("uvicorn.run")

    """
    Perform the action of invoking CLI command
    """
    result = runner.invoke(main, cmd)

    """
    Test the response of the CLI
    """
    assert result.exit_code == code

    # Check that `uvicorn.run` was called with the correct arguments
    mock_run.assert_called_once_with(
        "fastapi_ecom.app:app",
        host=config.servhost,
        port=config.servport,
        reload=config.cgreload
    )
