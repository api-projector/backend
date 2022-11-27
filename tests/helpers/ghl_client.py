from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse
from graphene.test import Client

from apps.users.models import Token, User
from apps.users.services.token import TokenService
from gql import schema


class GraphQLClient(Client):
    """Test graphql client."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializing."""
        super().__init__(schema, *args, **kwargs)

        self._user: User | None = None
        self._token: Token | None = None
        self._token_service = TokenService()

    def set_user(  # noqa: WPS615
        self,
        user: User,
        token: Token | None = None,
    ) -> None:
        """Set user for auth requests."""
        self._user = user

        if token is None:
            token = self._token_service.create_user_token(user)

        self._token = token

    def execute(self, *args, **kwargs) -> HttpResponse:
        """Execute graphql request."""
        request = HttpRequest()
        request.user = self._user or AnonymousUser()
        request.auth = self._token
        request.session = {}
        request.build_absolute_uri = lambda mock: mock

        kwargs["context_value"] = request

        return super().execute(*args, **kwargs)
