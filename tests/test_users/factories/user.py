import factory
from django.contrib.auth.hashers import make_password

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """User factory."""

    class Meta:
        model = User

    email = factory.Sequence(lambda index: "user_{0}@gl.com".format(index))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = make_password(None)
    is_staff = False
    is_active = True
