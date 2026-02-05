from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings


class Eixo(models.Model):
    """
    Eixos estratégicos do PNGI
    """
    ideixo = models.AutoField(primary_key=True, db_column='ideixo')
    strdescricaoeixo = models.CharField(max_length=100, db_column='strdescricaoeixo')
    stralias = models.CharField(max_length=5, unique=True, db_column='stralias')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'acoes_pngi.tbleixos'
        managed = True
        verbose_name = 'Eixo'
        verbose_name_plural = 'Eixos'
        ordering = ['stralias']

    def __str__(self):
        return f'{self.stralias} - {self.strdescricaoeixo}'

    def clean(self):
        if self.stralias:
            self.stralias = self.stralias.upper()


class SituacaoAcao(models.Model):
    """
    Situações possíveis de uma ação PNGI
    """
    idsituacaoacao = models.AutoField(primary_key=True, db_column='idsituacaoacao')
    strdescricaosituacao = models.CharField(
        max_length=15, 
        unique=True, 
        db_column='strdescricaosituacao'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'acoes_pngi.tblsituacaoacao'
        managed = True
        verbose_name = 'Situação de Ação'
        verbose_name_plural = 'Situações de Ações'
        ordering = ['strdescricaosituacao']

    def __str__(self):
        return self.strdescricaosituacao


class VigenciaPNGI(models.Model):
    """
    Períodos de vigência do PNGI
    """
    idvigenciapngi = models.AutoField(primary_key=True, db_column='idvigenciapngi')
    strdescricaovigenciapngi = models.CharField(
        max_length=100, 
        db_column='strdescricaovigenciapngi'
    )
    datiniciovigencia = models.DateField(db_column='datiniciovigencia')
    datfinalvigencia = models.DateField(db_column='datfinalvigencia')
    isvigenciaativa = models.BooleanField(default=False, db_column='isvigenciaativa')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'acoes_pngi.tblvigenciapngi'
        managed = True
        verbose_name = 'Vigência PNGI'
        verbose_name_plural = 'Vigências PNGI'
        ordering = ['-datiniciovigencia']

    def __str__(self):
        return f'{self.strdescricaovigenciapngi} ({self.datiniciovigencia} a {self.datfinalvigencia})'

    def clean(self):
        """
        Validação para garantir que a data final seja maior que a data inicial
        """
        if self.datfinalvigencia and self.datiniciovigencia:
            if self.datfinalvigencia <= self.datiniciovigencia:
                raise ValidationError({
                    'datfinalvigencia': 'A data final deve ser maior que a data inicial.'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def esta_vigente(self):
        """
        Verifica se a vigência está ativa no momento atual
        """
        hoje = timezone.now().date()
        return (
            self.isvigenciaativa and 
            self.datiniciovigencia <= hoje <= self.datfinalvigencia
        )

    @property
    def duracao_dias(self):
        """
        Retorna a duração da vigência em dias
        """
        return (self.datfinalvigencia - self.datiniciovigencia).days


class TipoEntraveAlerta(models.Model):
    """
    Tipos de entraves ou alertas que podem ser associados a ações
    """
    idtipoentravealerta = models.AutoField(primary_key=True, db_column='idtipoentravealerta')
    strdescricaotipoentravealerta = models.CharField(
        max_length=20,
        db_column='strdescricaotipoentravealerta'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'acoes_pngi.tbltipoentravealerta'
        managed = True
        verbose_name = 'Tipo de Entrave/Alerta'
        verbose_name_plural = 'Tipos de Entraves/Alertas'
        ordering = ['strdescricaotipoentravealerta']

    def __str__(self):
        return self.strdescricaotipoentravealerta


class Acoes(models.Model):
    """
    Ações do PNGI
    """
    idacao = models.AutoField(primary_key=True, db_column='idacao')
    strapelido = models.CharField(max_length=50, db_column='strapelido')
    strdescricaoacao = models.CharField(max_length=350, db_column='strdescricaoacao')
    strdescricaoentrega = models.CharField(max_length=20, db_column='strdescricaoentrega')
    idvigenciapngi = models.ForeignKey(
        VigenciaPNGI,
        on_delete=models.PROTECT,
        db_column='idvigenciapngi',
        related_name='acoes'
    )
    idtipoentravealerta = models.ForeignKey(
        TipoEntraveAlerta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='idtipoentravealerta',
        related_name='acoes'
    )
    datdataentrega = models.DateTimeField(
        null=True,
        blank=True,
        db_column='datdataentrega'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'acoes_pngi.tblacoes'
        managed = True
        verbose_name = 'Ação'
        verbose_name_plural = 'Ações'
        ordering = ['strapelido']

    def __str__(self):
        return f'{self.strapelido} - {self.strdescricaoacao[:50]}'


class AcaoPrazo(models.Model):
    """
    Prazos associados a ações com controle de ativo/inativo
    Apenas um prazo ativo por ação
    """
    idacaoprazo = models.AutoField(primary_key=True, db_column='idacaoprazo')
    idacao = models.ForeignKey(
        Acoes,
        on_delete=models.CASCADE,
        db_column='idacao',
        related_name='prazos'
    )
    isacaoprazoativo = models.BooleanField(default=True, db_column='isacaoprazoativo')
    strprazo = models.CharField(max_length=20, db_column='strprazo')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'acoes_pngi.tblacaoprazo'
        managed = True
        verbose_name = 'Prazo de Ação'
        verbose_name_plural = 'Prazos de Ações'
        ordering = ['-isacaoprazoativo', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['idacao', 'isacaoprazoativo'],
                condition=models.Q(isacaoprazoativo=True),
                name='idxacaoprazoativo'
            )
        ]

    def __str__(self):
        status = 'Ativo' if self.isacaoprazoativo else 'Inativo'
        return f'{self.idacao.strapelido} - {self.strprazo} ({status})'

    def clean(self):
        """
        Validação para garantir que apenas um prazo esteja ativo por ação
        """
        if self.isacaoprazoativo:
            existing = AcaoPrazo.objects.filter(
                idacao=self.idacao,
                isacaoprazoativo=True
            ).exclude(pk=self.pk)
            
            if existing.exists():
                raise ValidationError({
                    'isacaoprazoativo': 'Já existe um prazo ativo para esta ação.'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class AcaoDestaque(models.Model):
    """
    Destaques de ações por data
    Única combinação de ação e data de destaque
    """
    idacaodestaque = models.AutoField(primary_key=True, db_column='idacaodestaque')
    idacao = models.ForeignKey(
        Acoes,
        on_delete=models.CASCADE,
        db_column='idacao',
        related_name='destaques'
    )
    datdatadestaque = models.DateTimeField(db_column='datdatadestaque')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'acoes_pngi.tblacaodestaque'
        managed = True
        verbose_name = 'Destaque de Ação'
        verbose_name_plural = 'Destaques de Ações'
        ordering = ['-datdatadestaque']
        constraints = [
            models.UniqueConstraint(
                fields=['idacao', 'datdatadestaque'],
                name='idxacaodestaque'
            )
        ]

    def __str__(self):
        return f'{self.idacao.strapelido} - {self.datdatadestaque.strftime("%d/%m/%Y")}'


class TipoAnotacaoAlinhamento(models.Model):
    """
    Tipos de anotações de alinhamento
    """
    idtipoanotacaoalinhamento = models.AutoField(
        primary_key=True,
        db_column='idtipoanotacaoalinhamento'
    )
    strdescricaotipoanotacaoalinhamento = models.CharField(
        max_length=50,
        db_column='strdescricaotipoanotacaoalinhamento'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'acoes_pngi.tbltipoanotacaoalinhamento'
        managed = True
        verbose_name = 'Tipo de Anotação de Alinhamento'
        verbose_name_plural = 'Tipos de Anotações de Alinhamento'
        ordering = ['strdescricaotipoanotacaoalinhamento']

    def __str__(self):
        return self.strdescricaotipoanotacaoalinhamento


class AcaoAnotacaoAlinhamento(models.Model):
    """
    Anotações de alinhamento das ações
    Combinação única de ação, tipo e data
    """
    idacaoanotacaoalinhamento = models.AutoField(
        primary_key=True,
        db_column='idacaoanotacaoalinhamento'
    )
    idacao = models.ForeignKey(
        Acoes,
        on_delete=models.CASCADE,
        db_column='idacao',
        related_name='anotacoes_alinhamento'
    )
    idtipoanotacaoalinhamento = models.ForeignKey(
        TipoAnotacaoAlinhamento,
        on_delete=models.PROTECT,
        db_column='idtipoanotacaoalinhamento',
        related_name='anotacoes'
    )
    datdataanotacaoalinhamento = models.DateTimeField(
        db_column='datdataanotacaoalinhamento'
    )
    strdescricaoanotacaoalinhamento = models.CharField(
        max_length=500,
        db_column='strdescricaoanotacaoalinhamento'
    )
    strlinkanotacaoalinhamento = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_column='strlinkanotacaoalinhamento'
    )
    strnumeromonitoramento = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        db_column='strnumeromonitoramento'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'acoes_pngi.tblacaoanotacaoalinhamento'
        managed = True
        verbose_name = 'Anotação de Alinhamento'
        verbose_name_plural = 'Anotações de Alinhamento'
        ordering = ['-datdataanotacaoalinhamento']
        constraints = [
            models.UniqueConstraint(
                fields=['idacao', 'idtipoanotacaoalinhamento', 'datdataanotacaoalinhamento'],
                name='idxacaoanotacaoalinhamento'
            )
        ]

    def __str__(self):
        return f'{self.idacao.strapelido} - {self.idtipoanotacaoalinhamento} - {self.datdataanotacaoalinhamento.strftime("%d/%m/%Y")}'

class UsuarioResponsavel(models.Model):
    """
    Usuários responsáveis por ações com informações de contato e órgão
    Relacionado à tabela tblusuario via AUTH_USER_MODEL
    """
    idusuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='idusuario',
        primary_key=True,
        related_name='responsavel_pngi'
    )
    strtelefone = models.CharField(max_length=20, db_column='strtelefone')
    strorgao = models.CharField(max_length=20, db_column='strorgao')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'acoes_pngi.tblusuarioresponsavel'
        managed = True
        verbose_name = 'Usuário Responsável'
        verbose_name_plural = 'Usuários Responsáveis'

    def __str__(self):
        return f'{self.idusuario.name} - {self.strorgao}'


class RelacaoAcaoUsuarioResponsavel(models.Model):
    """
    RelaçãoMany-to-Many entre Ações e Usuários Responsáveis
    Uma ação pode ter vários responsáveis e um responsável pode ter várias ações
    """
    idacaousuarioresponsavel = models.BigAutoField(
        primary_key=True,
        db_column='idacaousuarioresponsavel'
    )
    idacao = models.ForeignKey(
        'Acoes',
        on_delete=models.CASCADE,
        db_column='idacao',
        related_name='responsaveis'
    )
    idusuarioresponsavel = models.ForeignKey(
        'UsuarioResponsavel',
        on_delete=models.CASCADE,
        db_column='idusuarioresponsavel',
        related_name='acoes'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    
    class Meta:
        db_table = 'acoes_pngi.tblrelacaoacaousuarioresponsavel'
        managed = True
        verbose_name = 'Relação Ação X Usuário Responsável'
        verbose_name_plural = 'Relações Ação X Usuários Responsáveis'
        ordering = ['idacaousuarioresponsavel']
        constraints = [
            models.UniqueConstraint(
                fields=['idacao', 'idusuarioresponsavel'],
                name='idxrelacaoacaousuarioresponsavel'
            )
        ]

    def __str__(self):
        return f'{self.idacao.strapelido} - {self.idusuarioresponsavel.idusuario.name}'
