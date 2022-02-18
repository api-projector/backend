from graphene_django.rest_framework.tests.test_mutation import mock_info

from apps.projects.graphql.types import FigmaIntegrationType
from tests.test_projects.factories.figma_integration import (
    FigmaIntegrationFactory,
)


def test_resolve_token(project):
    """Test resolve filled tokens."""
    integration = FigmaIntegrationFactory.create(project=project)

    assert FigmaIntegrationType.resolve_token(integration, mock_info()) == "*"


def test_resolve_empty_tokens(project):
    """Test resolve not filled tokens."""
    integration = FigmaIntegrationFactory.create(project=project, token="")

    assert FigmaIntegrationType.resolve_token(integration, mock_info()) is None
