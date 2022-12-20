from django.utils.translation import gettext_lazy as _

from apps.core.services.errors import BaseInfrastructureError


class BaseRegistrationError(BaseInfrastructureError):
    """Base registration error."""


class UserAlreadyExistsError(BaseRegistrationError):
    """User already exists error."""

    code = "user_already_exists"
    message = _("MSG__USER_ALREADY_EXISTS")


class RegistrationInputError(BaseRegistrationError):
    """User registration input error."""

    code = "validation_error"
    message = _("MSG__NOT_VALID_REGISTRATION_INPUT")
