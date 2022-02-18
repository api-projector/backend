import factory

from apps.media.models import Image
from tests.test_users.factories.user import UserFactory


class ImageFactory(factory.django.DjangoModelFactory):
    """Image factory."""

    class Meta:
        model = Image

    storage_image = factory.django.ImageField()
    original_filename = factory.Sequence(
        lambda index: "Image {0}.jpg".format(index),
    )
    created_by = factory.SubFactory(UserFactory)
