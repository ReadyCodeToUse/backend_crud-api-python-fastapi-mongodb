from datetime import timedelta
from typing import Final

import pytest
from jose import jwt

from src.core.auth import (
    create_token,
    has_roles,
    hash_password,
    is_admin,
    is_authorized,
    require_admin,
    valid_access_token,
    valid_refresh_token,
    valid_token,
    verify_password,
)
from src.models.user import Role
from tests import admin_login, build_db_client, user_login

PLAIN_PASSWORD: Final[str] = "test-pwd"
USER: Final[dict] = {"username": "mariorossi", "password": "secure-hashed-pwd"}
SECRET_KEY: Final[str] = "secret-key"


def test_hashing():
    """Test passowrd hashing"""
    assert PLAIN_PASSWORD != hash_password(PLAIN_PASSWORD)


def test_verify_password():
    """Test password verification"""
    hashed_password = hash_password(PLAIN_PASSWORD)
    assert verify_password(PLAIN_PASSWORD, hashed_password)


def test_verify_bad_password():
    """Test bad password verification"""
    hashed_password = hash_password(PLAIN_PASSWORD)
    assert not verify_password("bad-pwd", hashed_password)


def test_create_token():
    """Test token creation"""
    exp_delta = timedelta(minutes=5)

    token = create_token(
        data=USER,
        expires_delta=exp_delta,
        secret_key=SECRET_KEY,
        is_refresh=True,
        algorithm="HS256",
    )

    try:
        decoded_token: dict = jwt.decode(token=token, key=SECRET_KEY, algorithms="HS256")
        assert decoded_token == {
            **USER,
            "exp": decoded_token["exp"],
            "is_refresh": True,
        }
    except Exception:
        assert False


def test_valid_token():
    """Test access token validation"""
    test_decoded_token = {
        "email": "",
        "username": "",
        "roles": "",
        "exp": "",
        "is_refresh": True,
    }
    assert valid_token(test_decoded_token)


def test_valid_refresh_token():
    """Test refresh token validation"""
    test_decoded_token = {
        "email": "",
        "username": "",
        "roles": "",
        "exp": "",
        "is_refresh": True,
    }
    assert valid_refresh_token(test_decoded_token)


def test_valid_access_token():
    """Test access token validation"""
    test_decoded_token = {
        "email": "",
        "username": "",
        "roles": "",
        "exp": "",
        "is_refresh": False,
    }
    assert valid_access_token(test_decoded_token)


def test_has_roles():
    """Test good roles"""
    assert has_roles(user_roles=[Role.ADMIN], required_roles=[Role.ADMIN])


def test_has_bad_roles():
    """Test bad roles"""
    assert not has_roles(user_roles=[Role.USER], required_roles=[Role.ADMIN])


@pytest.mark.asyncio
async def test_is_athorized():
    """Test if given a token the user is authorized, should return authorized=True"""
    await build_db_client()
    login_response = await user_login()

    authorized, decoded_token = is_authorized(login_response.access_token)

    assert authorized
    assert not decoded_token["is_refresh"]


@pytest.mark.asyncio
async def test_is_admin():
    """Test if a given user is admin, should return admin=True"""
    await build_db_client()
    login_response = await admin_login()

    authorized, admin, decoded_token = is_admin(login_response.access_token)

    assert authorized
    assert admin
    assert not decoded_token["is_refresh"]


@pytest.mark.asyncio
async def test_require_admin():
    """Test admin required"""
    await build_db_client()
    login_response = await admin_login()

    require_admin(login_response.access_token)

    # The require_admin function does not return anything, but if an exception is raised,
    # test fail, if it complete everything then everything ok whith admin login.
    assert True


@pytest.mark.asyncio
async def test_require_admin_fail():
    """Test admin required fail"""
    await build_db_client()
    login_response = await user_login()

    try:
        require_admin(login_response.access_token)
    except Exception as e:
        # pylint: disable=no-member
        assert e.status_code == 403
    else:
        # The require_admin function does not return anything, but if an exception is NOT raised,
        # with user_login test fail.
        assert False
