"""View related mixin classes"""


class ActionViewMixin():  # pylint: disable=too-few-public-methods
    """View that performs an action"""

    def post(self, request, **kwargs):
        """Validates data against serializer and performs an action"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self._action(serializer, request, **kwargs)
