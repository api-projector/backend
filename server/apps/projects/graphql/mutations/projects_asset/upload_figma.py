import graphene
from graphql import GraphQLResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.projects.graphql.types import ProjectAssetType
from apps.projects.logic.commands.project_asset import (
    upload_figma as project_asset_create,
)


class UploadFigmaProjectAssetInput(graphene.InputObjectType):
    """Input for create figma project asset."""

    project = graphene.ID(required=True)
    url = graphene.String(required=True)


class UploadFigmaProjectAssetMutation(BaseCommandMutation):
    """Create project asset mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        input = graphene.Argument(  # noqa: WPS125
            UploadFigmaProjectAssetInput,
            required=True,
        )

    project_asset = graphene.Field(ProjectAssetType)

    @classmethod
    def build_command(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> project_asset_create.Command:
        """Build command."""
        return project_asset_create.Command(
            user=info.context.user,
            data=project_asset_create.FigmaProjectAssetDto(
                **kwargs.get("input"),
            ),
        )

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        command_result: project_asset_create.CommandResult,
    ) -> dict[str, object]:
        """Prepare response data."""
        return {
            "project_asset": command_result.project_asset,
        }
