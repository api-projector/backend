import factory

from apps.media.models import File
from tests.test_users.factories.user import UserFactory


class FileFactory(factory.django.DjangoModelFactory):
    """File factory."""

    class Meta:
        model = File

    storage_file = factory.django.FileField()
    original_filename = factory.Sequence(
        lambda index: "File {0}.dat".format(index),
    )
    created_by = factory.SubFactory(UserFactory)
