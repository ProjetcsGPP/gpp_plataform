from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


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
        managed = False
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
        managed = False
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
        managed = False
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
    
    