"""Custom pagination classes"""
from rest_framework.pagination import PageNumberPagination


class PageNumberPaginationWithPageSize(PageNumberPagination):
    """Default PageNumberPagination with page_size parameter defined"""
    page_size_query_param = 'page_size'
