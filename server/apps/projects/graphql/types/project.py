import graphene
from django.db import models
from graphql import GraphQLResolveInfo
from jnt_django_graphene_toolbox import types

from apps.core.logic import messages
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
        info: GraphQLResolveInfo,  # noqa: WPS110
    ) -> models.QuerySet:
        """Get queryset."""
        return messages.dispatch_message(
            allowed.Query(
                user=(
                    None
                    if info.context.user.is_anonymous
                    else info.context.user
                ),
                queryset=queryset.all(),
                only_owned=False,
            ),
        ).instances
