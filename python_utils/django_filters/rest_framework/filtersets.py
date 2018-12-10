"""Custom filtersets"""
from copy import deepcopy

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_filters import rest_framework as filters

from python_utils.django_filters.rest_framework import \
    filters as custom_filters

FILTER_FOR_DBFIELD_DEFAULTS = deepcopy(filters.filterset.FILTER_FOR_DBFIELD_DEFAULTS)
FILTER_FOR_DBFIELD_DEFAULTS.update({
    models.ImageField: {'filter_class': filters.CharFilter},
    models.FileField: {'filter_class': filters.CharFilter},
    ArrayField: {'filter_class': custom_filters.ArrayFieldFilter},
})


class BaseFilterSet(filters.FilterSet):
    """Base filter class with new Filter mappings"""
    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS


class UUIDInFilterSet(BaseFilterSet):
    """A filter class with id__in filter added"""
    id__in = custom_filters.UUIDInFieldFilter(field_name='id')
