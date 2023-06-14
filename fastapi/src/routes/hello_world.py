from os import environ

from jose import jwt

from fastapi import APIRouter, Depends, status
from src.core.auth import OAUTH2_SCHEME
from src.helpers.container import CONTAINER
from src.models.commons import BaseMessage
from src.services.logger.interfaces.i_logger import ILogger

router = APIRouter()


@router.get("/", response_model=BaseMessage, status_code=status.HTTP_200_OK)
async def root():
    # pylint: disable=missing-function-docstring
    log = CONTAINER.get(ILogger)
    log.info("some", "Hello world")
    return BaseMessage(message="Hello, world! (Simple message type)")


@router.get("/test-auth")
async def test_auth(token: str = Depends(OAUTH2_SCHEME)):
    # pylint: disable=missing-function-docstring
    return jwt.decode(token, environ["SECRET_KEY"], algorithms="HS256")
