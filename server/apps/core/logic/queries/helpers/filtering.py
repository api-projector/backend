import dataclasses
import typing as ty

import django_filters
from django.db import models

from apps.core.logic.errors import InvalidInputApplicationError
from apps.core.utils.objects import empty


def filter_queryset(
    queryset: models.QuerySet,
    filterset_class: ty.Type[django_filters.FilterSet],
    filters,
) -> models.QuerySet:
    """Filter queryset."""
    if not filters:
        return queryset

    prepared_filters = _prepare_filters(filters)

    if not prepared_filters:
        return queryset

    filterset = filterset_class(data=prepared_filters, queryset=queryset)
    if not filterset.is_valid():
        raise InvalidInputApplicationError(filterset.errors)

    return filterset.qs


def _prepare_filters(filters) -> dict[str, object]:
    return {
        data_key: data_value
        for data_key, data_value in dataclasses.asdict(filters).items()
        if data_value != empty
    }
