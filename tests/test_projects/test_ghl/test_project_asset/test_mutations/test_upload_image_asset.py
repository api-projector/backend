import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.projects.models.project_asset import ProjectAssetSource

IMAGE_FILE = "image.jpg"


@pytest.fixture()
def in_memory_image(assets):
    """Wrap image to in memory."""
    image = assets.open_file(IMAGE_FILE)
    return InMemoryUploadedFile(
        image,
        "image",
        "middle.jpeg",
        "image/jpeg",
        42,
        "utf-8",
    )


def test_upload_raw_query(user, project, ghl_client, ghl_raw, in_memory_image):
    """Test success raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("upload_image_asset"),
        variable_values={
            "input": {
                "project": project.pk,
                "file": in_memory_image,
            },
        },
    )

    assert "errors" not in response

    asset = response["data"]["uploadImageAsset"]["projectAsset"]

    assert asset["project"]["id"] == project.pk
    assert asset["source"] == ProjectAssetSource.UPLOAD
    assert asset["file"]


def test_success(
    project,
    ghl_auth_mock_info,
    upload_image_asset_mutation,
    in_memory_image,
):
    """Test success upload."""
    response = upload_image_asset_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "project": project.pk,
            "file": in_memory_image,
        },
    )

    assert response.project_asset.project == project
    assert response.project_asset.source == ProjectAssetSource.UPLOAD
    assert response.project_asset.file
