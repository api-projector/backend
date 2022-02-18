from django.utils.translation import gettext_lazy as _
from jnt_django_toolbox.helpers.modules import load_module_from_app

from apps.core import injector
from apps.core.utils.apps import BaseAppConfig


class AppConfig(BaseAppConfig):
    """Base class for app config."""

    name = "apps.core"
    default = True
    verbose_name = _("VN__CORE")

    def ready(self):
        """Trigger on app ready."""
        super().ready()

        load_module_from_app(self, "models.lookups")
        self._setup_dependency_injection()

    def _setup_dependency_injection(self) -> None:
        from apps.core.logic.modules import (  # noqa: WPS433
            CoreApplicationModule,
        )
        from apps.core.services.modules import (  # noqa: WPS433
            CoreInfrastructureModule,
        )

        injector.binder.install(CoreInfrastructureModule)
        injector.binder.install(CoreApplicationModule)
