from django.apps import AppConfig
from jnt_django_toolbox.helpers.modules import load_module_from_app


class BaseAppConfig(AppConfig):
    """Base class representing a Django application and its configuration."""

    def ready(self):
        """Run this code when Django starts."""
        load_module_from_app(self, "graphql.types")
