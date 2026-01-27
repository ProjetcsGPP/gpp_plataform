"""
Serializers para carga_org_lot
"""

from rest_framework import serializers
from .models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblOrgaoUnidade,
    TblOrganogramaJson,
    TblLotacaoVersao,
    TblLotacao,
    TblLotacaoJsonOrgao,
    TblLotacaoInconsistencia,
    TblCargaPatriarca,
    TblDetalheStatusCarga,
    TblTokenEnvioCarga,
    TblStatusProgresso,
    TblStatusCarga,
    TblTipoCarga,
    TblStatusTokenEnvioCarga,
)


# ============================================
# SERIALIZERS AUXILIARES (Tabelas de Status)
# ============================================

class TblStatusProgressoSerializer(serializers.ModelSerializer):
    """Serializer para Status Progresso"""
    class Meta:
        model = TblStatusProgresso
        fields = '__all__'


class TblStatusCargaSerializer(serializers.ModelSerializer):
    """Serializer para Status Carga"""
    class Meta:
        model = TblStatusCarga
        fields = '__all__'


class TblTipoCargaSerializer(serializers.ModelSerializer):
    """Serializer para Tipo Carga"""
    class Meta:
        model = TblTipoCarga
        fields = '__all__'


class TblStatusTokenEnvioCargaSerializer(serializers.ModelSerializer):
    """Serializer para Status Token Envio Carga"""
    class Meta:
        model = TblStatusTokenEnvioCarga
        fields = '__all__'


# ============================================
# SERIALIZERS PRINCIPAIS
# ============================================

class TblPatriarcaSerializer(serializers.ModelSerializer):
    """Serializer para Patriarca"""
    status_progresso = TblStatusProgressoSerializer(source='id_status_progresso', read_only=True)
    usuario_criacao = serializers.StringRelatedField(source='id_usuario_criacao', read_only=True)
    usuario_alteracao = serializers.StringRelatedField(source='id_usuario_alteracao', read_only=True)
    
    class Meta:
        model = TblPatriarca
        fields = '__all__'
        read_only_fields = ('id_patriarca', 'dat_criacao', 'dat_alteracao')


class TblOrganogramaVersaoSerializer(serializers.ModelSerializer):
    """Serializer para Versão de Organograma"""
    patriarca_sigla = serializers.CharField(source='id_patriarca.str_sigla_patriarca', read_only=True)
    patriarca_nome = serializers.CharField(source='id_patriarca.str_nome', read_only=True)
    
    class Meta:
        model = TblOrganogramaVersao
        fields = '__all__'
        read_only_fields = ('id_organograma_versao', 'dat_processamento')


class TblOrgaoUnidadeSerializer(serializers.ModelSerializer):
    """Serializer para Órgão/Unidade"""
    patriarca_sigla = serializers.CharField(source='id_patriarca.str_sigla_patriarca', read_only=True)
    pai_sigla = serializers.CharField(source='id_orgao_unidade_pai.str_sigla', read_only=True, allow_null=True)
    
    class Meta:
        model = TblOrgaoUnidade
        fields = '__all__'
        read_only_fields = ('id_orgao_unidade', 'dat_criacao', 'dat_alteracao')


class TblOrganogramaJsonSerializer(serializers.ModelSerializer):
    """Serializer para JSON Organograma"""
    organograma_versao_id = serializers.IntegerField(source='id_organograma_versao.id_organograma_versao', read_only=True)
    patriarca_sigla = serializers.CharField(source='id_organograma_versao.id_patriarca.str_sigla_patriarca', read_only=True)
    
    class Meta:
        model = TblOrganogramaJson
        fields = '__all__'
        read_only_fields = ('id_organograma_json', 'dat_criacao')


class TblLotacaoVersaoSerializer(serializers.ModelSerializer):
    """Serializer para Versão de Lotação"""
    patriarca_sigla = serializers.CharField(source='id_patriarca.str_sigla_patriarca', read_only=True)
    organograma_versao_id = serializers.IntegerField(source='id_organograma_versao.id_organograma_versao', read_only=True)
    
    class Meta:
        model = TblLotacaoVersao
        fields = '__all__'
        read_only_fields = ('id_lotacao_versao', 'dat_processamento')


