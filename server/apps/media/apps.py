from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.logic.commands import ICommandBus
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """App configuration."""

    name = "apps.media"
    default = True
    verbose_name = _("VN__MEDIA")

    def ready(self):
        """Trigger on app ready."""
        from apps.media.logic.commands import COMMANDS  # noqa: WPS433

        super().ready()

        self._setup_dependency_injection()
        injector.get(ICommandBus).register_many(COMMANDS)

    def _setup_dependency_injection(self) -> None:
        from apps.media.services.modules import (  # noqa: WPS433
            MediaInfrastructureServicesModule,
        )

        injector.binder.install(MediaInfrastructureServicesModule)
