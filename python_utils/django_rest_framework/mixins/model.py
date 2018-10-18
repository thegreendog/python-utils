"""Model related mixin classes"""
import json
import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from python_utils.django_rest_framework.serializers import (AllElementsQuerySerializer,
                                                            DeleteQuerySerializer)


class DestroyActivatableModelMixin:
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


class ListActivatableModelMixin(ListModelMixin):
    @swagger_auto_schema(query_serializer=AllElementsQuerySerializer)
    def list(self, request, *args, **kwargs):
        query_params = AllElementsQuerySerializer(request.query_params)
        all_elements = query_params.data.get('all_elements', False)
        if not all_elements:
            self.queryset = self.queryset.filter(is_active=True)
        return super().list(request, *args, **kwargs)
