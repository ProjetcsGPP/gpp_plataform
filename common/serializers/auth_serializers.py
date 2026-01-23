"""
Serializers de autenticação genéricos.
"""

from rest_framework import serializers


class PortalAuthSerializer(serializers.Serializer):
    """
    Serializer para autenticação via token do portal.
    
    Usado em endpoints de autenticação entre aplicações.
    
    Exemplo:
        POST /api/v1/acoes_pngi/auth/portal/
        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    """
    
    token = serializers.CharField(
        required=True,
        help_text="Token JWT do portal"
    )
    
    def validate_token(self, value):
        """Valida que token não está vazio"""
        if not value or not value.strip():
            raise serializers.ValidationError("Token não pode estar vazio")
        return value.strip()


class LoginSerializer(serializers.Serializer):
    """
    Serializer para login tradicional (email + senha).
    
    Exemplo:
        POST /api/v1/auth/login/
        {
            "email": "usuario@example.com",
            "password": "senha123"
        }
    """
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_email(self, value):
        """Normaliza email"""
        return value.lower().strip()


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer para mudança de senha.
    
    Exemplo:
        POST /api/v1/auth/change-password/
        {
            "old_password": "senha_antiga",
            "new_password": "senha_nova",
            "confirm_password": "senha_nova"
        }
    """
    
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        """Valida que senhas coincidem"""
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Senhas não coincidem'
            })
        
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({
                'new_password': 'Nova senha deve ser diferente da antiga'
            })
        
        return data
