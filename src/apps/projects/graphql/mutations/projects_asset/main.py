from apps.projects.graphql.mutations import projects_asset


class ProjectsAssetsMutations:
    """All projects assets mutations."""

    upload_figma_asset = (
        projects_asset.upload_figma.UploadFigmaProjectAssetMutation.Field()
    )

    upload_image_asset = (
        projects_asset.upload_image.UploadImageProjectAssetMutation.Field()
    )
