"""Reusable serializers"""
from rest_framework import serializers


class DeleteQuerySerializer(serializers.Serializer):
    """Serialize a Boolean field for deleting the element or only deactivate"""
    force = serializers.BooleanField(help_text="Deactivate (false) or Force delete (true)", required=False)


class BaseModelSerializer(serializers.ModelSerializer):
    """Base model serializer"""
    class Meta:
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'modified_at')


class BaseActivatableModelSerializer(BaseModelSerializer):
    """Base model serializer"""
    class Meta(BaseModelSerializer.Meta):
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ('is_active',)
