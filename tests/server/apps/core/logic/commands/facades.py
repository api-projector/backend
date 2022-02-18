from apps.core import injector
from apps.core.logic.commands import ICommand, ICommandBus


def execute_command(command: ICommand):
    """Execute query."""
    command_bus = injector.get(ICommandBus)
    return command_bus.dispatch(command)
