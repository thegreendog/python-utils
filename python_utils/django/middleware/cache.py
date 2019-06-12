"""Middlewares related with cache"""
from django.utils.cache import add_never_cache_headers


class NeverCacheMiddleware:  # pylint: disable=too-few-public-methods
    """
    Adds `Cache-Control: max-age=0, no-cache, no-store, must-revalidate`
    header to response if no previous Cache-control header is present
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not (("Cache-Control" in response) or ("cache-control" in response)):
            add_never_cache_headers(response)
        return response
