from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.helpers.apps import BaseAppConfig
from apps.core.logic import messages


class AppConfig(BaseAppConfig):
    """Class represents the "users" application."""

    name = "apps.users"
    default = True
    verbose_name = _("VN__USERS")

    def ready(self):
        """Trigger on app ready."""
        from apps.users.logic.commands import register  # noqa: WPS433
        from apps.users.logic.commands.auth import (  # noqa: WPS433
            login,
            logout,
            social_complete_login,
            social_login,
        )
        from apps.users.logic.commands.me import update  # noqa: WPS433

        super().ready()

        self._setup_dependency_injection()

        messages.register_messages_handlers(
            # commands
            login.CommandHandler,
            logout.CommandHandler,
            update.CommandHandler,
            register.CommandHandler,
            social_login.CommandHandler,
            social_complete_login.CommandHandler,
            # queries
        )

    def _setup_dependency_injection(self) -> None:
        from apps.users.services.modules import (  # noqa: WPS433
            UserInfrastructureServicesModule,
        )

        injector.binder.install(UserInfrastructureServicesModule)
