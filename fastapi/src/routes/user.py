from datetime import datetime
from typing import List, Tuple

from beanie.odm.enums import SortDirection
from beanie.operators import All
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.core.auth import hash_password, is_admin, is_authorized, require_admin
from src.db.collections.user import User as UserCollection
from src.helpers.container import CONTAINER
from src.models.commons import BaseMessage, HttpExceptionMessage
from src.models.user import (
    CurrentUserDetails,
    Role,
    UpdateUserDetails,
    UserPartialDetails,
    UserPartialDetailsAdmin,
    UserRegistration,
    UserRegistrationAdmin,
)
from src.services.logger.interfaces.i_logger import ILogger

# Router instantiation.
router = APIRouter()


@router.post(
    "/register",
    response_model=BaseMessage,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": HttpExceptionMessage,
            "description": "Unsuccesful registration, the user already exists",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while registering the user",
        },
    },
    description=(
        "User registration for basic user, this will set the default user role to 'user', "
        "to let the use chose the roles use the /register-admin endpoint"
    ),
)
async def register(user_registration: UserRegistration):
    # pylint: disable=missing-function-docstring
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: BaseModel
    now_date = datetime.utcnow()

    # Document creation.
    logger.info(
        "routes",
        f"Document creation for user having {user_registration.username} as username.",
    )
    user = UserCollection(
        email=user_registration.email,
        username=user_registration.username,
        password=hash_password(user_registration.password),
        roles=[Role.USER.value],
        creation=now_date,
        last_update=now_date,
    )

    # Saving the document to db.
    try:
        await user.insert()
    except DuplicateKeyError as e:
        logger.error("routes", str(e))
        duplicates = dict(e.details).get("keyPattern")
        msg = f"The following fields must be unique: {duplicates}"
        raise HTTPException(status.HTTP_409_CONFLICT, detail=msg) from e
    except Exception as e:
        logger.error("routes", str(e))
        print(e)
        msg = "An unknown exception occured, maybe bad db connection"
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg) from e

    response = BaseMessage(message="OK")
    status_code = status.HTTP_201_CREATED

    logger.info(
        "routes",
        f"The user having username {user_registration.username} has been added to the db.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


@router.post(
    "/register-roles",
    response_model=BaseMessage,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HttpExceptionMessage,
            # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
            "description": f"Forbidden access, {Role.ADMIN} role required",
        },
        status.HTTP_409_CONFLICT: {
            "model": HttpExceptionMessage,
            "description": "Unsuccesful registration, the user already exists",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while registering the user",
        },
    },
    description=(
        "User registration for admin, this will let the user chose the roles, "
        "at least one role is required.This endpoint execution is "
        "limited to users having the admin role. "
        "This endpoint execution is limited to users having the admin role."
    ),
    dependencies=[Depends(require_admin)],
)
async def register_admin(
    user_registration: UserRegistrationAdmin,
    is_admin_result: Tuple[bool, bool, dict] = Depends(is_admin),
):
    # pylint: disable=missing-function-docstring
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: BaseModel
    now_date = datetime.utcnow()

    # Check if user access token is valid.
    if not is_admin_result[0]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # Check if user has admin role.
    if not is_admin_result[1]:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    # Document creation.
    logger.info(
        "routes",
        f"Document creation for user having {user_registration.username}"
        f" as username and roles {user_registration.roles}.",
    )
    user = UserCollection(
        email=user_registration.email,
        username=user_registration.username,
        password=hash_password(user_registration.password),
        roles=user_registration.roles,
        creation=now_date,
        last_update=now_date,
    )

    # Saving the document to db.
    try:
        await user.insert()
    except DuplicateKeyError as e:
        logger.error("routes", str(e))
        duplicates = dict(e.details).get("keyPattern")
        msg = f"The following fields must be unique: {duplicates}"
        raise HTTPException(status.HTTP_409_CONFLICT, detail=msg) from e
    except Exception as e:
        logger.error("routes", str(e))
        msg = "An unknown exception occured, maybe bad db connection"
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg) from e

    response = BaseMessage(message="OK")
    status_code = status.HTTP_201_CREATED

    logger.info(
        "routes",
        f"The user having username {user_registration.username}"
        f" and roles {user_registration.roles} has been succesully added to the db.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


@router.get(
    "/all",
    response_model=List[UserPartialDetails | UserPartialDetailsAdmin],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HttpExceptionMessage,
            # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
            "description": f"Forbidden access, {Role.ADMIN} role required",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while registering the user",
        },
    },
    description=(
        "Get all users with parial details from the db. "
        "If needed is possible to limit returned entities and skip the required amount"
    ),
    dependencies=[Depends(is_admin)],
)
async def get_all_users(
    limit: int | None = None,
    skip: int | None = None,
    is_admin_result: Tuple[bool, bool, dict] = Depends(is_admin),
):
    # pylint: disable=missing-function-docstring
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: BaseModel
    projection: BaseModel

    # Check if user is authorized to access the endpoint.
    if not is_admin_result[0]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # Check if the user has admin role or not.
    if not is_admin_result[1]:
        projection = UserPartialDetails
    else:
        projection = UserPartialDetailsAdmin

    logger.info(
        "routes",
        f"Returning the users in the db: limit={limit} and skip={skip}.",
    )

    try:
        response = await UserCollection.find_all(
            projection_model=projection,
            limit=limit,
            skip=skip,
            sort=[("username", SortDirection.ASCENDING)],
        ).to_list()
    except Exception as e:
        logger.error(
            "routes", f"An unknown exception occured while fetcthing the users: {e}"
        )
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) from e

    status_code = status.HTTP_200_OK

    logger.info(
        "routes",
        "Success returning all the users.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


@router.get(
    "/count",
    response_model=int,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HttpExceptionMessage,
            # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
            "description": f"Forbidden access, {Role.ADMIN} role required",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while registering the user",
        },
    },
    description=("Get the total number of users in the database"),
    dependencies=[Depends(is_authorized)],
)
async def get_users_count(
    is_authorized_result: Tuple[bool, dict] = Depends(is_authorized)
):
    # pylint: disable=missing-function-docstring
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: int

    # Check if teh user is authorized or not.
    if not is_authorized_result[0]:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="The provided token may be expired or invalid.",
        )

    logger.info(
        "routes",
        "Returning the total number of users document in the db.",
    )

    try:
        response = await UserCollection.find_all().count()
    except Exception as e:
        logger.error(
            "routes",
            "An unknown exception occured while fetcthing the total number of users documents: {e}",
        )
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) from e

    status_code = status.HTTP_200_OK

    logger.info(
        "routes",
        "Success returning the total number of users documents in the db.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


@router.get(
    "/username/{username}",
    response_model=List[UserPartialDetails | UserPartialDetailsAdmin],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
            "description": "Unauthorized",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while retriving the user",
        },
    },
    description=(
        "Get user parial details from the db given the username."
        " To get full details run admin endpoint."
    ),
    dependencies=[Depends(is_admin)],
)
async def get_user_by_username(
    username: str, is_admin_result: Tuple[bool, bool, dict] = Depends(is_admin)
):
    # pylint: disable=missing-function-docstring
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: BaseModel
    projection: BaseModel

    # Check if user access token was valid and user authorized.
    if not is_admin_result[0]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # Check if user has admin role or not.
    if not is_admin_result[1]:
        projection = UserPartialDetails
    else:
        projection = UserPartialDetailsAdmin

    logger.info(
        "routes",
        f"Returning the in the db: username={username}.",
    )

    try:
        response = await UserCollection.find_one(
            UserCollection.username == username,
            projection_model=projection,
        )
    except Exception as e:
        logger.error(
            "routes", f"An unknown exception occured while fetcthing the user: {e}"
        )
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) from e

    status_code = status.HTTP_200_OK

    logger.info(
        "routes",
        "Success returning the serched user.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


@router.get(
    "/me",
    response_model=CurrentUserDetails,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "Unauthorized",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while retriving the user",
        },
    },
    description="Get current user complete details.",
    dependencies=[Depends(is_authorized)],
)
async def get_current_user(
    is_authorized_result: Tuple[bool, dict] = Depends(is_authorized),
):
    # pylint: disable=missing-function-docstring

    # Check if the user is authorized or not.
    if not is_authorized_result[0]:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="The provided token may be expired or invalid.",
        )

    # Decoded token is in is_authorized_result[1]
    status_code = status.HTTP_200_OK
    response = await UserCollection.find_one(
        UserCollection.username == is_authorized_result[1]["username"]
    ).project(CurrentUserDetails)

    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


