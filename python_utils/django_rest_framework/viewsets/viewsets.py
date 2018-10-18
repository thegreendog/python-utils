"""Viewsets"""

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from python_utils.django_rest_framework.mixins.model import (DestroyActivatableModelMixin,
                                                             ListActivatableModelMixin)


class ActivatableModelViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              DestroyActivatableModelMixin,
                              ListActivatableModelMixin,
                              GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `list()` and `destroy()`, this one with forced mode for deleting or normal for deactivating
    """
    pass
