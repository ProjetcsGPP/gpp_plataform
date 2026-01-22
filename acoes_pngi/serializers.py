"""
Serializers específicos da aplicação Ações PNGI.
Contém apenas serializers relacionados aos modelos desta aplicação.

Para serializers de User e autenticação, use common.serializers.
"""

from rest_framework import serializers
from django.db import transaction

from .models import Eixo, SituacaoAcao, VigenciaPNGI
from common.serializers import TimestampedModelSerializer, BaseModelSerializer


class EixoSerializer(TimestampedModelSerializer):
    """
    Serializer para o modelo Eixo.
    Gerencia a serialização de eixos estratégicos do PNGI.
    """
    
    class Meta:
        model = Eixo
        fields = [
            'ideixo',
            'strdescricaoeixo',
            'stralias',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['ideixo', 'created_at', 'updated_at']
    
    def validate_stralias(self, value):
        """Valida que o alias está em maiúsculas e tem no máximo 5 caracteres"""
        if not value.isupper():
            raise serializers.ValidationError("O alias deve estar em letras maiúsculas.")
        if len(value) > 5:
            raise serializers.ValidationError("O alias deve ter no máximo 5 caracteres.")
        return value
    
    def validate_strdescricaoeixo(self, value):
        """Valida que a descrição não está vazia"""
        if not value or not value.strip():
            raise serializers.ValidationError("A descrição do eixo não pode estar vazia.")
        return value.strip()


class EixoListSerializer(BaseModelSerializer):
    """
    Serializer otimizado para listagem de eixos (apenas campos essenciais).
    """
    
    class Meta:
        model = Eixo
        fields = ['ideixo', 'strdescricaoeixo', 'stralias']


class SituacaoAcaoSerializer(BaseModelSerializer):
    """
    Serializer para o modelo SituacaoAcao.
    Gerencia as situações possíveis de uma ação PNGI.
    """
    
    class Meta:
        model = SituacaoAcao
        fields = [
            'idsituacaoacao',
            'strdescricaosituacao'
        ]
        read_only_fields = ['idsituacaoacao']
    
    def validate_strdescricaosituacao(self, value):
        """Valida que a descrição está em maiúsculas e não vazia"""
        if not value or not value.strip():
            raise serializers.ValidationError("A descrição da situação não pode estar vazia.")
        return value.strip().upper()


class VigenciaPNGISerializer(TimestampedModelSerializer):
    """
    Serializer para o modelo VigenciaPNGI.
    Gerencia os períodos de vigência do PNGI.
    """
    
    class Meta:
        model = VigenciaPNGI
        fields = [
            'idvigenciapngi',
            'strdescricaovigenciapngi',
            'datiniciovigencia',
            'datfinalvigencia',
            'isvigenciaativa',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['idvigenciapngi', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        Valida que a data final é posterior à data inicial.
        """
        datiniciovigencia = data.get('datiniciovigencia')
        datfinalvigencia = data.get('datfinalvigencia')
        
        if datiniciovigencia and datfinalvigencia:
            if datfinalvigencia <= datiniciovigencia:
                raise serializers.ValidationError({
                    'datfinalvigencia': 'A data final deve ser posterior à data inicial.'
                })
        
        return data
    
    def create(self, validated_data):
        """
        Ao criar uma vigência ativa, desativa as demais.
        """
        if validated_data.get('isvigenciaativa', False):
            with transaction.atomic():
                VigenciaPNGI.objects.filter(isvigenciaativa=True).update(isvigenciaativa=False)
                return super().create(validated_data)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Ao ativar uma vigência, desativa as demais.
        """
        if validated_data.get('isvigenciaativa', False) and not instance.isvigenciaativa:
            with transaction.atomic():
                VigenciaPNGI.objects.filter(isvigenciaativa=True).update(isvigenciaativa=False)
                return super().update(instance, validated_data)
        return super().update(instance, validated_data)


class VigenciaPNGIListSerializer(BaseModelSerializer):
    """
    Serializer otimizado para listagem de vigências.
    """
    
    class Meta:
        model = VigenciaPNGI
        fields = [
            'idvigenciapngi',
            'strdescricaovigenciapngi',
            'datiniciovigencia',
            'datfinalvigencia',
            'isvigenciaativa'
        ]
