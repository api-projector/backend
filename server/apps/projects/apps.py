from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.helpers.apps import BaseAppConfig
from apps.core.logic import messages


class AppConfig(BaseAppConfig):
    """App configuration."""

    name = "apps.projects"
    default = True
    verbose_name = _("VN__PROJECTS")

    def ready(self):
        """Trigger on app ready."""
        from apps.projects.logic.commands import (  # noqa: WPS433
            project as project_commands,
        )
        from apps.projects.logic.commands import (  # noqa: WPS433
            project_asset as project_assets_commands,
        )
        from apps.projects.logic.queries import (  # noqa: WPS433
            project as project_queries,
        )

        super().ready()

        self._setup_dependency_injection()

        messages.register_messages_handlers(
            # commands
            project_assets_commands.upload_figma.CommandHandler,
            project_assets_commands.upload_image.CommandHandler,
            project_commands.delete.CommandHandler,
            project_commands.update.CommandHandler,
            project_commands.create.CommandHandler,
            project_commands.import_swagger.CommandHandler,
            # queries
            project_queries.allowed.QueryHandler,
            project_queries.openapi.QueryHandler,
        )

    def _setup_dependency_injection(self) -> None:
        from apps.projects.services.modules import (  # noqa: WPS433
            ProjectInfrastructureServicesModule,
        )

        injector.binder.install(ProjectInfrastructureServicesModule)
