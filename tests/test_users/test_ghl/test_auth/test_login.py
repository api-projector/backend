from apps.core.graphql.errors import GenericGraphQLError
from apps.users.models import Token
from apps.users.services.auth import AuthenticationError
from tests.fixtures.users import DEFAULT_EMAIL, DEFAULT_USER_PASSWORD


def test_query(user, ghl_client, ghl_raw):
    """Test login raw query."""
    assert not Token.objects.filter(user=user).exists()

    response = ghl_client.execute(
        ghl_raw("login"),
        variable_values={
            "input": {
                "email": DEFAULT_EMAIL,
                "password": DEFAULT_USER_PASSWORD,
            },
        },
    )

    assert "errors" not in response

    token = Token.objects.filter(user=user).first()
    assert token is not None
    assert response["data"]["login"]["token"]["key"] == token.key


def test_success(user, ghl_mock_info, login_mutation):
    """Test success login."""
    assert not Token.objects.filter(user=user).exists()

    response = login_mutation(
        root=None,
        info=ghl_mock_info,
        input={
            "email": DEFAULT_EMAIL,
            "password": DEFAULT_USER_PASSWORD,
        },
    )

    assert Token.objects.filter(pk=response.token.pk, user=user).exists()


def test_wrong_username(user, ghl_mock_info, login_mutation):
    """Test wrong username case."""
    assert not Token.objects.filter(user=user).exists()

    response = login_mutation(
        None,
        ghl_mock_info,
        input={
            "email": "wrong{0}".format(DEFAULT_EMAIL),
            "password": DEFAULT_USER_PASSWORD,
        },
    )

    assert isinstance(response, GenericGraphQLError)
    assert response.original_error.code == AuthenticationError.code
    assert not Token.objects.filter(user=user).exists()


def test_wrong_password(user, ghl_mock_info, login_mutation):
    """Test wrong password case."""
    assert not Token.objects.filter(user=user).exists()

    response = login_mutation(
        None,
        ghl_mock_info,
        input={
            "email": DEFAULT_EMAIL,
            "password": "wrong{0}".format(DEFAULT_USER_PASSWORD),
        },
    )

    assert isinstance(response, GenericGraphQLError)
    assert response.original_error.code == AuthenticationError.code
    assert not Token.objects.filter(user=user).exists()


def test_empty_credentials(user, ghl_mock_info, login_mutation):
    """Test empty credentials."""
    assert not Token.objects.filter(user=user).exists()

    response = login_mutation(
        None,
        ghl_mock_info,
        input={
            "email": "",
            "password": "",
        },
    )

    assert isinstance(response, GenericGraphQLError)
    assert not Token.objects.filter(user=user).exists()
