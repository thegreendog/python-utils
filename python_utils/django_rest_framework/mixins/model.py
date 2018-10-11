"""Model related mixin classes"""
import json
import logging

from drf_yasg.utils import swagger_auto_schema
from python_utils.django_rest_framework.serializers import \
    DeleteQuerySerializer
from rest_framework import status
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response


class DestroyActivatableModelMixin(object):
    """
    Destroy a model instance.
    """
    @swagger_auto_schema(query_serializer=DeleteQuerySerializer)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        query_params = DeleteQuerySerializer(request.query_params)
        force = query_params.data.get('force', False)
        self.perform_destroy(instance, force)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance, force=False):
        instance.delete(force=force)
