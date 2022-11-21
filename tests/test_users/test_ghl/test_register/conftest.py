import pytest


@pytest.fixture(scope="session")
def register_mutation(ghl_mutations):
    """
    Register mutation.

    :param ghl_mutations:
    """
    return ghl_mutations.fields["register"].resolve
