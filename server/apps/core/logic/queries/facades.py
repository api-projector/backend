from apps.core import injector
from apps.core.logic.queries import IQuery, IQueryBus


def execute_query(query: IQuery):
    """Execute query."""
    query_bus = injector.get(IQueryBus)
    return query_bus.dispatch(query)
