"""Reusable serializers"""
from rest_framework import serializers


class DeleteQuerySerializer(serializers.Serializer):
    force = serializers.BooleanField(help_text="Deactivate (false) or Force delete (true)", required=False)
