from apps.projects.graphql.mutations import project, projects_asset


class ProjectsMutations(
    project.ProjectsMutations,
    projects_asset.ProjectsAssetsMutations,
):
    """All projects mutations."""
