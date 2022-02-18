import pytest
from graphene_django.rest_framework.tests.test_mutation import mock_info
from graphql import ResolveInfo


@pytest.fixture()
def ghl_auth_mock_info(user, rf) -> ResolveInfo:
    """
    Ghl auth mock info.

    :param user:
    :param auth_rf:
    :rtype: ResolveInfo
    """
    rf.set_user(user)
    request = rf.post("/graphql/")

    return _get_mock_info(request)


@pytest.fixture()
def ghl_mock_info(rf) -> ResolveInfo:
    """
    Ghl mock info.

    :param rf:
    :rtype: ResolveInfo
    """
    request = rf.post("/graphql/")

    return _get_mock_info(request)


def _get_mock_info(request) -> ResolveInfo:
    """
    Get mock info.

    :param request:
    """
    m_info = mock_info()
    m_info.context = request
    m_info.field_asts = [{}]
    m_info.fragments = {}
    return m_info
