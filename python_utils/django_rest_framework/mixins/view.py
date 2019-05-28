"""View related mixin classes"""
from functools import partial
import copy
import json

import requests
from django.conf import settings
from django.utils import translation
from rest_framework import permissions
from rest_framework.response import Response

from python_utils.generic.defaults import DEFAULT_REQUEST_TIMEOUT


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


class ProxyBaseViewMixin():
    """
    Custom API view to perform a proxy request. Some fields to define:
    - upstream: destination endpoint. Can have parameters to be filled with format function or can be a partial
    """
    upstream = None

    def get_headers(self):
        """Passes through the language"""
        return {'Accept-Language': translation.get_language()}

    def get_url(self):
        """Completes the url against kwargs"""
        if isinstance(self.upstream, str):
            return self.upstream.format(**self.kwargs)
        if isinstance(self.upstream, partial):
            return self.upstream(**self.kwargs)  # pylint: disable=not-callable
        raise ValueError('upstream has to be an string or a partial')


class ProxyDjangoViewMixin(ProxyBaseViewMixin):
    """
    Custom query parameter management for proxy views that point to Django views. Some fields to define:
    - fields: set or list of the fields that we want to return
    - parameters: set or list of the parameters we enable to filter against
    - page_size: if set, will be the number of results per page
    - page_size_param: name of the `page_size` parameter to be used
    - page_param: name of the `page` parameter to be used
    - keys_to_remove: keys to remove from response JSON (tipical Django keys)
    """
    fields = None
    parameters = None
    page_size = None
    page_size_param = 'page_size'
    page_param = 'page'
    keys_to_remove = ('count', 'next', 'previous')

    def get_query_params(self):
        """Construct the query parameters based on fields and parameters"""
        query_params = {}
        if self.fields:
            query_params['fields'] = ','.join(str(field) for field in self.fields)
        if self.parameters:
            for parameter in self.parameters:
                parameter_value = self.request.query_params.get(parameter, None)
                if parameter_value:
                    query_params[parameter] = parameter_value
        if self.page_size:
            query_params[self.page_size_param] = self.page_size
            parameter_value = self.request.query_params.get(self.page_param, None)
            if parameter_value:
                query_params[self.page_param] = parameter_value
        return query_params


class ProxyEveViewMixin(ProxyBaseViewMixin):
    """
    Custom query parameter management for proxy views that point to EVE views. Some fields to define:
    - initial_query_params: initial query parameters
    - fields: set or list of the fields that we want to return
    - parameters: set or list of the parameters we enable to filter against
    - page_size: if set, will be the number of results per page
    - page_size_param: name of the `page_size` parameter to be used
    - page_param: name of the `page` parameter to be used
    - keys_to_remove: keys to remove from response JSON (tipical EVE keys)
    """
    initial_query_params = {}
    fields = None
    parameters = None
    page_size = None
    page_size_param = 'max_results'
    page_param = 'page'
    keys_to_remove = ('_meta', '_links')

    def get_query_params(self):
        """Construct the query parameters based on fields and parameters"""
        query_params = copy.deepcopy(self.initial_query_params)
        if self.fields:
            query_params['projection'] = json.dumps({field: 1 for field in self.fields})
        if self.parameters:
            for parameter in self.parameters:
                parameter_value = self.request.query_params.get(parameter, None)
                if parameter_value:
                    query_params[parameter] = parameter_value
        if self.page_size:
            query_params[self.page_size_param] = self.page_size
            parameter_value = self.request.query_params.get(self.page_param, None)
            if parameter_value:
                query_params[self.page_param] = parameter_value
        return query_params


class ProxyGetViewMixin():  # pylint: disable=too-few-public-methods
    """
    ProxyViewMixin with a default get method implementation. Could be customized:
    - timeout: default timeout of this request
    """
    timeout = getattr(settings, 'REQUESTS_TIMEOUT', DEFAULT_REQUEST_TIMEOUT)

    def get(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Makes a get request"""
        res = requests.get(url=self.get_url(), headers=self.get_headers(),
                           params=self.get_query_params(), timeout=self.timeout)
        custom_response = {'status': res.status_code}
        try:
            custom_response['data'] = res.json()
            if self.keys_to_remove:
                for key_to_remove in self.keys_to_remove:
                    custom_response['data'].pop(key_to_remove, None)
        except Exception:
            pass
        return Response(**custom_response)
