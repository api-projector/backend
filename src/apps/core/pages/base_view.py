from django.http import Http404, HttpRequest
from django.views import View

from apps.core.errors import BaseError
from apps.core.logic.errors import ObjectNotFoundError


class BaseView(View):
    """Base view."""

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        """Dispatch request."""
        try:
            return super().dispatch(request, *args, **kwargs)
        except BaseError as err:
            return self._handle_error(request, err)

    def _handle_error(self, request: HttpRequest, err: BaseError):
        if isinstance(err, ObjectNotFoundError):
            raise Http404()

        raise err
