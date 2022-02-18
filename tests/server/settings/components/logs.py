import sentry_sdk
from decouple import config
from graphql import GraphQLError
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from settings.components.ap import AP_APP_VERSION

STANDARD_FORMAT = "[%(asctime)s]|%(levelname)s|%(module)s.%(funcName)s:%(lineno)s|%(message)s"  # noqa: E501, WPS323

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": STANDARD_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",  # noqa: WPS323
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# graphene wtf!!!
IGNORED_ERRORS_TXT = ("graphql.error.located_error.GraphQLLocatedError",)


class _BeforeSendHandler:
    def __call__(self, event, hint):
        """Filter by exception."""
        exc_info = hint.get("exc_info")

        skip_event = (
            exc_info and self._skip_by_error(exc_info)
        ) or self._skip_by_message(event)

        if not skip_event:
            return event

    def _skip_by_error(self, exc_info) -> bool:
        exc_type, exc_value, tb = exc_info
        return isinstance(exc_value, GraphQLError)

    def _skip_by_message(self, event) -> bool:
        return any(
            err in event["logentry"]["message"] for err in IGNORED_ERRORS_TXT
        )


sentry_dsn = config("DJANGO_SENTRY_DSN", default=None)
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        release=AP_APP_VERSION,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        send_default_pii=True,
        before_send=_BeforeSendHandler(),
    )
    sentry_sdk.utils.MAX_STRING_LENGTH = 4096
