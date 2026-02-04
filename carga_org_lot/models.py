# carga_org_lot/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

User = get_user_model()


class TblStatusProgresso(models.Model):
    """Status de progresso da carga"""
    id_status_progresso = models.SmallIntegerField(primary_key=True, db_column='idstatusprogresso')
    str_descricao = models.CharField(max_length=100, db_column='strdescricao')

    class Meta:
        db_table = '"carga_org_lot"."tblstatusprogresso"'
        managed = True
        verbose_name = 'Status Progresso'
        verbose_name_plural = 'Status Progresso'

    def __str__(self):
        return self.str_descricao


class TblPatriarca(models.Model):
    """Patriarca - Órgão principal para organograma e lotação"""
    id_patriarca = models.BigAutoField(primary_key=True, db_column='idpatriarca')
    id_externo_patriarca = models.UUIDField(
        unique=True, 
        db_column='idexternopatriarca',
        help_text='UUID do patriarca no sistema PRODEST'
    )
    str_sigla_patriarca = models.CharField(
        max_length=20, 
        db_column='strsiglapatriarca',
        help_text='Sigla do patriarca (ex: SEGER, SEDU)'
    )
    str_nome = models.CharField(
        max_length=255, 
        db_column='strnome',
        help_text='Nome completo do patriarca'
    )
    id_status_progresso = models.ForeignKey(
        TblStatusProgresso,
        on_delete=models.PROTECT,
        db_column='idstatusprogresso',
        related_name='patriarcas'
    )
    dat_criacao = models.DateTimeField(
        db_column='datcriacao',
        default=timezone.now
    )
    id_usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='patriarcas_criados',
        db_column='idusuariocriacao'
    )
    dat_alteracao = models.DateTimeField(
        null=True, 
        blank=True, 
        db_column='datalteracao'
    )
    id_usuario_alteracao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='patriarcas_alterados',
        db_column='idusuarioalteracao'
    )

    class Meta:
        db_table = '"carga_org_lot"."tblpatriarca"'
        managed = True
        verbose_name = 'Patriarca'
        verbose_name_plural = 'Patriarcas'
        ordering = ['str_sigla_patriarca']

    def __str__(self):
        return f"{self.str_sigla_patriarca} - {self.str_nome}"
    
    def clean(self):
        """Validações customizadas"""
        if self.str_sigla_patriarca:
            self.str_sigla_patriarca = self.str_sigla_patriarca.upper().strip()
        
        if self.str_nome:
            self.str_nome = self.str_nome.strip()
            if len(self.str_nome) < 3:
                raise ValidationError({'str_nome': 'Nome deve ter pelo menos 3 caracteres'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def tem_organograma_ativo(self):
        """Verifica se possui organograma ativo"""
        return self.versoes_organograma.filter(flg_ativo=True).exists()
    
    @property
    def tem_lotacao_ativa(self):
        """Verifica se possui lotação ativa"""
        return self.versoes_lotacao.filter(flg_ativo=True).exists()


class TblOrganogramaVersao(models.Model):
    """Versão do organograma"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PROCESSANDO', 'Processando'),
        ('SUCESSO', 'Sucesso'),
        ('ERRO', 'Erro'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    id_organograma_versao = models.BigAutoField(primary_key=True, db_column='idorganogramaversao')
    id_patriarca = models.ForeignKey(
        TblPatriarca,
        on_delete=models.CASCADE,
        db_column='idpatriarca',
        related_name='versoes_organograma'
    )
    str_origem = models.CharField(
        max_length=50, 
        db_column='strorigem',
        help_text='Origem dos dados (API, UPLOAD, MANUAL)'
    )
    str_tipo_arquivo_original = models.CharField(
        max_length=20, 
        null=True, 
        blank=True, 
        db_column='strtipoarquivooriginal'
    )
    str_nome_arquivo_original = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        db_column='strnomearquivooriginal'
    )
    dat_processamento = models.DateTimeField(
        db_column='datprocessamento',
        default=timezone.now
    )
    str_status_processamento = models.CharField(
        max_length=30, 
        db_column='strstatusprocessamento',
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    str_mensagem_processamento = models.TextField(
        null=True, 
        blank=True, 
        db_column='strmensagemprocessamento'
    )
    flg_ativo = models.BooleanField(
        db_column='flgativo',
        default=False,
        help_text='Indica se esta é a versão ativa'
    )

    class Meta:
        db_table = '"carga_org_lot"."tblorganogramaversao"'
        managed = True
        verbose_name = 'Versão de Organograma'
        verbose_name_plural = 'Versões de Organograma'
        ordering = ['-id_organograma_versao']

    def __str__(self):
        return f"Organograma v{self.id_organograma_versao} - {self.id_patriarca.str_sigla_patriarca}"
    
    @property
    def total_orgaos(self):
        """Retorna total de órgãos/unidades nesta versão"""
        return self.tblorgaounidade_set.count()
    
    @property
    def sucesso(self):
        """Verifica se processamento foi bem-sucedido"""
        return self.str_status_processamento == 'SUCESSO'


class TblOrgaoUnidade(models.Model):
    """Órgãos e Unidades organizacionais"""
    id_orgao_unidade = models.BigAutoField(primary_key=True, db_column='idorgaounidade')
    id_organograma_versao = models.ForeignKey(
        TblOrganogramaVersao,
        on_delete=models.RESTRICT,
        db_column='idorganogramaversao',
        related_name='orgaos_unidades'
    )
    id_patriarca = models.ForeignKey(
        TblPatriarca,
        on_delete=models.RESTRICT,
        db_column='idpatriarca',
        related_name='orgaos_unidades'
    )
    str_nome = models.CharField(
        max_length=255, 
        db_column='strnome',
        help_text='Nome completo do órgão/unidade'
    )
    str_sigla = models.CharField(
        max_length=50, 
        db_column='strsigla',
        help_text='Sigla do órgão/unidade'
    )
    id_orgao_unidade_pai = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='idorgaounidadepai',
        related_name='unidades_filhas'
    )
    str_numero_hierarquia = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        db_column='strnumerohierarquia',
        help_text='Número hierárquico (ex: 1.2.3)'
    )
    int_nivel_hierarquia = models.IntegerField(
        null=True, 
        blank=True, 
        db_column='intnivelhierarquia',
        help_text='Nível na hierarquia (0 = raiz)'
    )
    flg_ativo = models.BooleanField(
        db_column='flgativo',
        default=True
    )
    dat_criacao = models.DateTimeField(
        db_column='datcriacao',
        default=timezone.now
    )
    id_usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='orgaos_criados',
        db_column='idusuariocriacao'
    )
    dat_alteracao = models.DateTimeField(
        null=True, 
        blank=True, 
        db_column='datalteracao'
    )
    id_usuario_alteracao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='orgaos_alterados',
        db_column='idusuarioalteracao'
    )

    class Meta:
        db_table = '"carga_org_lot"."tblorgaounidade"'
        managed = True
        verbose_name = 'Órgão/Unidade'
        verbose_name_plural = 'Órgãos/Unidades'
        ordering = ['str_numero_hierarquia']

    def __str__(self):
        return f"{self.str_sigla} - {self.str_nome}"
    
    @property
    def eh_raiz(self):
        """Verifica se é um órgão raiz"""
        return self.id_orgao_unidade_pai is None
    
    @property
    def total_filhos(self):
        """Retorna total de unidades filhas"""
        return self.unidades_filhas.count()
    
    @property
    def caminho_completo(self):
        """Retorna caminho hierárquico completo"""
        caminho = [self.str_sigla]
        pai = self.id_orgao_unidade_pai
        while pai:
            caminho.insert(0, pai.str_sigla)
            pai = pai.id_orgao_unidade_pai
        return ' > '.join(caminho)


class TblOrganogramaJson(models.Model):
    """JSON do organograma para envio à API"""
    id_organograma_json = models.BigAutoField(primary_key=True, db_column='idorganogramajson')
    id_organograma_versao = models.OneToOneField(
        TblOrganogramaVersao,
        on_delete=models.CASCADE,
        db_column='idorganogramaversao',
        related_name='json_organograma'
    )
    js_conteudo = models.JSONField(db_column='jsconteudo')
    dat_criacao = models.DateTimeField(
        db_column='datcriacao',
        default=timezone.now
    )
    dat_envio_api = models.DateTimeField(
        null=True, 
        blank=True, 
        db_column='datenvioapi'
    )
    str_status_envio = models.CharField(
        max_length=30, 
        null=True, 
        blank=True, 
        db_column='strstatusenvio'
    )
    str_mensagem_retorno = models.TextField(
        null=True, 
        blank=True, 
        db_column='strmensagemretorno'
    )

    class Meta:
        db_table = '"carga_org_lot"."tblorganogramajson"'
        managed = True
        verbose_name = 'JSON Organograma'
        verbose_name_plural = 'JSONs Organograma'

    def __str__(self):
        return f"JSON Organograma v{self.id_organograma_versao_id}"
    
    @property
    def foi_enviado(self):
        """Verifica se já foi enviado para API"""
        return self.dat_envio_api is not None


class TblLotacaoVersao(models.Model):
    """Versão da lotação"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PROCESSANDO', 'Processando'),
        ('SUCESSO', 'Sucesso'),
        ('ERRO', 'Erro'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    id_lotacao_versao = models.BigAutoField(primary_key=True, db_column='idlotacaoversao')
    id_patriarca = models.ForeignKey(
        TblPatriarca,
        on_delete=models.CASCADE,
        db_column='idpatriarca',
        related_name='versoes_lotacao'
    )
    id_organograma_versao = models.ForeignKey(
        TblOrganogramaVersao,
        on_delete=models.CASCADE,
        db_column='idorganogramaversao',
        related_name='versoes_lotacao'
    )
    str_origem = models.CharField(
        max_length=50, 
        db_column='strorigem'
    )
    str_tipo_arquivo_original = models.CharField(
        max_length=20, 
        null=True, 
        blank=True, 
        db_column='strtipoarquivooriginal'
    )
    str_nome_arquivo_original = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        db_column='strnomearquivooriginal'
    )
    dat_processamento = models.DateTimeField(
        db_column='datprocessamento',
        default=timezone.now
    )
    str_status_processamento = models.CharField(
        max_length=30, 
        db_column='strstatusprocessamento',
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    str_mensagem_processamento = models.TextField(
        null=True, 
        blank=True, 
        db_column='strmensagemprocessamento'
    )
    flg_ativo = models.BooleanField(
        db_column='flgativo',
        default=False
    )

    class Meta:
        db_table = '"carga_org_lot"."tbllotacaoversao"'
        managed = True
        verbose_name = 'Versão de Lotação'
        verbose_name_plural = 'Versões de Lotação'
        ordering = ['-id_lotacao_versao']

    def __str__(self):
        return f"Lotação v{self.id_lotacao_versao} - {self.id_patriarca.str_sigla_patriarca}"
    
    @property
    def total_lotacoes(self):
        """Retorna total de lotações nesta versão"""
        return self.tbllotacao_set.count()
    
    @property
    def total_validas(self):
        """Retorna total de lotações válidas"""
        return self.tbllotacao_set.filter(flg_valido=True).count()
    
    @property
    def total_invalidas(self):
        """Retorna total de lotações inválidas"""
        return self.tbllotacao_set.filter(flg_valido=False).count()


class TblLotacao(models.Model):
    """Lotação de servidores"""
    id_lotacao = models.BigAutoField(primary_key=True, db_column='idlotacao')
    id_lotacao_versao = models.ForeignKey(
        TblLotacaoVersao,
        on_delete=models.CASCADE,
        db_column='idlotacaoversao',
        related_name='lotacoes'
    )
    id_organograma_versao = models.ForeignKey(
        TblOrganogramaVersao,
        on_delete=models.CASCADE,
        db_column='idorganogramaversao',
        related_name='lotacoes'
    )
    id_patriarca = models.ForeignKey(
        TblPatriarca,
        on_delete=models.CASCADE,
        db_column='idpatriarca',
        related_name='lotacoes'
    )
    id_orgao_lotacao = models.ForeignKey(
        TblOrgaoUnidade,
        on_delete=models.CASCADE,
        related_name='lotacoes_orgao',
        db_column='idorgaolotacao'
    )
    id_unidade_lotacao = models.ForeignKey(
        TblOrgaoUnidade,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='lotacoes_unidade',
        db_column='idunidadelotacao'
    )
    str_cpf = models.CharField(
        max_length=14, 
        db_column='strcpf',
        help_text='CPF do servidor'
    )
    str_cargo_original = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        db_column='strcargooriginal'
    )
    str_cargo_normalizado = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        db_column='strcargonormalizado'
    )
    flg_valido = models.BooleanField(
        db_column='flgvalido',
        default=True
    )
    str_erros_validacao = models.TextField(
        null=True, 
        blank=True, 
        db_column='strerrosvalidacao'
    )
    dat_referencia = models.DateField(
        null=True, 
        blank=True, 
        db_column='datreferencia'
    )
    dat_criacao = models.DateTimeField(
        db_column='datcriacao',
        default=timezone.now
    )
    id_usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='lotacoes_criadas',
        db_column='idusuariocriacao'
    )
    dat_alteracao = models.DateTimeField(
        null=True, 
        blank=True, 
        db_column='datalteracao'
    )
    id_usuario_alteracao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='lotacoes_alteradas',
        db_column='idusuarioalteracao'
    )

    class Meta:
        db_table = '"carga_org_lot"."tbllotacao"'
        managed = True
        verbose_name = 'Lotação'
        verbose_name_plural = 'Lotações'
        ordering = ['str_cpf']

    def __str__(self):
        return f"Lotação {self.str_cpf} - {self.id_orgao_lotacao.str_sigla}"
    
    @property
    def tem_inconsistencias(self):
        """Verifica se possui inconsistências"""
        return self.tbllotacaoinconsistencia_set.exists()


