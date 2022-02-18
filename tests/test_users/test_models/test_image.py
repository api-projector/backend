from tests.test_media.factories.image import ImageFactory


def test_image_owner_none(user):
    """Test delete user but image not delete."""
    image = ImageFactory.create(created_by=user)
    user.delete()
    image.refresh_from_db()

    assert image.created_by is None
