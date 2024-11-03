from uuid import uuid4
from datetime import datetime, UTC
from functools import partial

from sqlalchemy import Column, Text
from sqlalchemy.types import TIMESTAMP


class UUIDCreatableMixin:
    """
    An SQLAlchemy mixin to automatically generate a custom 8-digit UUID string
    """

    uuid = Column("uuid", Text, unique=True, nullable=False, default=uuid4().hex[0:8])


class DateCreatableMixin:
    """
    An SQLAlchemy mixin to automatically generate a creation date
    """

    creation_date = Column("creation_date", TIMESTAMP(timezone=True), nullable=False, default=partial(datetime.now, tz=UTC))


class DateUpdateableMixin:
    """
    An SQLAlchemy mixin to automatically generate an update date
    """

    update_date = Column("update_date", TIMESTAMP(timezone=True), nullable=False, default=partial(datetime.now, tz=UTC))