class TblLotacaoJsonOrgao(models.Model):
    """JSON de lotação por órgão para envio à API"""
    id_lotacao_json_orgao = models.BigAutoField(primary_key=True, db_column='idlotacaojsonorgao')
    id_lotacao_versao = models.ForeignKey(
        TblLotacaoVersao,
        on_delete=models.CASCADE,
        db_column='idlotacaoversao',
        related_name='jsons_orgao'
    )
    id_organograma_versao = models.ForeignKey(
        TblOrganogramaVersao,
        on_delete=models.CASCADE,
        db_column='idorganogramaversao',
        related_name='jsons_lotacao'
    )
    id_patriarca = models.ForeignKey(
        TblPatriarca,
        on_delete=models.CASCADE,
        db_column='idpatriarca',
        related_name='jsons_lotacao'
    )
    id_orgao_lotacao = models.ForeignKey(
        TblOrgaoUnidade,
        on_delete=models.CASCADE,
        db_column='idorgaolotacao',
        related_name='jsons_lotacao'
    )
    js_conteudo = models.JSONField(db_column='jsconteudo')
    dat_criacao = models.DateTimeField(
        db_column='datcriacao',
        default=timezone.now
    )
    dat_envio_api = models.DateTimeField(
        null=True, 
        blank=True, 
        db_column='datenvioapi'
    )
    str_status_envio = models.CharField(
        max_length=30, 
        null=True, 
        blank=True, 
        db_column='strstatusenvio'
    )
    str_mensagem_retorno = models.TextField(
        null=True, 
        blank=True, 
        db_column='strmensagemretorno'
    )

    class Meta:
        db_table = '"carga_org_lot"."tbllotacaojsonorgao"'
        managed = True
        verbose_name = 'JSON Lotação por Órgão'
        verbose_name_plural = 'JSONs Lotação por Órgão'

    def __str__(self):
        return f"JSON Lotação {self.id_orgao_lotacao.str_sigla}"
    
    @property
    def foi_enviado(self):
        """Verifica se já foi enviado para API"""
        return self.dat_envio_api is not None


