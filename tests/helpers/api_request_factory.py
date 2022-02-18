from typing import Optional

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from rest_framework.test import APIRequestFactory as DjangoAPIRequestFactory

from apps.users.models import Token, User
from apps.users.services.token import TokenService


class ApiRequestFactory(DjangoAPIRequestFactory):
    """Api request factory."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializing."""
        super().__init__(*args, **kwargs)

        self._user: Optional[User] = None
        self._token: Optional[Token] = None
        self._token_service = TokenService()

    def set_user(  # noqa: WPS615
        self,
        user: User,
        token: Optional[Token] = None,
    ) -> None:
        """Set user for auth requests."""
        self._user = user

        if token is None:
            token = self._token_service.create_user_token(user)

        self._token = token

    def get(self, *args, **kwargs):
        """Construct a GET request."""
        request = super().get(*args, **kwargs)
        self._auth_if_need(request)

        return request

    def post(self, *args, **kwargs):
        """Construct a POST request."""
        request = super().post(*args, **kwargs)
        self._auth_if_need(request)

        return request

    def _auth_if_need(self, request: HttpRequest) -> None:
        """
        Auth if need.

        :param request:
        :type request: HttpRequest
        :rtype: None
        """
        request.user = self._user or AnonymousUser()
        request.auth = self._token
