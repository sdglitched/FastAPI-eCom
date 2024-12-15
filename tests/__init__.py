from pathlib import Path
from uuid import uuid4

from fastapi_ecom.database.models.business import Business


def _alempath():
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

def _test_data_business():
    data = set()
    duplicate_business = Business(
        email="duplicate_business@example.com",
        password="duplicate_business",
        name="duplicate_business",
        addr_line_1="abc",
        addr_line_2="xyz",
        city="aaa",
        state="bbb",
        uuid=uuid4().hex[0:8]
    )
    data.add(duplicate_business)

    return data
