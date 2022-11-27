from dataclasses import dataclass
from enum import Enum

import django_filters
from django.db import models

from apps.core.logic import messages, queries
from apps.projects.models import Project
from apps.users.models import User


class ProjectSort(Enum):
    """Allowed sort fields."""

    CREATED_AT_ASC = "created_at"  # noqa: WPS115
    CREATED_AT_DESC = "-created_at"  # noqa: WPS115


class _ProjectFilterSet(django_filters.FilterSet):
    """Tariff filterSet."""

    title = django_filters.CharFilter()


@dataclass(frozen=True)
class QueryResult:
    """Query result."""

    instances: models.QuerySet


@dataclass(frozen=True)
class ProjectFilter:
    """Project filter ."""

    title: str | None = None


class Query(messages.BaseQuery[QueryResult]):
    """List allowed projects."""

    user: User | None
    queryset: models.QuerySet | None = None
    sort: ProjectSort | None = None
    filters: ProjectFilter | None = None
    only_owned: bool = True


class QueryHandler(messages.BaseQueryHandler[Query]):
    """Allowed projects for user query."""

    def handle(self, query: Query) -> QueryResult:
        """Handler."""
        return QueryResult(
            instances=self._get_allowed_projects_for_user(query),
        )

    def _get_allowed_projects_for_user(self, query: Query):
        if not query.user:
            return Project.objects.none()

        projects = query.queryset
        if projects is None:
            projects = Project.objects.all()

        if query.only_owned:
            projects = projects.filter(owner=query.user)

        return queries.sort_queryset(
            queries.filter_queryset(
                projects,
                _ProjectFilterSet,
                query.filters,
            ),
            queries.SortHandler(ProjectSort),
            query.sort,
        )
