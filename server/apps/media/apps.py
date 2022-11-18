from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.helpers.apps import BaseAppConfig
from apps.core.logic import messages


class AppConfig(BaseAppConfig):
    """App configuration."""

    default = True
    name = "apps.media"
    verbose_name = _("VN__MEDIA")

    def ready(self):
        """Trigger on app ready."""
        from apps.media.logic.commands import (  # noqa: WPS433
            images as images_commands,
        )

        super().ready()

        self._setup_dependency_injection()

        messages.register_messages_handlers(
            # commands
            images_commands.upload_image.CommandHandler,
            # queries
        )

    def _setup_dependency_injection(self) -> None:
        from apps.media.services.modules import (  # noqa: WPS433
            MediaInfrastructureServicesModule,
        )

        injector.binder.install(MediaInfrastructureServicesModule)
