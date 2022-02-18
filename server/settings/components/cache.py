from decouple import config

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": config("DJANGO_MEMCACHED", "memcached:11211"),
    },
}
