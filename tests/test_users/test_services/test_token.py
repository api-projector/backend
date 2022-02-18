from datetime import timedelta

import pytest
from django.utils import timezone

from apps.core import injector
from apps.users.models import Token
from apps.users.services.token import TokenService

TOKEN_EXPIRE = 5


@pytest.fixture()
def token_service() -> TokenService:
    """Provides user token."""
    return injector.get(TokenService)


def test_create_user_token(user, token_service):
    """Test create user token."""
    user_tokens = list(
        Token.objects.filter(user=user).values_list("key", flat=True),
    )
    token = token_service.create_user_token(user)

    assert token
    assert token.key not in user_tokens


def test_clear_tokens(user, token_service, settings):
    """Test clear user token."""
    settings.TOKEN_EXPIRE_PERIOD = TOKEN_EXPIRE

    token = token_service.create_user_token(user)
    Token.objects.filter(pk=token.pk).update(
        created=timezone.now() - timedelta(minutes=TOKEN_EXPIRE + 1),
    )

    token_service.clear_tokens()

    assert not Token.objects.filter(pk=token.pk).exists()


def test_clear_tokens_not_expire(user, token_service, settings):
    """Test create user token if not expire."""
    settings.TOKEN_EXPIRE_PERIOD = TOKEN_EXPIRE

    token = token_service.create_user_token(user)

    token_service.clear_tokens()

    assert Token.objects.filter(pk=token.pk).exists()


def test_clear_tokens_token_expire_is_none(user, token_service, settings):
    """Test clear tokens if expire is none."""
    settings.TOKEN_EXPIRE = None

    token = token_service.create_user_token(user)
    token_service.clear_tokens()

    assert Token.objects.filter(pk=token.pk).exists()