@router.put(
    "/username/{username}",
    response_model=int,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HttpExceptionMessage,
            "description": "Only users with admin role can update other users.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": HttpExceptionMessage,
            "description": "The user to update was not found",
        },
        status.HTTP_409_CONFLICT: {
            "model": HttpExceptionMessage,
            "description": "The username or email are already in use by another user.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while retriving the user",
        },
    },
    description=(
        "Update user given the username in path and user with updated fields in body."
    ),
    dependencies=[Depends(is_admin)],
)
async def put_user_by_username(
    username: str,
    updated_user: UpdateUserDetails,
    is_admin_result: Tuple[bool, bool, dict] = Depends(is_admin),
):
    # pylint: disable=missing-function-docstring

    logger = CONTAINER.get(ILogger)

    # Check if user is authorized.
    if not is_admin_result[0]:
        logger.info("routes", "The user is not authenticated.")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # Check if user is not admin that the user in the decoded token
    # is equal to the given one in the endpoint path.
    if not is_admin_result[1] and username != is_admin_result[2]["username"]:
        logger.info("routes", "The user has not right to update a different user.")
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    to_update = await UserCollection.find_one(UserCollection.username == username)

    if to_update is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    to_update.email = updated_user.email
    to_update.username = updated_user.username
    to_update.roles = updated_user.roles
    to_update.last_update = datetime.utcnow()

    try:
        await to_update.save()
    except DuplicateKeyError as e:
        logger.error("routes", str(e))
        duplicates = dict(e.details).get("keyPattern")
        msg = f"The following fields must be unique: {duplicates}"
        raise HTTPException(status.HTTP_409_CONFLICT, detail=msg) from e
    except Exception as e:
        logger.error("routes", str(e))
        msg = "An unknown exception occured, maybe bad db connection"
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg) from e

    logger.info("routes", f"Succesful update for {username} to {updated_user.json()}")

    return JSONResponse(status.HTTP_200_OK)


