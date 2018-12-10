"""Custom filters"""
from django_filters import rest_framework as filters


class UUIDInFieldFilter(filters.BaseInFilter, filters.UUIDFilter):
    """Class for generating an id__in field"""


class ArrayFieldFilter(filters.BaseCSVFilter, filters.CharFilter):
    """For working with PostgreSQL's ArrayFields"""

    def __init__(self, *args, **kwargs):
        kwargs['lookup_expr'] = 'contains'
        super().__init__(*args, **kwargs)
