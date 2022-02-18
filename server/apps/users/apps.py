from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.logic.commands import ICommandBus
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """Class represents the "users" application."""

    name = "apps.users"
    default = True
    verbose_name = _("VN__USERS")

    def ready(self):
        """Trigger on app ready."""
        from apps.users.logic.commands import COMMANDS  # noqa: WPS433

        super().ready()

        self._setup_dependency_injection()

        injector.get(ICommandBus).register_many(COMMANDS)

    def _setup_dependency_injection(self) -> None:
        from apps.users.logic.services.modules import (  # noqa: WPS433
            UserLogicServicesModule,
        )
        from apps.users.services.modules import (  # noqa: WPS433
            UserInfrastructureServicesModule,
        )

        injector.binder.install(UserInfrastructureServicesModule)
        injector.binder.install(UserLogicServicesModule)
