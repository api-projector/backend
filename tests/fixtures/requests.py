import pytest

from tests.helpers.api_request_factory import ApiRequestFactory
from tests.helpers.request_factory import RequestFactory


@pytest.fixture()
def rf() -> RequestFactory:
    """Request factory."""
    return RequestFactory()


@pytest.fixture()
def admin_rf(rf, admin_user) -> RequestFactory:
    """Admin request factory with setted admin user."""
    rf.set_user(admin_user)

    return rf


@pytest.fixture()
def api_rf() -> ApiRequestFactory:
    """Api request factory."""
    return ApiRequestFactory()