class TblLotacaoInconsistencia(models.Model):
    """Inconsistências encontradas na lotação"""
    id_inconsistencia = models.BigAutoField(primary_key=True, db_column='idinconsistencia')
    id_lotacao = models.ForeignKey(
        TblLotacao,
        on_delete=models.CASCADE,
        db_column='idlotacao',
        related_name='inconsistencias'
    )
    str_tipo = models.CharField(
        max_length=100, 
        db_column='strtipo'
    )
    str_detalhe = models.TextField(db_column='strdetalhe')
    dat_registro = models.DateTimeField(
        db_column='datregistro',
        default=timezone.now
    )

    class Meta:
        db_table = '"carga_org_lot"."tbllotacaoinconsistencia"'
        managed = True
        verbose_name = 'Inconsistência de Lotação'
        verbose_name_plural = 'Inconsistências de Lotação'
        ordering = ['-dat_registro']

    def __str__(self):
        return f"{self.str_tipo} - Lotação {self.id_lotacao_id}"


class TblStatusTokenEnvioCarga(models.Model):
    """Status do token de envio de carga"""
    id_status_token_envio_carga = models.SmallIntegerField(primary_key=True, db_column='idstatustokenenviocarga')
    str_descricao = models.CharField(max_length=100, db_column='strdescricao')

    class Meta:
        db_table = '"carga_org_lot"."tblstatustokenenviocarga"'
        managed = True
        verbose_name = 'Status Token Envio Carga'
        verbose_name_plural = 'Status Token Envio Carga'

    def __str__(self):
        return self.str_descricao


