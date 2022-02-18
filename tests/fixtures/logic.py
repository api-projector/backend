import pytest

from apps.core import injector
from apps.core.logic.commands import ICommandBus
from apps.core.logic.queries import IQueryBus


@pytest.fixture()
def command_bus() -> ICommandBus:
    """Command bus."""
    return injector.get(ICommandBus)


@pytest.fixture()
def query_bus() -> IQueryBus:
    """Query bus."""
    return injector.get(IQueryBus)
