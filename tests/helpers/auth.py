from apps.core import injector
from apps.users.logic.interfaces import IAuthenticationService


def check_auth(email, password) -> None:
    """Check success auth after register user."""
    auth = injector.get(IAuthenticationService)
    assert auth.auth(email, password)
