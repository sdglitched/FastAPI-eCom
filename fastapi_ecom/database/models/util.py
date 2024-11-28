from datetime import UTC, datetime
from functools import partial
from uuid import uuid4

from sqlalchemy import Column, Text
from sqlalchemy.types import TIMESTAMP


class UUIDCreatableMixin:
    """
    SQLAlchemy mixin to automatically generate a unique 8-character UUID for each record.

    :cvar uuid: An 8-character hexadecimal string serving as a unique identifier for the record.
                This UUID is generated upon creation and remains constant.
    """
    uuid = Column("uuid", Text, unique=True, nullable=False, default=uuid4().hex[0:8])


class DateCreatableMixin:
    """
    SQLAlchemy mixin to automatically set a record's creation date.

    :cvar creation_date: Timestamp marking when the record was created.
                         Automatically set to the current UTC datetime at creation.
    """
    creation_date = Column("creation_date", TIMESTAMP(timezone=True), nullable=False, default=partial(datetime.now, tz=UTC))


class DateUpdateableMixin:
    """
    SQLAlchemy mixin to automatically set or update a record's last modification date.

    :cvar update_date: Timestamp marking the last time the record was updated.
                       Automatically set to the current UTC datetime at creation and should be
                       updated on each modification.
    """
    update_date = Column("update_date", TIMESTAMP(timezone=True), nullable=False, default=partial(datetime.now, tz=UTC))
