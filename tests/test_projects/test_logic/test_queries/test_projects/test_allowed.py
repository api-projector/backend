import pytest

from apps.core.logic import messages
from apps.projects.logic.queries.project.allowed import Query
from tests.test_projects.factories.project import ProjectFactory


@pytest.fixture()
def project(db):
    """Create project."""
    return ProjectFactory.create()


def test_anonymous(project):
    """Test available is public project."""
    query_result = messages.dispatch_message(
        Query(user=None),
    )

    assert not query_result.instances.exists()


def test_owner(user, project):
    """Test empty projects."""
    project.owner = user
    project.save()

    query_result = messages.dispatch_message(
        Query(user=user),
    )

    assert query_result.instances.count() == 1
    assert query_result.instances.first() == project


def test_not_owner(user, project):
    """Test empty projects."""
    query_result = messages.dispatch_message(
        Query(user=user),
    )

    assert query_result.instances.count() == 0


def test_not_owner_but_not_only_owned(user, project):
    """Test empty projects."""
    query_result = messages.dispatch_message(
        Query(
            user=user,
            only_owned=False,
        ),
    )

    assert query_result.instances.count() == 1
    assert query_result.instances.first() == project
