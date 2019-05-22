"""Custom DRF response schema"""
from drf_yasg import openapi
from drf_yasg.inspectors.view import SwaggerAutoSchema
from drf_yasg.utils import force_real_str, is_list_view
from rest_framework import exceptions
from rest_framework.settings import api_settings


class ErrorResponseAutoSchema(SwaggerAutoSchema):
    def get_generic_error_schema(self):
        return openapi.Schema(
            'Generic API Error',
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details'),
                'code': openapi.Schema(type=openapi.TYPE_STRING, description='Error code'),
            },
            required=['detail']
        )

    def get_validation_error_schema(self):
        return openapi.Schema(
            'Validation Error',
            type=openapi.TYPE_OBJECT,
            properties={
                api_settings.NON_FIELD_ERRORS_KEY: openapi.Schema(
                    description='List of validation errors not related to any field',
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
                ),
            },
            additional_properties=openapi.Schema(
                description='A list of error messages for each field that triggered a validation error',
                type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
            )
        )

    def get_response_serializers(self):
        responses = super().get_response_serializers()
        definitions = self.components.with_scope(openapi.SCHEMA_DEFINITIONS)  # type: openapi.ReferenceResolver

        definitions.setdefault('GenericError', self.get_generic_error_schema)
        definitions.setdefault('ValidationError', self.get_validation_error_schema)
        definitions.setdefault('APIException', self.get_generic_error_schema)

        if self.get_request_serializer() or self.get_query_serializer():
            responses.setdefault(exceptions.ValidationError.status_code, openapi.Response(
                description=force_real_str(exceptions.ValidationError.default_detail),
                schema=openapi.SchemaRef(definitions, 'ValidationError')
            ))

        authenticators = self.view.get_authenticators()
        if authenticators and len(authenticators) > 0:
            responses.setdefault(exceptions.AuthenticationFailed.status_code, openapi.Response(
                description="Authentication credentials were invalid, absent or insufficient.",
                schema=openapi.SchemaRef(definitions, 'GenericError')
            ))
        if not is_list_view(self.path, self.method, self.view):
            responses.setdefault(exceptions.PermissionDenied.status_code, openapi.Response(
                description="Permission denied.",
                schema=openapi.SchemaRef(definitions, 'APIException')
            ))
            responses.setdefault(exceptions.NotFound.status_code, openapi.Response(
                description="Object does not exist or caller has insufficient permissions to access it.",
                schema=openapi.SchemaRef(definitions, 'APIException')
            ))

        return responses
