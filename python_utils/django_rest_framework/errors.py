"""DRF custom errors"""
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import as_serializer_error


def as_serializer_validation_error(detail):
    """Raises a validation error with the form of a serializer validation error"""
    raise ValidationError(detail=as_serializer_error(ValidationError(detail)))
