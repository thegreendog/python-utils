"""Model related mixin classes"""
import json
import logging

from rest_framework import status
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response


class DestroyActivatableModelMixin(object):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        force = request.query_params.get('force', False)
        self.perform_destroy(instance, force)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance, force=False):
        instance.delete(force=force)
