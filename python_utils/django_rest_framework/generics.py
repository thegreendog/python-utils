"""Generics for rest framework"""
from rest_framework import mixins
from rest_framework.generics import GenericAPIView


class PutAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """Concrete view for putting a model instance."""

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class PatchAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """Concrete view for patching a model instance."""

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
