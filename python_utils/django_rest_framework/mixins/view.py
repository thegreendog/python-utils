"""View related mixin classes"""
from rest_framework import permissions


class ActionViewMixin():  # pylint: disable=too-few-public-methods
    """View that performs an action"""

    def post(self, request, *args, **kwargs):
        """Validates data against serializer and performs an action"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self._action(serializer, request, *args, **kwargs)


class OpenViewMixin():  # pylint: disable=too-few-public-methods
    """Mixin for views which doesn't need authentication nor permission"""
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