class TblLotacaoSerializer(serializers.ModelSerializer):
    """Serializer para Lotação"""
    orgao_sigla = serializers.CharField(source='id_orgao_lotacao.str_sigla', read_only=True)
    unidade_sigla = serializers.CharField(source='id_unidade_lotacao.str_sigla', read_only=True, allow_null=True)
    
    class Meta:
        model = TblLotacao
        fields = '__all__'
        read_only_fields = ('id_lotacao', 'dat_criacao', 'dat_alteracao')


class TblLotacaoJsonOrgaoSerializer(serializers.ModelSerializer):
    """Serializer para JSON Lotação por Órgão"""
    lotacao_versao_id = serializers.IntegerField(source='id_lotacao_versao.id_lotacao_versao', read_only=True)
    organograma_versao_id = serializers.IntegerField(source='id_organograma_versao.id_organograma_versao', read_only=True)
    patriarca_sigla = serializers.CharField(source='id_patriarca.str_sigla_patriarca', read_only=True)
    orgao_sigla = serializers.CharField(source='id_orgao_lotacao.str_sigla', read_only=True)
    orgao_nome = serializers.CharField(source='id_orgao_lotacao.str_nome', read_only=True)
    
    # Estatísticas do JSON (calculadas)
    total_servidores = serializers.SerializerMethodField()
    
    class Meta:
        model = TblLotacaoJsonOrgao
        fields = '__all__'
        read_only_fields = ('id_lotacao_json_orgao', 'dat_criacao')
    
    def get_total_servidores(self, obj):
        """Extrai total de servidores do JSON"""
        try:
            if obj.js_conteudo and isinstance(obj.js_conteudo, dict):
                return len(obj.js_conteudo.get('servidores', []))
        except:
            pass
        return 0


class TblLotacaoInconsistenciaSerializer(serializers.ModelSerializer):
    """Serializer para Inconsistências de Lotação"""
    lotacao_cpf = serializers.CharField(source='id_lotacao.str_cpf', read_only=True)
    
    class Meta:
        model = TblLotacaoInconsistencia
        fields = '__all__'
        read_only_fields = ('id_inconsistencia', 'dat_registro')


class TblTokenEnvioCargaSerializer(serializers.ModelSerializer):
    """Serializer para Token Envio Carga"""
    patriarca_sigla = serializers.CharField(source='id_patriarca.str_sigla_patriarca', read_only=True)
    status_descricao = serializers.CharField(source='id_status_token_envio_carga.str_descricao', read_only=True)
    
    class Meta:
        model = TblTokenEnvioCarga
        fields = '__all__'
        read_only_fields = ('id_token_envio_carga', 'dat_data_hora_inicio')


class TblCargaPatriarcaSerializer(serializers.ModelSerializer):
    """Serializer para Carga Patriarca"""
    patriarca_sigla = serializers.CharField(source='id_patriarca.str_sigla_patriarca', read_only=True)
    status_carga = TblStatusCargaSerializer(source='id_status_carga', read_only=True)
    tipo_carga = TblTipoCargaSerializer(source='id_tipo_carga', read_only=True)
    
    class Meta:
        model = TblCargaPatriarca
        fields = '__all__'
        read_only_fields = ('id_carga_patriarca', 'dat_data_hora_inicio')


class TblDetalheStatusCargaSerializer(serializers.ModelSerializer):
    """Serializer para Detalhe Status Carga (Timeline)"""
    status_descricao = serializers.CharField(source='id_status_carga.str_descricao', read_only=True)
    status_sucesso = serializers.IntegerField(source='id_status_carga.flg_sucesso', read_only=True)
    
    class Meta:
        model = TblDetalheStatusCarga
        fields = '__all__'
        read_only_fields = ('id_detalhe_status_carga', 'dat_registro')
