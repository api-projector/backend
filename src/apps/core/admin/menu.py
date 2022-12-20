from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from jnt_admin_tools.menu import Menu as BaseMenu
from jnt_admin_tools.menu import items

MANAGEMENT_MENU_ITEMS = ((_("VN__JOB_QUEUE"), "/admin/flower/", None),)
UTILS_MENU_ITEMS = ((_("VN__GRAPHQL_PLAYGROUND"), "/graphql/", None),)


class AdminMenuItem(items.MenuItem):
    """Admin menu item."""

    def __init__(self, title, menu_items) -> None:
        """Initializing AdminMenuItem."""
        super().__init__(title)
        self.menu_items = menu_items

    def init_with_context(self, context):
        """Init menu items."""
        for title, url, perm in self.menu_items:
            if perm and not context.request.user.has_perm(perm):
                continue

            self.children.append(items.MenuItem(title, url))


class Menu(BaseMenu):
    """A class represents menu admin dashboard."""

    def __init__(self, **kwargs):
        """
        Initialize self.

        Add menu item in Admin Dashboard.
        """
        super().__init__(**kwargs)

        self.children += [
            items.MenuItem(_("VN__HOME"), reverse_lazy("admin:index")),
            items.AppList(_("VN__APPLICATIONS")),
            AdminMenuItem(_("VN__MANAGEMENT"), MANAGEMENT_MENU_ITEMS),
            AdminMenuItem(_("VN__UTILS"), UTILS_MENU_ITEMS),
        ]
