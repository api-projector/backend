import graphene

from apps.core.graphql.fields import BaseQueryConnectionField
from apps.core.logic import queries
from apps.projects.graphql.types import ProjectType
from apps.projects.logic.queries.project import allowed


class ProjectConnectionField(BaseQueryConnectionField):
    """Handler for projects collections."""

    query = allowed.Query
    auth_required = True

    def __init__(self):
        """Initialize."""
        super().__init__(
            ProjectType,
            title=graphene.String(),
        )

    @classmethod
    def resolve_queryset(
        cls,
        connection,
        queryset,
        info,  # noqa: WPS110
        args,
    ):  # noqa: C901
        """Resolve queryset."""
        return queries.execute_query(
            cls.query(
                queryset=queryset,
                filters=allowed.ProjectFilter(
                    title=args.get("title"),
                ),
                sort=args.get("sort"),
                user=(
                    None
                    if info.context.user.is_anonymous
                    else info.context.user
                ),
            ),
        )
