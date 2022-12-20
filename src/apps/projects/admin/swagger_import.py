from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.projects.models import SwaggerImport


@admin.register(SwaggerImport)
class SwaggerImportAdmin(BaseModelAdmin):
    """Swagger import admin."""

    list_display = ("project", "state", "created_at")
