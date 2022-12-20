from django.db import models
from django.db.models.fields.related_lookups import RelatedLookupMixin


@models.Field.register_lookup
class NotEqual(models.Lookup):
    """
    Provides __ne lookup.

    Based on https://docs.djangoproject.com/en/3.1/howto/custom-lookups/
    """

    lookup_name = "ne"

    def as_sql(self, compiler, connection):
        """Return sql."""
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        return "{0} <> {1}".format(lhs, rhs), lhs_params + rhs_params


class RelatedNotEqual(RelatedLookupMixin, NotEqual):
    """Not equal lookup for foreigns."""


models.ForeignObject.register_lookup(RelatedNotEqual)
