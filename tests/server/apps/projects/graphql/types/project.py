import graphene
from django.db import models
from graphql import ResolveInfo
from jnt_django_graphene_toolbox import types

from apps.core.logic import queries
from apps.media.graphql.types import ImageType
from apps.projects.graphql.types import FigmaIntegrationType
from apps.projects.logic.queries.project import allowed
from apps.projects.models import Project
from apps.users.graphql.types import UserType


class ProjectType(types.BaseModelObjectType):
    """Project type."""

    class Meta:
        model = Project

    title = graphene.String()
    description = graphene.String()
    db_name = graphene.String()
    owner = graphene.Field(UserType)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    emblem = graphene.Field(ImageType)
    figma_integration = graphene.Field(FigmaIntegrationType)

    @classmethod
    def get_queryset(
        cls,
        queryset: models.QuerySet,
        info: ResolveInfo,  # noqa: WPS110
    ) -> models.QuerySet:
        """Get queryset."""
        return queries.execute_query(
            allowed.Query(
                user=(
                    None
                    if info.context.user.is_anonymous  # type: ignore
                    else info.context.user  # type: ignore
                ),
                queryset=queryset,
                only_owned=False,
            ),
        )
