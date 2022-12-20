import graphene


class ImportSwaggerJobType(graphene.ObjectType):
    """ImportSwaggerJobType type."""

    class Meta:
        name = "ImportSwaggerJob"

    state = graphene.String(required=True)
    log = graphene.String(required=True)
