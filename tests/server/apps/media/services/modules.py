import injector

from apps.media import services
from apps.media.logic import interfaces


class MediaInfrastructureServicesModule(injector.Module):
    """Setup di for media infrastructure services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(
            interfaces.IImageDownloadService,
            services.ImageDownloadService,
        )
        binder.bind(
            interfaces.ICleanupMediaFilesService,
            services.CleanupMediaFilesService,
        )
