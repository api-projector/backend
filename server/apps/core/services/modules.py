import injector

from apps.core import services
from apps.core.logic import interfaces
from apps.core.logic.messages.interfaces import IMessagesBus


class CoreInfrastructureModule(injector.Module):
    """Setup di for core services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(interfaces.ICouchDBService, services.CouchDBService)
        binder.bind(
            IMessagesBus,
            services.MessagesBus,
            scope=injector.singleton,
        )
