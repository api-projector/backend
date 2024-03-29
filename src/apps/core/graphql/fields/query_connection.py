import enum
import typing as ty
from functools import partial

import graphene
from django.db import models
from graphene.relay import connection as relay_connection
from graphene.relay.connection import connection_adapter, page_info_adapter
from graphene_django import DjangoConnectionField, settings, utils
from graphql import GraphQLResolveInfo
from graphql_relay import (
    connection_from_array_slice,
    cursor_to_offset,
    get_offset_with_default,
    offset_to_cursor,
)
from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied
from jnt_django_graphene_toolbox.types import BaseModelObjectType
from promise import Promise

from apps.core.logic import messages


@ty.runtime_checkable
class InstancesQueryResult(ty.Protocol):
    """Query result with instances queryset field."""

    instances: models.QuerySet


class BaseQueryConnectionField(DjangoConnectionField):  # noqa: WPS214
    """Base class for model collections."""

    query: ty.Type[messages.BaseQuery]
    auth_required: bool = False

    def __init__(self, *args, **kwargs):
        """Initialize."""
        self.on = kwargs.pop("on", False)
        self.max_limit = kwargs.pop(
            "max_limit",
            settings.graphene_settings.RELAY_CONNECTION_MAX_LIMIT,
        )
        self.enforce_first_or_last = kwargs.pop(
            "enforce_first_or_last",
            settings.graphene_settings.RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST,
        )
        kwargs.setdefault("offset", graphene.Int())

        sort_argument = self._get_sort_argument()
        if sort_argument:
            kwargs["sort"] = sort_argument

        super().__init__(*args, **kwargs)

    @property
    def type(self):  # noqa: WPS125
        """Returns connection field type."""
        _type = super(  # noqa: WPS122 WPS608
            relay_connection.IterableConnectionField,
            self,
        ).type
        non_null = False
        if isinstance(_type, graphene.NonNull):
            _type = _type.of_type  # noqa: WPS122
            non_null = True

        if not issubclass(_type, BaseModelObjectType):
            raise ValueError(
                "BaseModelConnectionField only accepts BaseModelObjectType types",  # noqa: E501
            )

        if not _type._meta.connection:  # noqa: WPS437
            raise ValueError(
                "The type {0} doesn't have a connection".format(
                    _type.__name__,
                ),
            )

        connection_type = _type._meta.connection  # noqa: WPS437
        if non_null:
            return graphene.NonNull(connection_type)
        return connection_type

    @property
    def connection_type(self):
        """Return connection type."""
        if isinstance(self.type, graphene.NonNull):
            return self.type.of_type
        return self.type

    @property
    def node_type(self):
        """Return node type."""
        return self.connection_type._meta.node  # noqa: WPS437

    @property
    def model(self):
        """Return model."""
        return self.node_type._meta.model  # noqa: WPS437

    @classmethod
    def resolve_queryset(
        cls,
        connection,
        queryset,
        info,  # noqa: WPS110
        args,
    ):  # noqa: C901
        """Filter queryset."""
        queryset = connection._meta.node.get_queryset(  # noqa: WPS437
            queryset,
            info,
        )

        return messages.dispatch_message(cls.build_query(queryset, info, args))

    @classmethod
    def build_query(
        cls,
        queryset: models.QuerySet,
        info: GraphQLResolveInfo,  # noqa: WPS110
        args,
    ) -> messages.BaseQuery:
        """Get params for creating query."""
        raise NotImplementedError()

    @classmethod
    def resolve_connection(  # noqa: WPS210, C901
        cls,
        connection,
        args,
        iterable,
        max_limit=None,
    ):
        """Resolves connection."""
        # Remove the offset parameter and convert it to an after cursor.
        offset = args.pop("offset", None)
        after = args.get("after")
        if offset:
            if after:
                offset += (cursor_to_offset(after) or 0) + 1
            # input offset starts at 1 while the graphene offset starts at 0
            args["after"] = offset_to_cursor(offset - 1)

        iterable = utils.maybe_queryset(iterable)
        if isinstance(iterable, InstancesQueryResult):
            iterable = iterable.instances

        if isinstance(iterable, models.QuerySet):
            array_length = iterable.count()
        else:
            array_length = len(iterable)

        # If after is higher than array_length, connection_from_array_slice
        # would try to do a negative slicing which makes django throw an
        # AssertionError
        slice_start = min(
            get_offset_with_default(args.get("after"), -1) + 1,
            array_length,
        )
        array_slice_length = array_length - slice_start

        # Impose the maximum limit via the `first` field if neither first
        # or last are already provided (note that if any of them is provided
        # they must be under max_limit otherwise an error is raised).

        is_max_limit = (
            max_limit is not None
            and args.get("first", None) is None
            and args.get("last", None) is None
        )
        if is_max_limit:
            args["first"] = max_limit

        connection = connection_from_array_slice(
            iterable[slice_start:],
            args,
            slice_start=slice_start,
            array_length=array_length,
            array_slice_length=array_slice_length,
            connection_type=partial(connection_adapter, connection),
            edge_type=connection.Edge,
            page_info_type=page_info_adapter,
        )
        connection.iterable = iterable
        connection.length = array_length
        return connection

    @classmethod
    def connection_resolver(  # noqa: C901 WPS211 WPS210 R701 WPS231
        cls,
        resolver,
        connection,
        default_manager,
        queryset_resolver,
        max_limit,
        enforce_first_or_last,
        root,
        info,  # noqa: WPS110
        **args,
    ):
        """Return connection resolver."""
        if cls.auth_required and not info.context.user.is_authenticated:
            return GraphQLPermissionDenied()

        first = args.get("first")
        last = args.get("last")
        offset = args.get("offset")
        before = args.get("before")

        if enforce_first_or_last and not (first or last):
            raise ValueError(
                "You must provide a `first` or `last` value to properly paginate the `{0}` connection.".format(  # noqa: E501
                    info.field_name,
                ),
            )

        if max_limit:
            if first:
                if first > max_limit:
                    raise ValueError(
                        "Requesting {0} records on the `{1}` connection exceeds the `first` limit of {2} records.".format(  # noqa: E501
                            first,
                            info.field_name,
                            max_limit,
                        ),
                    )
                args["first"] = min(first, max_limit)

            if last:
                if last > max_limit:
                    raise ValueError(
                        "Requesting {0} records on the `{1}` connection exceeds the `last` limit of {2} records.".format(  # noqa: E501
                            last,
                            info.field_name,
                            max_limit,
                        ),
                    )
                args["last"] = min(last, max_limit)

        if offset is not None and before is not None:
            raise ValueError(
                "You can't provide a `before` value at the same time as an `offset` value to properly paginate the `{0}` connection.".format(  # noqa: E501
                    info.field_name,
                ),
            )

        # eventually leads to DjangoObjectType's get_queryset (accepts queryset)
        # or a resolve_foo (does not accept queryset)
        iterable = resolver(root, info, **args)
        if iterable is None:
            iterable = default_manager
        # thus the iterable gets refiltered by resolve_queryset
        # but iterable might be promise
        iterable = queryset_resolver(connection, iterable, info, args)
        on_resolve = partial(
            cls.resolve_connection,
            connection,
            args,
            max_limit=max_limit,
        )

        if Promise.is_thenable(iterable):
            return Promise.resolve(iterable).then(on_resolve)

        return on_resolve(iterable)

    def get_resolver(self, parent_resolver):
        """Returns resolver."""
        return partial(
            self.connection_resolver,
            parent_resolver,
            self.connection_type,
            self.get_manager(),
            self.get_queryset_resolver(),  # type: ignore
            self.max_limit,
            self.enforce_first_or_last,
        )

    def get_queryset_resolver(self):
        """Returns queryset resolver."""
        return self.resolve_queryset

    def get_manager(self) -> models.Manager:  # noqa: CCE001
        """Return manager."""
        if self.on:
            return getattr(self.model, self.on)

        return self.model._default_manager  # noqa: WPS437

    def _get_sort_argument(self) -> graphene.Argument | None:
        type_hints = ty.get_type_hints(self.query)
        sort_type = type_hints.get("sort")
        if not sort_type:
            return None

        if not isinstance(sort_type, enum.EnumMeta):
            sort_type = ty.get_args(sort_type)[0]

        return graphene.Argument(
            graphene.List(
                graphene.Enum.from_enum(sort_type),
            ),
        )
