"""Custom backends"""
from django_filters import rest_framework as filters

from python_utils.django_filters.rest_framework.filtersets import (BaseFilterSet,
                                                                   UUIDInFilterSet)


class BaseFilterBackend(filters.DjangoFilterBackend):
    """Base custom filter backend just with new filter mappings added"""
    filterset_base = BaseFilterSet


class UUIDInFilterBackend(filters.DjangoFilterBackend):
    """Custom filter backend with new filter mappings added and a default id__in field"""
    filterset_base = UUIDInFilterSet
