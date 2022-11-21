from graphql import GraphQLResolveInfo


def create_mock_info(context=None, fragments=None) -> GraphQLResolveInfo:
    """Create mock info."""
    return GraphQLResolveInfo(
        None,
        None,
        None,
        None,
        path=None,
        schema=None,
        fragments=fragments,
        root_value=None,
        operation=None,
        variable_values=None,
        context=context,
        is_awaitable=None,
    )
