import graphene
from jnt_django_graphene_toolbox.nodes import ModelRelayNode

from apps.projects.graphql.fields import ProjectConnectionField
from apps.projects.graphql.types import ProjectType


class ProjectsQueries(graphene.ObjectType):
    """Project graphql queries."""

    project = ModelRelayNode.Field(ProjectType)
    all_projects = ProjectConnectionField()
