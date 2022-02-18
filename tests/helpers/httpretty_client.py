import json
from http import HTTPStatus
from typing import Dict, List, Optional

import httpretty
from httpretty.core import HTTPrettyRequest


class _RequestCallbackFactory:
    """Create request callback."""

    def __init__(
        self,
        body: Optional[object] = None,
        status: int = HTTPStatus.OK,
    ) -> None:
        """Initializing."""
        self._body = body or {}
        self._status = status

    def __call__(
        self,
        request: HTTPrettyRequest,
        uri: str,
        response_headers: Dict[str, str],
    ) -> List[object]:
        response_headers["Content-Type"] = "application/json"

        return [self._status, response_headers, json.dumps(self._body)]


class HttprettyMock:
    """Httpretty mocker."""

    base_api_url = ""

    def __init__(self) -> None:
        """Initializing."""
        assert httpretty.is_enabled()

    def register_get(
        self,
        path: str,
        body: Optional[object] = None,
        status: int = HTTPStatus.OK,
    ) -> None:
        """Registry url for mock get-query."""
        self._register_url(
            method=httpretty.GET,
            uri=self._prepare_uri(path),
            request_callback=_RequestCallbackFactory(body, status),
            priority=1,
        )

    def register_post(
        self,
        path: str,
        body: Optional[object] = None,
        status: int = HTTPStatus.OK,
    ) -> None:
        """Registry url for mock post-query."""
        self._register_url(
            method=httpretty.POST,
            uri=self._prepare_uri(path),
            request_callback=_RequestCallbackFactory(body, status),
            priority=1,
        )

    def _register_url(
        self,
        method: str,
        uri: str,
        request_callback: _RequestCallbackFactory,
        priority: int = 0,
    ) -> None:
        httpretty.register_uri(
            method=method,
            uri=uri,
            body=request_callback,
            priority=priority,
        )

    def _prepare_uri(self, path: str) -> str:
        return "{0}{1}".format(self.base_api_url, path)