class TblTokenEnvioCarga(models.Model):
    """Token de envio de carga"""
    id_token_envio_carga = models.BigAutoField(primary_key=True, db_column='idtokenenviocarga')
    id_patriarca = models.ForeignKey(
        TblPatriarca,
        on_delete=models.CASCADE,
        db_column='idpatriarca',
        related_name='tokens_envio'
    )
    id_status_token_envio_carga = models.ForeignKey(
        TblStatusTokenEnvioCarga,
        on_delete=models.PROTECT,
        db_column='idstatustokenenviocarga',
        related_name='tokens'
    )
    str_token_retorno = models.CharField(
        max_length=1000, 
        db_column='strtokenretorno'
    )
    dat_data_hora_inicio = models.DateTimeField(
        db_column='datdatahorainicio',
        default=timezone.now
    )
    dat_data_hora_fim = models.DateTimeField(
        null=True, 
        blank=True, 
        db_column='datdatahorafim'
    )

    class Meta:
        db_table = '"carga_org_lot"."tbltokenenviocarga"'
        managed = True
        verbose_name = 'Token Envio Carga'
        verbose_name_plural = 'Tokens Envio Carga'
        ordering = ['-dat_data_hora_inicio']

    def __str__(self):
        return f"Token {self.id_token_envio_carga} - {self.id_patriarca.str_sigla_patriarca}"
    
    @property
    def ativo(self):
        """Verifica se token ainda está ativo"""
        return self.dat_data_hora_fim is None


