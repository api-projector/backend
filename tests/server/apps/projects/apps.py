from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.logic.commands import ICommandBus
from apps.core.logic.queries import IQueryBus
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """App configuration."""

    name = "apps.projects"
    default = True
    verbose_name = _("VN__PROJECTS")

    def ready(self):
        """Trigger on app ready."""
        from apps.projects.logic.commands import COMMANDS  # noqa: WPS433
        from apps.projects.logic.queries import QUERIES  # noqa: WPS433

        super().ready()

        self._setup_dependency_injection()
        injector.get(ICommandBus).register_many(COMMANDS)
        injector.get(IQueryBus).register_many(QUERIES)

    def _setup_dependency_injection(self) -> None:
        from apps.projects.services.modules import (  # noqa: WPS433
            ProjectInfrastructureServicesModule,
        )

        injector.binder.install(ProjectInfrastructureServicesModule)
