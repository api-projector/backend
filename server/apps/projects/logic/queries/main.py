from apps.projects.logic.queries import project

QUERIES = (
    (project.allowed.Query, project.allowed.QueryHandler),
    (project.openapi.Query, project.openapi.QueryHandler),
)
