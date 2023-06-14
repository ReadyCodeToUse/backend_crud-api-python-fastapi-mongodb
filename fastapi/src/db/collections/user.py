from datetime import datetime
from typing import List

from beanie import Document, Indexed


# Disabling this warning because the inhheritance from Document
# is requierd and the module is built that way.
# pylint: disable=too-many-ancestors
class User(Document):
    email: Indexed(str, unique=True)
    username: Indexed(str, unique=True)
    password: str
    roles: List[str]
    creation: datetime
    last_update: datetime

    class Settings:
        # pylint: disable=fixme
        # TODO: create PyLint beanie plugin to prevent this warning
        # pylint: disable=too-few-public-methods
        name = "users"
