from datetime import datetime
from json import JSONDecodeError
from typing import List

import pytest
from httpx import AsyncClient
from pydantic import parse_raw_as
from src.db.collections.user import User
from src.models.user import (
    CurrentUserDetails,
    UserPartialDetails,
    UserPartialDetailsAdmin,
)
from tests import (
    BASE_URL,
    IS_TYPED,
    admin_login,
    build_db_client,
    fastapi_app,
    user_login,
)


@pytest.mark.asyncio
async def test_register():
    """Test user registration"""

    # DB connection.
    await build_db_client()

    # Endpoint test
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register",
            json={
                "username": "new_test_user",
                "email": "new_test_user@email.com",
                "password": "new_test_user",
            },
        )
    assert response.status_code == 201

    # Clearing environement.
    await User.find_one(User.username == "new_test_user").delete()


@pytest.mark.asyncio
async def test_register_duplicate_email():
    """Test user registration with duplicate email"""

    # DB connection.
    await build_db_client()

    # Add values to test the db.
    now_date = datetime.utcnow()
    await User(
        email="new_test_user@email.com",
        username="new_test_user",
        password="new_test_user",
        roles=["user"],
        creation=now_date,
        last_update=now_date,
    ).save()

    # Endpoint test
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register",
            json={
                "username": "different_username",
                "email": "new_test_user@email.com",
                "password": "new_test_user",
            },
        )
    assert response.status_code == 409

    # Clearing environement.
    await User.find_one(User.username == "new_test_user").delete()


@pytest.mark.asyncio
async def test_register_duplicate_username():
    """Test user registration with duplicate username"""

    # DB connection.
    await build_db_client()

    # Add values to test the db.
    now_date = datetime.utcnow()
    await User(
        email="new_test_user@email.com",
        username="new_test_user",
        password="new_test_user",
        roles=["user"],
        creation=now_date,
        last_update=now_date,
    ).save()

    # Endpoint test
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register",
            json={
                "username": "new_test_user",
                "email": "different@email.com",
                "password": "new_test_user",
            },
        )
    assert response.status_code == 409

    # Clearing environement.
    await User.find_one(User.username == "new_test_user").delete()


@pytest.mark.asyncio
async def test_register_admin():
    """Test admin registration"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register-roles",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "new_test_user_admin",
                "email": "new_test_user_admin@email.com",
                "password": "new_test_user_admin",
                "roles": ["admin", "user"],
            },
        )
    assert response.status_code == 201

    # Clearing environement.
    await User.find_one(User.username == "new_test_user_admin").delete()


@pytest.mark.asyncio
async def test_register_admin_wrong_roles():
    """Test admin registration with bad roles"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register-roles",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "missing_role_user",
                "email": "missing_role_user@email.com",
                "password": "missing_role_user",
                "roles": ["admina"],
            },
        )
    assert response.status_code == 422

    # Clearing environement.
    # Not needed because no elements have been added to DB.


@pytest.mark.asyncio
async def test_register_admin_missing_roles():
    """Test admin registration with missing roles"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register-roles",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "missing_role_user",
                "email": "missing_role_user@email.com",
                "password": "missing_role_user",
            },
        )
    assert response.status_code == 422

    # Clearing environement.
    # Not needed because no elements have been added to DB.


@pytest.mark.asyncio
async def test_register_admin_duplicate_email():
    """Test admin registration with duplicate email"""

    # DB connection.
    await build_db_client()

    # Add values to test the db.
    now_date = datetime.utcnow()
    await User(
        email="new_test_user_admin@email.com",
        username="new_test_user_admin",
        password="new_test_user",
        roles=["user"],
        creation=now_date,
        last_update=now_date,
    ).save()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register-roles",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "duplicate_test_user_admin",
                "email": "new_test_user_admin@email.com",
                "password": "new_test_user_admin",
                "roles": ["admin", "user"],
            },
        )
    assert response.status_code == 409

    # Clearing environement.
    await User.find_one(User.username == "new_test_user_admin").delete()


@pytest.mark.asyncio
async def test_register_admin_duplicate_username():
    """Test admin registration with duplicate username"""

    # DB connection.
    await build_db_client()

    # Add values to test the db.
    now_date = datetime.utcnow()
    await User(
        email="new_test_user_admin@email.com",
        username="new_test_user_admin",
        password="new_test_user",
        roles=["user"],
        creation=now_date,
        last_update=now_date,
    ).save()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register-roles",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "new_test_user_admin",
                "email": "duplicate_test_user_admin@email.com",
                "password": "new_test_user_admin",
                "roles": ["admin", "user"],
            },
        )
    assert response.status_code == 409

    # Clearing environement.
    await User.find_one(User.username == "new_test_user_admin").delete()


@pytest.mark.asyncio
async def test_get_all_users():
    """Test get all users db call."""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            "/user/all",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200
    assert IS_TYPED(
        parse_raw_as(List[UserPartialDetails], response.text), List[UserPartialDetails]
    )


@pytest.mark.asyncio
async def test_get_all_user_as_admin():
    """Test get all user from adim user, should expect more details"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            "/user/all",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200
    assert IS_TYPED(
        parse_raw_as(List[UserPartialDetailsAdmin], response.text),
        List[UserPartialDetailsAdmin],
    )


