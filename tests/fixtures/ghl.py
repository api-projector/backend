import pytest

from gql import schema
from tests.helpers.ghl_client import GraphQLClient
from tests.helpers.gql_raw_query_provider import GhlRawQueryProvider


@pytest.fixture(scope="session")
def ghl_queries():
    """Ghl queries."""
    return schema.graphql_schema.query_type


@pytest.fixture(scope="session")
def ghl_mutations():
    """Ghl mutations."""
    return schema.graphql_schema.mutation_type


@pytest.fixture()
def ghl_client() -> GraphQLClient:
    """
    Ghl client.

    :rtype: GraphQLClient
    """
    return GraphQLClient()


@pytest.fixture()
def ghl_raw(request) -> GhlRawQueryProvider:
    """Ghl raw query provider."""
    return GhlRawQueryProvider(request.fspath.dirname)
