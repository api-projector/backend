import graphene
from graphql import ResolveInfo

from apps.projects.models import FigmaIntegration


class FigmaIntegrationType(graphene.ObjectType):
    """FigmaIntegration type."""

    class Meta:
        name = "FigmaIntegration"

    token = graphene.String(required=True)

    def resolve_token(
        self: FigmaIntegration,
        info: ResolveInfo,  # noqa: WPS110
    ) -> str | None:
        """Resolve token integration."""
        return "*" if self.token else None
