from typing import Dict

import pytest

from apps.users.logic.commands.register.errors import UserAlreadyExistsError
from apps.users.models import Token, User
from tests.fixtures.users import DEFAULT_USER_PASSWORD
from tests.helpers import auth

EMAIL = "new_user@mail.net"


def test_query(db, ghl_client, ghl_raw):
    """Test register raw query."""
    assert not User.objects.filter(email=EMAIL).exists()

    register_data = _get_register_data()
    register_data["firstName"] = register_data.pop("first_name")
    register_data["lastName"] = register_data.pop("last_name")

    response = ghl_client.execute(
        ghl_raw("register"),
        variable_values={
            "input": register_data,
        },
    )

    assert "errors" not in response

    user = User.objects.get(email=EMAIL)
    token = Token.objects.get(user=user)

    assert response["data"]["register"]["token"]["key"] == token.key
    auth.check_auth(register_data["email"], register_data["password"])

    user = User.objects.filter(email=EMAIL).first()
    assert user
    assert user.last_login


def test_success(db, ghl_mock_info, register_mutation):
    """Test success register."""
    assert not User.objects.filter(email=EMAIL).exists()

    register_data = _get_register_data()
    response = register_mutation(
        root=None,
        info=ghl_mock_info,
        input=register_data,
    )

    assert Token.objects.get(pk=response.token.pk, user__email=EMAIL)
    auth.check_auth(register_data["email"], register_data["password"])


def test_wrong_register(
    user,
    register_mutation,
    ghl_mock_info,
):
    """Test exists user."""
    user.email = EMAIL
    user.save()

    register_data = _get_register_data()
    with pytest.raises(UserAlreadyExistsError):
        register_mutation(
            root=None,
            info=ghl_mock_info,
            input=register_data,
        )

    assert User.objects.count() == 1


def _get_register_data() -> Dict[str, str]:
    """Create register data."""
    return {
        "email": EMAIL,
        "password": DEFAULT_USER_PASSWORD,
        "first_name": "first name",
        "last_name": "last name",
    }
