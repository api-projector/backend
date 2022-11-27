import pytest

from apps.core import injector
from apps.core.logic.messages.interfaces import IMessagesBus


@pytest.fixture()
def messages_bus() -> IMessagesBus:
    """Command bus."""
    return injector.get(IMessagesBus)
