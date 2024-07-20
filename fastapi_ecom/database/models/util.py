from sqlalchemy import Column, Text

from uuid import uuid4


class UUIDCreatableMixin:
    """
    An SQLAlchemy mixin to automatically generate a custom 8-digit UUID string
    """

    uuid = Column("uuid", Text, unique=True, nullable=False, default=uuid4().hex[0:8])

    