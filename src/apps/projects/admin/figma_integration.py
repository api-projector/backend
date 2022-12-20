from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.projects.models import FigmaIntegration


@admin.register(FigmaIntegration)
class FigmaIntegrationAdmin(BaseModelAdmin):
    """Figma integration admin."""

    search_fields = ("id",)
