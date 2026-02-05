from django.contrib import admin
from .models import (
    Eixo, 
    SituacaoAcao, 
    VigenciaPNGI,
    TipoEntraveAlerta,
    Acoes,
    AcaoPrazo,
    AcaoDestaque,
    TipoAnotacaoAlinhamento,
    AcaoAnotacaoAlinhamento,
    UsuarioResponsavel
)


@admin.register(Eixo)
class EixoAdmin(admin.ModelAdmin):
    list_display = ('stralias', 'strdescricaoeixo', 'created_at', 'updated_at')
    search_fields = ('stralias', 'strdescricaoeixo')
    list_filter = ('created_at',)
    ordering = ('stralias',)


@admin.register(SituacaoAcao)
class SituacaoAcaoAdmin(admin.ModelAdmin):
    list_display = ('strdescricaosituacao', 'created_at', 'updated_at')
    search_fields = ('strdescricaosituacao',)
    list_filter = ('created_at',)
    ordering = ('strdescricaosituacao',)


@admin.register(VigenciaPNGI)
class VigenciaPNGIAdmin(admin.ModelAdmin):
    list_display = (
        'strdescricaovigenciapngi', 
        'datiniciovigencia', 
        'datfinalvigencia', 
        'isvigenciaativa',
        'esta_vigente',
        'duracao_dias'
    )
    search_fields = ('strdescricaovigenciapngi',)
    list_filter = ('isvigenciaativa', 'datiniciovigencia', 'datfinalvigencia')
    date_hierarchy = 'datiniciovigencia'
    ordering = ('-datiniciovigencia',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('strdescricaovigenciapngi', 'isvigenciaativa')
        }),
        ('Período de Vigência', {
            'fields': ('datiniciovigencia', 'datfinalvigencia')
        }),
    )
    
    def esta_vigente(self, obj):
        return obj.esta_vigente
    esta_vigente.boolean = True
    esta_vigente.short_description = 'Vigente Agora'
    
    def duracao_dias(self, obj):
        return f'{obj.duracao_dias} dias'
    duracao_dias.short_description = 'Duração'


@admin.register(TipoEntraveAlerta)
class TipoEntraveAlertaAdmin(admin.ModelAdmin):
    list_display = ('idtipoentravealerta', 'strdescricaotipoentravealerta', 'created_at', 'updated_at')
    search_fields = ('strdescricaotipoentravealerta',)
    list_filter = ('created_at',)
    ordering = ('strdescricaotipoentravealerta',)


@admin.register(Acoes)
class AcoesAdmin(admin.ModelAdmin):
    list_display = (
        'idacao',
        'strapelido',
        'strdescricaoacao_truncated',
        'strdescricaoentrega',
        'idvigenciapngi',
        'idtipoentravealerta',
        'datdataentrega',
        'created_at'
    )
    search_fields = ('strapelido', 'strdescricaoacao', 'strdescricaoentrega')
    list_filter = (
        'idvigenciapngi',
        'idtipoentravealerta',
        'datdataentrega',
        'created_at'
    )
    date_hierarchy = 'datdataentrega'
    ordering = ('strapelido',)
    raw_id_fields = ('idvigenciapngi', 'idtipoentravealerta')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('strapelido', 'strdescricaoacao', 'strdescricaoentrega')
        }),
        ('Relacionamentos', {
            'fields': ('idvigenciapngi', 'idtipoentravealerta')
        }),
        ('Datas', {
            'fields': ('datdataentrega',)
        }),
    )
    
    def strdescricaoacao_truncated(self, obj):
        if len(obj.strdescricaoacao) > 50:
            return f'{obj.strdescricaoacao[:50]}...'
        return obj.strdescricaoacao
    strdescricaoacao_truncated.short_description = 'Descrição'


@admin.register(AcaoPrazo)
class AcaoPrazoAdmin(admin.ModelAdmin):
    list_display = (
        'idacaoprazo',
        'idacao',
        'strprazo',
        'isacaoprazoativo',
        'created_at',
        'updated_at'
    )
    search_fields = ('idacao__strapelido', 'strprazo')
    list_filter = ('isacaoprazoativo', 'created_at')
    ordering = ('-isacaoprazoativo', '-created_at')
    raw_id_fields = ('idacao',)
    
    fieldsets = (
        ('Informações da Ação', {
            'fields': ('idacao',)
        }),
        ('Prazo', {
            'fields': ('strprazo', 'isacaoprazoativo')
        }),
    )


@admin.register(AcaoDestaque)
class AcaoDestaqueAdmin(admin.ModelAdmin):
    list_display = (
        'idacaodestaque',
        'idacao',
        'datdatadestaque',
        'created_at'
    )
    search_fields = ('idacao__strapelido',)
    list_filter = ('datdatadestaque', 'created_at')
    date_hierarchy = 'datdatadestaque'
    ordering = ('-datdatadestaque',)
    raw_id_fields = ('idacao',)


@admin.register(TipoAnotacaoAlinhamento)
class TipoAnotacaoAlinhamentoAdmin(admin.ModelAdmin):
    list_display = (
        'idtipoanotacaoalinhamento',
        'strdescricaotipoanotacaoalinhamento',
        'created_at',
        'updated_at'
    )
    search_fields = ('strdescricaotipoanotacaoalinhamento',)
    list_filter = ('created_at',)
    ordering = ('strdescricaotipoanotacaoalinhamento',)


@admin.register(AcaoAnotacaoAlinhamento)
class AcaoAnotacaoAlinhamentoAdmin(admin.ModelAdmin):
    list_display = (
        'idacaoanotacaoalinhamento',
        'idacao',
        'idtipoanotacaoalinhamento',
        'datdataanotacaoalinhamento',
        'strnumeromonitoramento',
        'created_at'
    )
    search_fields = (
        'idacao__strapelido',
        'strdescricaoanotacaoalinhamento',
        'strnumeromonitoramento'
    )
    list_filter = (
        'idtipoanotacaoalinhamento',
        'datdataanotacaoalinhamento',
        'created_at'
    )
    date_hierarchy = 'datdataanotacaoalinhamento'
    ordering = ('-datdataanotacaoalinhamento',)
    raw_id_fields = ('idacao', 'idtipoanotacaoalinhamento')
    
    fieldsets = (
        ('Relacionamentos', {
            'fields': ('idacao', 'idtipoanotacaoalinhamento')
        }),
        ('Anotação', {
            'fields': (
                'datdataanotacaoalinhamento',
                'strdescricaoanotacaoalinhamento',
                'strlinkanotacaoalinhamento',
                'strnumeromonitoramento'
            )
        }),
    )


@admin.register(UsuarioResponsavel)
class UsuarioResponsavelAdmin(admin.ModelAdmin):
    list_display = (
        'idusuarioresponsavel',
        'idusuario',
        'strtelefone',
        'strorgao',
        'created_at',
        'updated_at'
    )
    search_fields = ('idusuario', 'strtelefone', 'strorgao')
    list_filter = ('strorgao', 'created_at')
    ordering = ('idusuario',)
    
    fieldsets = (
        ('Usuário', {
            'fields': ('idusuario',)
        }),
        ('Informações de Contato', {
            'fields': ('strtelefone', 'strorgao')
        }),
    )
