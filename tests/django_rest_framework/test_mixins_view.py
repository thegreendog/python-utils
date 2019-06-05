"""Mixin view tests"""
import json
from functools import partial

from rest_framework.test import APIRequestFactory
from rest_framework import status as rfstatus
from rest_framework.views import APIView
import pytest
import responses

from python_utils.django_rest_framework.mixins.view import (
    ProxyDjangoViewMixin, ProxyEveViewMixin, ProxyBaseViewMixin,
    OpenViewMixin, ProxyGetViewMixin)


class ProxyBaseViewMixinTest(ProxyBaseViewMixin, APIView):
    upstream = 'https://api2.dev.domain.com/api/v1/backend/communities/{id}/'


class ProxyEveViewMixinTest(ProxyEveViewMixin, APIView):
    initial_query_params = {
        'sort': '-created_time'
    }
    upstream = 'https://api2.dev.domain.com/api/v1/content/'
    fields = ('title', 'description', 'created_time', 'actions', 'is_published')
    page_size = 25


class ProxyDjangoViewMixinTest(ProxyDjangoViewMixin, APIView):
    parameters = ('is_published',)
    upstream = 'https://api2.dev.domain.com/api/v1/communities/?is_published=true'
    fields = ('title', 'description', 'created_time', 'actions', 'is_published')
    page_size = 25


class ProxyGetViewMixinTest(ProxyGetViewMixin, ProxyDjangoViewMixin, APIView):
    upstream = 'https://api2.dev.domain.com/api/v1/others/'
    fields = ('title', 'description', 'created_time', 'is_published')
    page_size = 25


def setup_view(view, request, *args, **kwargs):
    """
    Mimic ``as_view()``, but returns view instance.
    Use this function to get view instances on which you can run unit tests,
    by testing specific methods.
    """

    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


def get_initialised_view_object(view, endpoint, *args, **kwargs):
    factory = APIRequestFactory()

    request = factory.get(endpoint)

    initialised_view = setup_view(view(), request)
    # Transform request from WSGI Request to DRF Request
    request = initialised_view.initialize_request(request)
    initialised_view = setup_view(view(), request, *args, **kwargs)

    return initialised_view


def test_view_proxy_base_view_mixin():
    newsfeed_view = get_initialised_view_object(
        ProxyBaseViewMixinTest, ProxyBaseViewMixinTest.upstream, id='aa')

    # Check get_url method
    assert newsfeed_view.get_url() == ProxyBaseViewMixinTest.upstream.format(id='aa')

    string_format_url = ProxyBaseViewMixinTest.upstream
    ProxyBaseViewMixinTest.upstream = partial('{base_url}/{id}/'.format,
                                              base_url='https://api2.dev.domain.com/api/v1/backend/communities')
    assert newsfeed_view.get_url() == string_format_url.format(id='aa')

    with pytest.raises(ValueError) as excinfo:
        ProxyBaseViewMixinTest.upstream = 112121212
        newsfeed_view.get_url()
    assert 'upstream has to be an string or a partial' in str(excinfo.value)

    # Check get_headers method
    assert 'Accept-Language' in newsfeed_view.get_headers()


def test_view_proxy_eve_view_mixin():
    # get_query_params
    newsfeed_view = get_initialised_view_object(
        ProxyEveViewMixinTest, ProxyEveViewMixinTest.upstream)
    expected_query_params = {
        'max_results': 25,
        'projection': '{"title": 1, "description": 1, "created_time": 1, "actions": 1, "is_published": 1}',
        'sort': '-created_time'
    }
    assert newsfeed_view.get_query_params() == expected_query_params

    # With page especified
    url = ProxyEveViewMixinTest.upstream + '?page=2'
    newsfeed_view = get_initialised_view_object(
        ProxyEveViewMixinTest, url)
    expected_query_params = {
        'max_results': 25,
        'projection': '{"title": 1, "description": 1, "created_time": 1, "actions": 1, "is_published": 1}',
        'sort': '-created_time',
        'page': '2'
    }
    assert newsfeed_view.get_query_params() == expected_query_params


def test_view_proxy_django_view_mixin():
    # Check get_query_params method
    newsfeed_view = get_initialised_view_object(
        ProxyDjangoViewMixinTest, ProxyDjangoViewMixinTest.upstream)
    expected_query_params = {
        'fields': 'title,description,created_time,actions,is_published',
        'page_size': 25,
        'is_published': 'true'
    }
    assert newsfeed_view.get_query_params() == expected_query_params

    # With page especified
    url = ProxyDjangoViewMixinTest.upstream + '&page=2'
    newsfeed_view = get_initialised_view_object(
        ProxyDjangoViewMixinTest, url)
    expected_query_params = {
        'fields': 'title,description,created_time,actions,is_published',
        'page_size': 25,
        'is_published': 'true',
        'page': '2'
    }
    assert newsfeed_view.get_query_params() == expected_query_params


def test_view_proxy_get_view_mixin():
    # Check get method
    newsfeed_view = get_initialised_view_object(
        ProxyGetViewMixinTest, ProxyGetViewMixinTest.upstream)
    with responses.RequestsMock() as rsps:
        url = ProxyGetViewMixinTest.upstream
        mocked_response = {'results': [], 'count': 0, 'previous': None, 'next': None}
        rsps.add(responses.GET, url, json=mocked_response, status=rfstatus.HTTP_200_OK, content_type='application/json')

        method_call_result = newsfeed_view.get(newsfeed_view.request)
        for keys_to_remove in ProxyGetViewMixinTest.keys_to_remove:
            assert keys_to_remove not in method_call_result.data

        ProxyGetViewMixinTest.keys_to_remove = ()
        method_call_result = newsfeed_view.get(newsfeed_view.request)
        assert mocked_response == method_call_result.data