class TblStatusCarga(models.Model):
    """Status da carga"""
    id_status_carga = models.SmallIntegerField(primary_key=True, db_column='idstatuscarga')
    str_descricao = models.CharField(max_length=150, db_column='strdescricao')
    flg_sucesso = models.IntegerField(db_column='flgsucesso')

    class Meta:
        db_table = '"carga_org_lot"."tblstatuscarga"'
        managed = True
        verbose_name = 'Status Carga'
        verbose_name_plural = 'Status Carga'

    def __str__(self):
        return self.str_descricao


class TblTipoCarga(models.Model):
    """Tipo de carga"""
    id_tipo_carga = models.SmallIntegerField(primary_key=True, db_column='idtipocarga')
    str_descricao = models.CharField(max_length=100, db_column='strdescricao')

    class Meta:
        db_table = '"carga_org_lot"."tbltipocarga"'
        managed = True
        verbose_name = 'Tipo Carga'
        verbose_name_plural = 'Tipos Carga'

    def __str__(self):
        return self.str_descricao


class TblCargaPatriarca(models.Model):
    """Carga do patriarca"""
    id_carga_patriarca = models.BigAutoField(primary_key=True, db_column='idcargapatriarca')
    id_patriarca = models.ForeignKey(
        TblPatriarca,
        on_delete=models.CASCADE,
        db_column='idpatriarca',
        related_name='cargas'
    )
    id_token_envio_carga = models.ForeignKey(
        TblTokenEnvioCarga,
        on_delete=models.CASCADE,
        db_column='idtokenenviocarga',
        related_name='cargas'
    )
    id_status_carga = models.ForeignKey(
        TblStatusCarga,
        on_delete=models.PROTECT,
        db_column='idstatuscarga',
        related_name='cargas'
    )
    id_tipo_carga = models.ForeignKey(
        TblTipoCarga,
        on_delete=models.PROTECT,
        db_column='idtipocarga',
        related_name='cargas'
    )
    str_mensagem_retorno = models.TextField(
        null=True, 
        blank=True, 
        db_column='strmensagemretorno'
    )
    dat_data_hora_inicio = models.DateTimeField(
        db_column='datdatahorainicio',
        default=timezone.now
    )
    dat_data_hora_fim = models.DateTimeField(
        null=True, 
        blank=True, 
        db_column='datdatahorafim'
    )

    class Meta:
        db_table = '"carga_org_lot"."tblcargapatriarca"'
        managed = True
        verbose_name = 'Carga Patriarca'
        verbose_name_plural = 'Cargas Patriarca'
        ordering = ['-dat_data_hora_inicio']

    def __str__(self):
        return f"Carga {self.id_carga_patriarca} - {self.id_tipo_carga.str_descricao}"
    
    @property
    def em_andamento(self):
        """Verifica se carga está em andamento"""
        return self.dat_data_hora_fim is None


class TblDetalheStatusCarga(models.Model):
    """Detalhes do status da carga (timeline)"""
    id_detalhe_status_carga = models.BigAutoField(primary_key=True, db_column='iddetalhestatuscarga')
    id_carga_patriarca = models.ForeignKey(
        TblCargaPatriarca,
        on_delete=models.CASCADE,
        db_column='idcargapatriarca',
        related_name='detalhes_status'
    )
    id_status_carga = models.ForeignKey(
        TblStatusCarga,
        on_delete=models.PROTECT,
        db_column='idstatuscarga',
        related_name='detalhes'
    )
    dat_registro = models.DateTimeField(
        db_column='datregistro',
        default=timezone.now
    )
    str_mensagem = models.TextField(
        null=True, 
        blank=True, 
        db_column='strmensagem'
    )

    class Meta:
        db_table = '"carga_org_lot"."tbldetalhestatuscarga"'
        managed = True
        verbose_name = 'Detalhe Status Carga'
        verbose_name_plural = 'Detalhes Status Carga'
        ordering = ['dat_registro']

    def __str__(self):
        return f"Detalhe {self.id_detalhe_status_carga} - {self.id_status_carga.str_descricao}"
