import abc

from apps.users.models import Token, User


class ITokenService(abc.ABC):
    """User token service."""

    @abc.abstractmethod
    def create_user_token(self, user: User) -> Token:
        """Create token for user."""

    @abc.abstractmethod
    def delete_token(self, token: Token) -> None:
        """Remove token."""

    @abc.abstractmethod
    def clear_tokens(self) -> None:
        """Deletes expired tokens."""
