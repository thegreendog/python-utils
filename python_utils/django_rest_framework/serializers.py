"""Reusable serializers"""
from rest_framework import serializers


class DeleteQuerySerializer(serializers.Serializer):
    """Serialize a Boolean field for deleting the element or only deactivate"""
    force = serializers.BooleanField(
        help_text="Deactivate (false) or Force delete from DB (true). Defaults to deactivate", required=False)


class AllElementsQuerySerializer(serializers.Serializer):
    """Serialize a Boolean field for returning all elements, not only active ones"""
    all_elements = serializers.BooleanField(
        help_text="Show all elements (by default, only active elements are shown)", required=False)


class BaseModelSerializer(serializers.ModelSerializer):
    """Base model serializer"""
    class Meta:
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'modified_at')


class BaseActivatableModelSerializer(BaseModelSerializer):
    """Base model serializer"""
    class Meta(BaseModelSerializer.Meta):
        fields = BaseModelSerializer.Meta.fields
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ('is_active',)
