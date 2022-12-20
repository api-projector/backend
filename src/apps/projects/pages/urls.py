from django.urls import re_path

from apps.projects.pages import views

app_name = "projects"

urlpatterns = [
    re_path(
        "^projects/(?P<project_id>[0-9a-zA-Z-_]+)/export/openapi.(?P<output_format>yaml|json)$",  # noqa: E501
        views.export_openapi.View.as_view(),
        name="openapi-download",
    ),
]