@router.delete(
    "/username/{username}",
    response_model=int,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HttpExceptionMessage,
            "description": "Only users with admin role can update other users.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": HttpExceptionMessage,
            "description": "The user to update was not found",
        },
        status.HTTP_406_NOT_ACCEPTABLE: {
            "model": HttpExceptionMessage,
            "description": "You are trying to delete the last admin, not acceptable.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while retriving the user",
        },
    },
    description=(
        "Update user given the username in path and user with updated fields in body."
    ),
    dependencies=[Depends(is_admin)],
)
async def delete_user_by_username(
    username: str,
    is_admin_result: Tuple[bool, bool, dict] = Depends(is_admin),
):
    # pylint: disable=missing-function-docstring

    logger = CONTAINER.get(ILogger)

    # Check if user is authorized.
    if not is_admin_result[0]:
        logger.info("routes", "The user is not authenticated.")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # Check if user is not admin that the user in the decoded token
    # is equal to the given one in the endpoint path.
    if not is_admin_result[1] and username != is_admin_result[2]["username"]:
        logger.info("routes", "The user has not right to update a different user.")
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    to_delete = await UserCollection.find_one(UserCollection.username == username)

    if to_delete is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    # If the user to delete is admin and the last one return 406.
    if Role.ADMIN in to_delete.roles:
        admin_count = await UserCollection.find_many(
            All(UserCollection.roles, [Role.ADMIN.value])
        ).count()
        if admin_count == 1:
            raise HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE,
                detail="Trying to delete the last admin user, impossible.",
            )

    try:
        await to_delete.delete()
    except Exception as e:
        logger.error("routes", str(e))
        msg = "An unknown exception occured, maybe bad db connection"
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg) from e

    logger.info("routes", f"Succesful deletion for {username}")

    return JSONResponse(status.HTTP_200_OK)
