"""Logging related mixin classes"""
import json
import logging

from python_utils.django.serializer.json import DjangoWithFileJSONEncoder
from rest_framework import status

LOGGER = logging.getLogger(__name__)


class LoggingMixin():
    """Log Mixin only when one of the following methods is being performed"""

    allowed_logging_methods = ('post', 'put', 'patch', 'delete')

    def finalize_response(self, request, response, *args, **kwargs):
        """Override finalize_response"""
        # regular finalize response
        response = super().finalize_response(request, response, *args, **kwargs)
        # do not log, if method not found
        if request.method.lower() not in self.allowed_logging_methods:
            return response
        status_code = response.status_code
        log_kwargs = {
            'view': self.get_view_name(),
            'action': self.action,
            'method': request.method.lower(),
            'status_code': status_code,
            'request_path': request.path,
            'request_data': request.data,
        }
        if status.is_server_error(status_code):
            LOGGER.error('DRF server error: {}'.format(json.dumps(log_kwargs, cls=DjangoWithFileJSONEncoder)))
        elif status.is_client_error(status_code):
            LOGGER.warning('DRF client error: {}'.format(json.dumps(log_kwargs, cls=DjangoWithFileJSONEncoder)))
        else:
            LOGGER.info("DRF successfully finished: {}".format(json.dumps(log_kwargs, cls=DjangoWithFileJSONEncoder)))
        return response
