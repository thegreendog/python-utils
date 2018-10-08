"""Viewsets"""

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from python_utils.django_rest_framework.mixins.model import \
    DestroyActivatableModelMixin


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   DestroyActivatableModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `list()` and `destroy()`, this one with forced mode for deleting or normal for deactivating
    """
    pass
