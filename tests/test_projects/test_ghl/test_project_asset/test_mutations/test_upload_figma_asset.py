import pytest

from apps.projects.models import FigmaIntegration
from apps.projects.models.project_asset import ProjectAssetSource
from apps.projects.services.figma import (
    ApiFigmaError,
    IntegrationNotFoundFigmaError,
)
from tests.test_projects.test_ghl.test_project_asset.test_mutations.helpers.register_figma_urls import (  # noqa: E501
    register_figma_bad_response,
    register_get_images,
    register_upload_image_url,
)

FIGMA_URL = "https://www.figma.com/file/f1gma_key/file-name?node-id=123"


def test_upload_raw_query(user, project, ghl_client, ghl_raw):
    """Test success raw query."""
    ghl_client.set_user(user)
    register_get_images()
    register_upload_image_url()

    response = ghl_client.execute(
        ghl_raw("upload_figma_asset"),
        variable_values={
            "input": {
                "project": project.pk,
                "url": FIGMA_URL,
            },
        },
    )

    assert "errors" not in response

    asset = response["data"]["uploadFigmaAsset"]["projectAsset"]

    assert asset["project"]["id"] == project.pk
    assert asset["source"] == ProjectAssetSource.FIGMA
    assert asset["file"]


def test_success(
    project,
    ghl_auth_mock_info,
    upload_figma_asset_mutation,
):
    """Test success upload."""
    register_get_images()
    register_upload_image_url()
    response = upload_figma_asset_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "project": project.pk,
            "url": FIGMA_URL,
        },
    )

    assert response.project_asset.project == project
    assert response.project_asset.source == ProjectAssetSource.FIGMA
    assert response.project_asset.file


def test_bad_response(
    ghl_auth_mock_info,
    project,
    upload_figma_asset_mutation,
):
    """Test error upload."""
    register_figma_bad_response()
    with pytest.raises(ApiFigmaError):
        upload_figma_asset_mutation(
            root=None,
            info=ghl_auth_mock_info,
            input={
                "project": project.pk,
                "url": FIGMA_URL,
            },
        )


def test_without_figma_token(
    ghl_auth_mock_info,
    project,
    upload_figma_asset_mutation,
):
    """Test upload without token."""
    FigmaIntegration.objects.filter(project=project).delete()
    register_get_images()
    register_upload_image_url()

    with pytest.raises(IntegrationNotFoundFigmaError):
        upload_figma_asset_mutation(
            root=None,
            info=ghl_auth_mock_info,
            input={
                "project": project.pk,
                "url": FIGMA_URL,
            },
        )


def test_not_owner(
    user,
    project,
    ghl_auth_mock_info,
    upload_figma_asset_mutation,
):
    """Test not allowed upload."""
    register_get_images()
    register_upload_image_url()
    response = upload_figma_asset_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "project": project.pk,
            "url": FIGMA_URL,
        },
    )

    assert response.project_asset.project == project
    assert response.project_asset.source == ProjectAssetSource.FIGMA
    assert response.project_asset.file


def test_owner(
    user,
    project,
    ghl_auth_mock_info,
    upload_figma_asset_mutation,
):
    """Test success as owner upload."""
    project.owner = user
    project.save()

    register_get_images()
    register_upload_image_url()
    response = upload_figma_asset_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "project": project.pk,
            "url": FIGMA_URL,
        },
    )

    assert response.project_asset.project == project
    assert response.project_asset.source == ProjectAssetSource.FIGMA
    assert response.project_asset.file
