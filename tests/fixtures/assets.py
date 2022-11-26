import pytest

from tests.helpers.asset_provider import AssetsProvider


@pytest.fixture()
def assets(request):
    """
    Assets.

    :param request:
    """
    provider = AssetsProvider(request.fspath.dirname)
    yield provider
    provider.close()
