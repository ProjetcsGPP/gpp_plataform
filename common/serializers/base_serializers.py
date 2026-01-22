"""
Serializers base para herança em outras aplicações.
"""

from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Serializer base com comportamentos comuns.
    Todas as apps podem herdar deste para consistência.
    """
    
    def to_representation(self, instance):
        """
        Customiza representação para remover campos None se configurado.
        """
        representation = super().to_representation(instance)
        
        # Se configurado, remove campos None
        if getattr(self.Meta, 'remove_null_fields', False):
            representation = {
                key: value 
                for key, value in representation.items() 
                if value is not None
            }
        
        return representation


class TimestampedModelSerializer(BaseModelSerializer):
    """
    Serializer para modelos com campos de timestamp (created_at, updated_at).
    """
    created_at = serializers.DateTimeField(
        read_only=True,
        format='%Y-%m-%d %H:%M:%S',
        required=False
    )
    updated_at = serializers.DateTimeField(
        read_only=True,
        format='%Y-%m-%d %H:%M:%S',
        required=False
    )
    
    class Meta:
        abstract = True
        fields = ['created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
