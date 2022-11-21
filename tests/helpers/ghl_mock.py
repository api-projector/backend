from graphql import GraphQLResolveInfo


def create_mock_info(context=None, fragments=None) -> GraphQLResolveInfo:
    """Create mock info."""
    return GraphQLResolveInfo(
        field_name="",
        field_nodes=[],
        return_type=None,  # type: ignore
        parent_type=None,  # type: ignore
        path=None,  # type: ignore
        schema=None,  # type: ignore
        fragments=fragments,
        root_value=None,
        operation=None,  # type: ignore
        variable_values={},
        context=context,
        is_awaitable=None,  # type: ignore
    )
