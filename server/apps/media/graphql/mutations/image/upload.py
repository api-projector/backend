import graphene
from graphene_file_upload.scalars import Upload
from graphql import GraphQLResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.media.graphql.types import ImageType
from apps.media.logic.commands.images import upload_image


class UploadImageInput(graphene.InputObjectType):
    """User image input."""

    file = graphene.Field(Upload, required=True)  # noqa: WPS110
    left = graphene.Int(required=True)
    top = graphene.Int(required=True)
    width = graphene.Int(required=True)
    height = graphene.Int(required=True)
    scale = graphene.Float(required=True)


class UploadImageMutation(BaseCommandMutation):
    """Upload image mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        input = graphene.Argument(UploadImageInput, required=True)

    image = graphene.Field(ImageType)

    @classmethod
    def build_command(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> upload_image.Command:
        """Build command."""
        return upload_image.Command(
            user=info.context.user,  # type: ignore
            image_data=upload_image.UploadImageDto(**kwargs["input"]),
        )

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        command_result: upload_image.CommandResult,
    ) -> dict[str, object]:
        """Prepare response data."""
        return {"image": command_result.image}