@pytest.mark.asyncio
async def test_get_users_count():
    """Test get user count"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            "/user/count",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_id_username():
    """Test get user by id username"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Username
    username = "admin"

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            f"/user/username/{username}",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200

    found = parse_raw_as(UserPartialDetails, response.text)
    assert found.username == username


@pytest.mark.asyncio
async def test_get_user_by_id_username_as_admin():
    """Test get user by id username as admin"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Username
    username = "admin"

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            f"/user/username/{username}",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200

    found = parse_raw_as(UserPartialDetailsAdmin, response.text)
    assert found.username == username


@pytest.mark.asyncio
async def test_get_current_user():
    """Test get current user"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            f"/user/me",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200

    try:
        found = parse_raw_as(CurrentUserDetails, response.text)
        assert found.username == "user"  # The login has made with admin user.
    except JSONDecodeError:
        raise AssertionError(
            f"Impossible to parse to {CurrentUserDetails.__name__} json: {response.text}."
        )


@pytest.mark.asyncio
async def test_update_user():
    """Test update user"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.put(
            f"/user/username/user",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "user1",
                "email": "user@email.com",
                "roles": ["user"],
            },
        )

    assert response.status_code == 200

    # Check and reset DB content to original state.
    user_check = await User.find_one(User.username == "user1")
    assert user_check.username == "user1"
    user_check.username = "user"
    await user_check.save()


@pytest.mark.asyncio
async def test_update_user_bad_user():
    """Test update user with bad user informations"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.put(
            f"/user/username/admin",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "admin1",
                "email": "admin@email.com",
                "roles": ["admin", "user"],
            },
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_user_bad_roles():
    """Test udpate user with bad roles"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.put(
            f"/user/username/admin",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "user",
                "email": "user@email.com",
                "roles": ["admin", "user"],
            },
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_user_admin():
    """Test udpate user admin"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.put(
            f"/user/username/user",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "user1",
                "email": "user@email.com",
                "roles": ["user"],
            },
        )

    assert response.status_code == 200

    # Check and reset DB content to original state.
    user_check = await User.find_one(User.username == "user1")
    assert user_check.username == "user1"
    user_check.username = "user"
    await user_check.save()


@pytest.mark.asyncio
async def test_update_user_admin_missing():
    """Test update user admin whose user not presetn"""
    # Try to update an user that does not exists.

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.put(
            f"/user/username/missing",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "user1",
                "email": "user@email.com",
                "roles": ["user"],
            },
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user_duplicate_uername_or_email():
    """Test update user duplicate using already existing username or email"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.put(
            f"/user/username/missing",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "admin",
                "email": "user@email.com",
                "roles": ["user"],
            },
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_user():
    """Test user deletion"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Store user to delete to then add it later after test completion.
    temp_user = await User.find_one(User.username == "user")

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.delete(
            f"/user/username/user",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200

    # Check and reset DB content to original state.
    await temp_user.create()


@pytest.mark.asyncio
async def test_delte_user_bad_user():
    """Test bad user deletion"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.delete(
            f"/user/username/admin",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_user_admin():
    """Test delete user admin"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Store user to delete to then add it later after test completion.
    temp_user = await User.find_one(User.username == "user")

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.delete(
            f"/user/username/user",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200

    # Check and reset DB content to original state.
    await temp_user.save()


@pytest.mark.asyncio
async def test_delete_user_admin_missing():
    """Test deleting admin user whose does not exists"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.delete(
            f"/user/username/missing",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_last_admin():
    """Test deleting last admin, should result in failure"""

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.delete(
            f"/user/username/admin",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 406
