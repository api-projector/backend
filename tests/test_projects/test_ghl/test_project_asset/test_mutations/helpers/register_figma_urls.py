import json
from http import HTTPStatus

from httpretty import httpretty

from tests.helpers.asset_provider import AssetsProvider


def register_get_images() -> None:
    """Register images urls."""
    assets = AssetsProvider(__file__)
    httpretty.register_uri(
        httpretty.GET,
        "https://api.figma.com/v1/images/f1gma_key",
        content_type="text/json",
        status=HTTPStatus.OK,
        body=json.dumps(assets.read_json("figma_response")),
    )
    assets.close()


def register_figma_bad_response() -> None:
    """Register figma bad response."""
    assets = AssetsProvider(__file__)
    httpretty.register_uri(
        httpretty.GET,
        "https://api.figma.com/v1/images/f1gma_key",
        content_type="text/json",
        status=HTTPStatus.FORBIDDEN,
        body=json.dumps(assets.read_json("figma_bad_response")),
    )
    assets.close()


def register_upload_image_url() -> None:
    """Register upload image url."""
    assets = AssetsProvider(__file__)
    httpretty.register_uri(
        httpretty.GET,
        "https://s3-us-west-2.amazonaws.com/img/123",
        body=assets.open_file("image.jpg").read(),
    )
    assets.close()
