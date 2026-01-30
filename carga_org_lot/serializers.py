"""
Serializers para carga_org_lot
Versão completa com validações, campos derivados e serializers otimizados
"""

from rest_framework import serializers
from django.utils import timezone
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
    """Serializer completo para Patriarca"""
    status_progresso = TblStatusProgressoSerializer(source='id_status_progresso', read_only=True)
    status_progresso_descricao = serializers.CharField(
        source='id_status_progresso.str_descricao', 
        read_only=True
    )
    usuario_criacao_nome = serializers.SerializerMethodField()
    usuario_alteracao_nome = serializers.SerializerMethodField()
    
    # Campos derivados
    tem_organograma_ativo = serializers.BooleanField(read_only=True)
    tem_lotacao_ativa = serializers.BooleanField(read_only=True)
    
    # Estatísticas
    total_organogramas = serializers.SerializerMethodField()
    total_lotacoes = serializers.SerializerMethodField()
    
    class Meta:
        model = TblPatriarca
        fields = '__all__'
        read_only_fields = (
            'id_patriarca', 
            'id_externo_patriarca',
            'dat_criacao', 
            'dat_alteracao'
        )
    
    def get_usuario_criacao_nome(self, obj):
        if obj.id_usuario_criacao:
            return str(obj.id_usuario_criacao)
        return None
    
    def get_usuario_alteracao_nome(self, obj):
        if obj.id_usuario_alteracao:
            return str(obj.id_usuario_alteracao)
        return None
    
    def get_total_organogramas(self, obj):
        return obj.versoes_organograma.count()
    
    def get_total_lotacoes(self, obj):
        return obj.versoes_lotacao.count()
    
    def validate_str_sigla_patriarca(self, value):
        """Valida e normaliza sigla"""
        if not value:
            raise serializers.ValidationError("Sigla não pode ser vazia")
        
        value = value.upper().strip()
        
        if len(value) > 20:
            raise serializers.ValidationError("Sigla deve ter no máximo 20 caracteres")
        
        return value
    
    def validate_str_nome(self, value):
        """Valida nome do patriarca"""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Nome deve ter pelo menos 3 caracteres")
        return value.strip()


class TblPatriarcaLightSerializer(serializers.ModelSerializer):
    """Serializer otimizado para listagens de Patriarca"""
    status_descricao = serializers.CharField(
        source='id_status_progresso.str_descricao', 
        read_only=True
    )
    
    class Meta:
        model = TblPatriarca
        fields = [
            'id_patriarca',
            'str_sigla_patriarca',
            'str_nome',
            'status_descricao',
        ]


class TblOrganogramaVersaoSerializer(serializers.ModelSerializer):
    """Serializer completo para Versão de Organograma"""
    patriarca_sigla = serializers.CharField(
        source='id_patriarca.str_sigla_patriarca', 
        read_only=True
    )
    patriarca_nome = serializers.CharField(
        source='id_patriarca.str_nome', 
        read_only=True
    )
    
    # Propriedades calculadas
    total_orgaos = serializers.IntegerField(read_only=True)
    sucesso = serializers.BooleanField(read_only=True)
    
    # Estatísticas
    total_orgaos_ativos = serializers.SerializerMethodField()
    total_lotacoes = serializers.SerializerMethodField()
    
    class Meta:
        model = TblOrganogramaVersao
        fields = '__all__'
        read_only_fields = ('id_organograma_versao', 'dat_processamento')
    
    def get_total_orgaos_ativos(self, obj):
        return obj.orgaos_unidades.filter(flg_ativo=True).count()
    
    def get_total_lotacoes(self, obj):
        return obj.versoes_lotacao.count()
    
    def validate(self, attrs):
        """Validações customizadas"""
        # Garante que apenas uma versão está ativa por patriarca
        if attrs.get('flg_ativo') and self.instance is None:
            patriarca = attrs.get('id_patriarca')
            if patriarca and TblOrganogramaVersao.objects.filter(
                id_patriarca=patriarca, 
                flg_ativo=True
            ).exists():
                raise serializers.ValidationError(
                    "Já existe uma versão ativa para este patriarca. "
                    "Desative a versão atual antes de ativar outra."
                )
        
        return attrs


class TblOrganogramaVersaoLightSerializer(serializers.ModelSerializer):
    """Serializer otimizado para listagens de Organograma"""
    patriarca_sigla = serializers.CharField(
        source='id_patriarca.str_sigla_patriarca', 
        read_only=True
    )
    total_orgaos = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = TblOrganogramaVersao
        fields = [
            'id_organograma_versao',
            'patriarca_sigla',
            'str_origem',
            'dat_processamento',
            'str_status_processamento',
            'flg_ativo',
            'total_orgaos',
        ]


