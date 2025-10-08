from enum import Enum

from pydantic import BaseModel


class APIResultAction(str, Enum):
    """
    Enum for API result actions, representing the HTTP methods supported.

    :cvar get: Represents an HTTP GET action.
    :cvar post: Represents an HTTP POST action.
    :cvar put: Represents an HTTP PUT action.
    :cvar delete: Represents an HTTP DELETE action.
    """

    get = "get"
    post = "post"
    put = "put"
    delete = "delete"


class APIResult(BaseModel):
    """
    Base schema for API result responses.

    :ivar action: The HTTP method associated with the API response, if applicable.
    """

    action: APIResultAction | None
