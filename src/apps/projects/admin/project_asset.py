from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.projects.models import ProjectAsset


@admin.register(ProjectAsset)
class ProjectAssetAdmin(BaseModelAdmin):
    """Project asset admin."""

    list_display = ("id", "project", "source")
    search_fields = ("source", "project__title")
    list_filter = ("source",)
    exclude = ("old_file",)
