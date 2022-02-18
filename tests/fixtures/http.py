import httpretty
import pytest


@pytest.fixture(autouse=True)
def _http_pretty():
    """Forces disallow net connect."""
    httpretty.enable(allow_net_connect=False)
    httpretty.reset()
    yield

    httpretty.disable()
