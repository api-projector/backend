INSTALLED_APPS = (
    "jnt_admin_tools",
    "jnt_admin_tools.theming",
    "jnt_admin_tools.menu",
    "jnt_admin_tools.dashboard",
    # default django apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # django-admin
    "django.contrib.admin",
    "django.contrib.admindocs",
    # vendors
    "jnt_django_toolbox",
    "jnt_django_graphene_toolbox",
    "graphene_django",
    "django_extensions",
    "django_filters",
    "social_django",
    "rest_framework",
    "corsheaders",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    # apps
    "apps.core",
    "apps.users",
    "apps.projects",
    "apps.media",
)
