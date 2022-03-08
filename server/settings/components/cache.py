from decouple import config

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": config("DJANGO_MEMCACHED", "memcached:11211"),
    },
}
