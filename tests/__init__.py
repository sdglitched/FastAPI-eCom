from pathlib import Path


def _alempath() -> Path:
    """
    Set path vairable for "alembic.ini" file

    :return: Path for alembic.ini
    """
    # Define the base path as the parent of the current file's directory
    base_path = Path(__file__).resolve().parent.parent

    # Navigate to the "fastapi_ecom/migrations" directory
    migr_path = base_path / "fastapi_ecom" / "migrations"

    # Get the full path to "alembic.ini"
    alem_path = migr_path / "alembic.ini"

    # Resolve the final path
    return alem_path.resolve()
