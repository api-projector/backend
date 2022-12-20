from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.projects.admin.inlines import FigmaIntegrationInline
from apps.projects.models import Project


@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    """Project admin."""

    list_display = ("title", "id", "owner", "created_at")
    search_fields = ("title",)
    inlines = (FigmaIntegrationInline,)
