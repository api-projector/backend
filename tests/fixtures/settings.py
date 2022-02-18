import pytest


@pytest.fixture(autouse=True)
def _django_settings(settings, tmpdir_factory) -> None:
    """Forces django test settings."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp("media", numbered=True)
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    settings.DOMAIN_NAME = "testserver"
    settings.LANGUAGE_CODE = "en"
