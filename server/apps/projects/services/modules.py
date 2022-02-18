import injector

from apps.projects import services
from apps.projects.logic import interfaces


class ProjectInfrastructureServicesModule(injector.Module):
    """Setup di for projects infrastructure services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(
            interfaces.IFigmaServiceFactory,
            services.FigmaServiceFactory,
            scope=injector.singleton,
        )
