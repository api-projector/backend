from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from apps.users.logic.interfaces import ITokenService
from apps.users.models import Token, User


class TokenService(ITokenService):
    """Service for manage tokens."""

    def create_user_token(self, user: User) -> Token:
        """Create token for user."""
        return Token.objects.create(user=user)

    def delete_token(self, token: Token) -> None:
        """Remove token."""
        token.delete()

    def clear_tokens(self) -> None:
        """Deletes expired tokens."""
        if settings.TOKEN_EXPIRE_PERIOD is None:
            return

        created = timezone.now() - timedelta(
            minutes=settings.TOKEN_EXPIRE_PERIOD,
        )

        Token.objects.filter(created__lt=created).delete()