class TblOrgaoUnidadeSerializer(serializers.ModelSerializer):
    """Serializer completo para Órgão/Unidade"""
    patriarca_sigla = serializers.CharField(
        source='id_patriarca.str_sigla_patriarca', 
        read_only=True
    )
    pai_sigla = serializers.CharField(
        source='id_orgao_unidade_pai.str_sigla', 
        read_only=True, 
        allow_null=True
    )
    pai_nome = serializers.CharField(
        source='id_orgao_unidade_pai.str_nome', 
        read_only=True, 
        allow_null=True
    )
    
    # Propriedades calculadas
    eh_raiz = serializers.BooleanField(read_only=True)
    total_filhos = serializers.IntegerField(read_only=True)
    caminho_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = TblOrgaoUnidade
        fields = '__all__'
        read_only_fields = ('id_orgao_unidade', 'dat_criacao', 'dat_alteracao')
    
    def validate(self, attrs):
        """Validações de hierarquia"""
        pai = attrs.get('id_orgao_unidade_pai')
        
        # Não pode ser pai de si mesmo
        if self.instance and pai and pai.id == self.instance.id:
            raise serializers.ValidationError(
                "Um órgão/unidade não pode ser pai de si mesmo"
            )
        
        # Verifica se pai pertence ao mesmo patriarca e versão
        if pai:
            patriarca = attrs.get('id_patriarca', getattr(self.instance, 'id_patriarca', None))
            versao = attrs.get('id_organograma_versao', getattr(self.instance, 'id_organograma_versao', None))
            
            if pai.id_patriarca != patriarca:
                raise serializers.ValidationError(
                    "O órgão/unidade pai deve pertencer ao mesmo patriarca"
                )
            
            if pai.id_organograma_versao != versao:
                raise serializers.ValidationError(
                    "O órgão/unidade pai deve pertencer à mesma versão do organograma"
                )
        
        return attrs


class TblOrgaoUnidadeLightSerializer(serializers.ModelSerializer):
    """Serializer otimizado para listagens de Órgão/Unidade"""
    patriarca_sigla = serializers.CharField(
        source='id_patriarca.str_sigla_patriarca', 
        read_only=True
    )
    pai_sigla = serializers.CharField(
        source='id_orgao_unidade_pai.str_sigla', 
        read_only=True, 
        allow_null=True
    )
    
    class Meta:
        model = TblOrgaoUnidade
        fields = [
            'id_orgao_unidade',
            'str_sigla',
            'str_nome',
            'patriarca_sigla',
            'pai_sigla',
            'int_nivel_hierarquia',
            'flg_ativo',
        ]


class TblOrgaoUnidadeTreeSerializer(serializers.ModelSerializer):
    """Serializer recursivo para árvore hierárquica de órgãos"""
    filhos = serializers.SerializerMethodField()
    
    class Meta:
        model = TblOrgaoUnidade
        fields = [
            'id_orgao_unidade',
            'str_sigla',
            'str_nome',
            'int_nivel_hierarquia',
            'flg_ativo',
            'filhos',
        ]
    
    def get_filhos(self, obj):
        """Serializa filhos recursivamente"""
        filhos = obj.unidades_filhas.filter(flg_ativo=True).order_by('str_numero_hierarquia')
        return TblOrgaoUnidadeTreeSerializer(filhos, many=True).data


class TblOrganogramaJsonSerializer(serializers.ModelSerializer):
    """Serializer para JSON Organograma"""
    organograma_versao_id = serializers.IntegerField(
        source='id_organograma_versao.id_organograma_versao', 
        read_only=True
    )
    patriarca_sigla = serializers.CharField(
        source='id_organograma_versao.id_patriarca.str_sigla_patriarca', 
        read_only=True
    )
    foi_enviado = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = TblOrganogramaJson
        fields = '__all__'
        read_only_fields = ('id_organograma_json', 'dat_criacao')


class TblLotacaoVersaoSerializer(serializers.ModelSerializer):
    """Serializer completo para Versão de Lotação"""
    patriarca_sigla = serializers.CharField(
        source='id_patriarca.str_sigla_patriarca', 
        read_only=True
    )
    organograma_versao_id = serializers.IntegerField(
        source='id_organograma_versao.id_organograma_versao', 
        read_only=True
    )
    
    # Propriedades calculadas
    total_lotacoes = serializers.IntegerField(read_only=True)
    total_validas = serializers.IntegerField(read_only=True)
    total_invalidas = serializers.IntegerField(read_only=True)
    
    # Taxa de sucesso
    taxa_sucesso = serializers.SerializerMethodField()
    
    class Meta:
        model = TblLotacaoVersao
        fields = '__all__'
        read_only_fields = ('id_lotacao_versao', 'dat_processamento')
    
    def get_taxa_sucesso(self, obj):
        """Calcula taxa de sucesso das validações"""
        total = obj.total_lotacoes
        if total == 0:
            return 0.0
        return round((obj.total_validas / total) * 100, 2)


class TblLotacaoVersaoLightSerializer(serializers.ModelSerializer):
    """Serializer otimizado para listagens de Lotação"""
    patriarca_sigla = serializers.CharField(
        source='id_patriarca.str_sigla_patriarca', 
        read_only=True
    )
    total_lotacoes = serializers.IntegerField(read_only=True)
    total_validas = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = TblLotacaoVersao
        fields = [
            'id_lotacao_versao',
            'patriarca_sigla',
            'str_origem',
            'dat_processamento',
            'str_status_processamento',
            'flg_ativo',
            'total_lotacoes',
            'total_validas',
        ]


