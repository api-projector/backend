from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from social_core.actions import do_complete
from social_core.utils import setting_name
from social_django.utils import psa
from social_django.views import _do_login  # noqa: WPS436, WPS450

NAMESPACE = getattr(settings, setting_name("URL_NAMESPACE"), None) or "social"


@never_cache
@csrf_exempt
@psa("{0}:complete".format(NAMESPACE))
def auth_complete(request, backend, *args, **kwargs):
    """Authentication complete view."""
    return do_complete(
        request.backend,
        _do_login,
        user=None,
        redirect_name=REDIRECT_FIELD_NAME,
        request=request,
        *args,  # noqa: B026
        **kwargs,
    )
