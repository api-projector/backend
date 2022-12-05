SECRET_KEY = "tests"  # noqa: S105

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "api-projector",
        "USER": "api-projector",
        "PASSWORD": "api-projector",
        "HOST": "postgres",
    },
}

CELERY_TASK_ALWAYS_EAGER = True
CONSTANCE_BACKEND = "constance.backends.memory.MemoryBackend"
CONSTANCE_DATABASE_CACHE_BACKEND = (
    "django.core.cache.backends.dummy.DummyCache"
)
CACHES = {
    "default": {"BACKEND": CONSTANCE_DATABASE_CACHE_BACKEND},
}
