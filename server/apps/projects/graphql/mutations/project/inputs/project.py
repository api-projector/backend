import graphene


class UpdateFigmaIntegrationType(graphene.InputObjectType):
    """FigmaIntegration type."""

    token = graphene.String()


class BaseProjectInput(graphene.InputObjectType):
    """Base input for add/create project."""

    title = graphene.String()
    description = graphene.String()
    figma_integration = graphene.Field(UpdateFigmaIntegrationType)
    emblem = graphene.ID()
