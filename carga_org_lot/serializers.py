"""
Serializers específicos da aplicação Carga de Organograma e Lotação.
Contém apenas serializers relacionados aos modelos desta aplicação.

Para serializers de User e autenticação, use common.serializers.
"""

from rest_framework import serializers
from .models import Patriarca, Orgao, Lotacao  # Seus modelos
from common.serializers import TimestampedModelSerializer, BaseModelSerializer


class PatriarcaSerializer(TimestampedModelSerializer):
    """Serializer para Patriarca (modelo específico desta app)"""
    
    class Meta:
        model = Patriarca
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrgaoSerializer(BaseModelSerializer):
    """Serializer para Órgão (modelo específico desta app)"""
    
    class Meta:
        model = Orgao
        fields = '__all__'
        read_only_fields = ['id']


# ... outros serializers específicos desta app
class LotacaoSerializer(BaseModelSerializer):
    """Serializer para Lotação (modelo específico desta app)"""
    
    class Meta:
        model = Lotacao
        fields = '__all__'
        read_only_fields = ['id']

class LotacaoDetailSerializer(LotacaoSerializer):
    """Serializer detalhado para Lotação, incluindo dados relacionados."""
    
    orgao = OrgaoSerializer(read_only=True)
    patriarca = PatriarcaSerializer(read_only=True)
    
    class Meta(LotacaoSerializer.Meta):
        fields = LotacaoSerializer.Meta.fields + ['orgao', 'patriarca']
        
class LotacaoCreateUpdateSerializer(BaseModelSerializer):
    """Serializer para criação/atualização de Lotação."""
    
    class Meta:
        model = Lotacao
        fields = [
            'id',
            'nome_lotacao',
            'codigo_lotacao',
            'orgao',
            'patriarca',
            # outros campos relevantes
        ]
        read_only_fields = ['id']
    
    def validate_nome_lotacao(self, value):
        """Valida que o nome da lotação não está vazio"""
        if not value or not value.strip():
            raise serializers.ValidationError("O nome da lotação não pode estar vazio.")
        return value.strip()
    
    def validate_codigo_lotacao(self, value):
        """Valida que o código da lotação segue um formato específico"""
        if not value or not value.strip().isalnum():
            raise serializers.ValidationError("O código da lotação deve ser alfanumérico.")
        return value.strip()
    
    