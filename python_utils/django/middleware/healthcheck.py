"""Healthcheck related middlewares"""
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError

LOGGER = logging.getLogger("healthcheck")

HEALTHZ_PATH = getattr(settings, 'HEALTHZ_PATH', "/healthz")
READYZ_PATH = getattr(settings, 'READYZ_PATH', "/readyz")


class HealthCheckMiddleware:
    """Middleware to check health and readyness. Thank you ianlewis"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET":
            if request.path == HEALTHZ_PATH:
                return self.healthz(request)
            elif request.path == READYZ_PATH:
                return self.readyz(request)
        return self.get_response(request)

    def healthz(self, request):
        """Returns that the server is alive."""
        return HttpResponse("OK")

    def readyz(self, request):
        """Returns that the databases and caches are ready"""
        # Connect to each database and do a generic standard SQL query that doesn't
        # write any data and doesn't depend on any tables being present.
        try:
            from django.db import connections
            for name in connections:
                cursor = connections[name].cursor()
                cursor.execute("SELECT 1;")
                row = cursor.fetchone()
                if row is None:
                    return HttpResponseServerError("db: invalid response")
        except Exception as e:
            LOGGER.exception(e)
            return HttpResponseServerError("db: cannot connect to database.")

        # Call get_stats() to connect to each memcached instance and get it's stats.
        # This can effectively check if each is online.
        try:
            from django.core.cache import caches
            from django.core.cache.backends.memcached import BaseMemcachedCache
            for cache in caches.all():
                if isinstance(cache, BaseMemcachedCache):
                    stats = cache._cache.get_stats()
                    if len(stats) != len(cache._servers):
                        return HttpResponseServerError("cache: cannot connect to cache.")
        except Exception as e:
            LOGGER.exception(e)
            return HttpResponseServerError("cache: cannot connect to cache.")

        return HttpResponse("OK")
