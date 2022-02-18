from apps.core.admin.inlines import BaseTabularInline
from apps.projects.models import FigmaIntegration


class FigmaIntegrationInline(BaseTabularInline):
    """Figma integration inline."""

    model = FigmaIntegration
