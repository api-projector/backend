import pytest
from graphql import GraphQLResolveInfo

from tests.helpers.ghl_mock import create_mock_info


@pytest.fixture()
def ghl_auth_mock_info(user, rf) -> GraphQLResolveInfo:
    """
    Ghl auth mock info.

    :param user:
    :param auth_rf:
    :rtype: GraphQLResolveInfo
    """
    rf.set_user(user)
    request = rf.post("/graphql/")

    return _get_mock_info(request)


@pytest.fixture()
def ghl_mock_info(rf) -> GraphQLResolveInfo:
    """
    Ghl mock info.

    :param rf:
    :rtype: GraphQLResolveInfo
    """
    request = rf.post("/graphql/")

    return _get_mock_info(request)


def _get_mock_info(request) -> GraphQLResolveInfo:
    """
    Get mock info.

    :param request:
    """
    return create_mock_info(
        context=request,
        fragments={},
    )
