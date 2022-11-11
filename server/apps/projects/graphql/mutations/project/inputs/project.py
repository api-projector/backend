import graphene
from graphene_file_upload.scalars import Upload


class UpdateFigmaIntegrationType(graphene.InputObjectType):
    """FigmaIntegration type."""

    token = graphene.String()


class ProjectFromSwaggerType(graphene.InputObjectType):
    """ProjectFromSwagger type."""

    scheme_url = graphene.String()
    scheme = graphene.Field(Upload)


class BaseProjectInput(graphene.InputObjectType):
    """Base input for add/create project."""

    title = graphene.String()
    description = graphene.String()
    figma_integration = graphene.Field(UpdateFigmaIntegrationType)
    emblem = graphene.ID()
    from_swagger = graphene.Field(ProjectFromSwaggerType)
