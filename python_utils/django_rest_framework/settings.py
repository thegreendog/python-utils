"""Reusable setting configurations"""
from rest_framework.metadata import BaseMetadata


class NoMetaData(BaseMetadata):
    """Return no metadata in OPTION method requests"""

    def determine_metadata(self, request, view):
        return None
