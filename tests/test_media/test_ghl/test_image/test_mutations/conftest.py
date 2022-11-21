import pytest


@pytest.fixture(scope="session")
def upload_image_mutation(ghl_mutations):
    """Provides upload image graphql mutation."""
    return ghl_mutations.fields["uploadImage"].resolve