class TblLotacaoSerializer(serializers.ModelSerializer):
    """Serializer completo para Lotação"""
    orgao_sigla = serializers.CharField(
        source='id_orgao_lotacao.str_sigla', 
        read_only=True
    )
    orgao_nome = serializers.CharField(
        source='id_orgao_lotacao.str_nome', 
        read_only=True
    )
    unidade_sigla = serializers.CharField(
        source='id_unidade_lotacao.str_sigla', 
        read_only=True, 
        allow_null=True
    )
    unidade_nome = serializers.CharField(
        source='id_unidade_lotacao.str_nome', 
        read_only=True, 
        allow_null=True
    )
    
    # Propriedades
    tem_inconsistencias = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = TblLotacao
        fields = '__all__'
        read_only_fields = ('id_lotacao', 'dat_criacao', 'dat_alteracao')
    
    def validate_str_cpf(self, value):
        """Valida formato do CPF"""
        import re
        
        # Remove caracteres não numéricos
        cpf = re.sub(r'\D', '', value)
        
        if len(cpf) != 11:
            raise serializers.ValidationError("CPF deve conter 11 dígitos")
        
        # Formata CPF
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


class TblLotacaoLightSerializer(serializers.ModelSerializer):
    """Serializer otimizado para listagens de Lotação"""
    orgao_sigla = serializers.CharField(
        source='id_orgao_lotacao.str_sigla', 
        read_only=True
    )
    
    class Meta:
        model = TblLotacao
        fields = [
            'id_lotacao',
            'str_cpf',
            'orgao_sigla',
            'str_cargo_normalizado',
            'flg_valido',
        ]


class TblLotacaoJsonOrgaoSerializer(serializers.ModelSerializer):
    """Serializer para JSON Lotação por Órgão"""
    lotacao_versao_id = serializers.IntegerField(
        source='id_lotacao_versao.id_lotacao_versao', 
        read_only=True
    )
    organograma_versao_id = serializers.IntegerField(
        source='id_organograma_versao.id_organograma_versao', 
        read_only=True
    )
    patriarca_sigla = serializers.CharField(
        source='id_patriarca.str_sigla_patriarca', 
        read_only=True
    )
    orgao_sigla = serializers.CharField(
        source='id_orgao_lotacao.str_sigla', 
        read_only=True
    )
    orgao_nome = serializers.CharField(
        source='id_orgao_lotacao.str_nome', 
        read_only=True
    )
    
    # Estatísticas do JSON (calculadas)
    total_servidores = serializers.SerializerMethodField()
    foi_enviado = serializers.BooleanField(read_only=True)
    
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
    lotacao_cpf = serializers.CharField(
        source='id_lotacao.str_cpf', 
        read_only=True
    )
    lotacao_orgao = serializers.CharField(
        source='id_lotacao.id_orgao_lotacao.str_sigla', 
        read_only=True
    )
    
    class Meta:
        model = TblLotacaoInconsistencia
        fields = '__all__'
        read_only_fields = ('id_inconsistencia', 'dat_registro')


class TblTokenEnvioCargaSerializer(serializers.ModelSerializer):
    """Serializer para Token Envio Carga"""
    patriarca_sigla = serializers.CharField(
        source='id_patriarca.str_sigla_patriarca', 
        read_only=True
    )
    status_descricao = serializers.CharField(
        source='id_status_token_envio_carga.str_descricao', 
        read_only=True
    )
    ativo = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = TblTokenEnvioCarga
        fields = '__all__'
        read_only_fields = ('id_token_envio_carga', 'dat_data_hora_inicio')


class TblCargaPatriarcaSerializer(serializers.ModelSerializer):
    """Serializer para Carga Patriarca"""
    patriarca_sigla = serializers.CharField(
        source='id_patriarca.str_sigla_patriarca', 
        read_only=True
    )
    status_carga = TblStatusCargaSerializer(
        source='id_status_carga', 
        read_only=True
    )
    tipo_carga = TblTipoCargaSerializer(
        source='id_tipo_carga', 
        read_only=True
    )
    em_andamento = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = TblCargaPatriarca
        fields = '__all__'
        read_only_fields = ('id_carga_patriarca', 'dat_data_hora_inicio')


class TblDetalheStatusCargaSerializer(serializers.ModelSerializer):
    """Serializer para Detalhe Status Carga (Timeline)"""
    status_descricao = serializers.CharField(
        source='id_status_carga.str_descricao', 
        read_only=True
    )
    status_sucesso = serializers.IntegerField(
        source='id_status_carga.flg_sucesso', 
        read_only=True
    )
    
    class Meta:
        model = TblDetalheStatusCarga
        fields = '__all__'
        read_only_fields = ('id_detalhe_status_carga', 'dat_registro')
