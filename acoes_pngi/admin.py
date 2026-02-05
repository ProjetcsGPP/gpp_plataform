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
    UsuarioResponsavel,
    RelacaoAcaoUsuarioResponsavel
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

@admin.register(UsuarioResponsavel)
class UsuarioResponsavelAdmin(admin.ModelAdmin):
    list_display = ['idusuario', 'get_nome_usuario', 'strtelefone', 'strorgao', 'created_at']
    list_filter = ['strorgao', 'created_at']
    search_fields = ['idusuario__name', 'idusuario__email', 'strtelefone', 'strorgao']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_nome_usuario(self, obj):
        return obj.idusuario.name
    get_nome_usuario.short_description = 'Nome'
    get_nome_usuario.admin_order_field = 'idusuario__name'


@admin.register(RelacaoAcaoUsuarioResponsavel)
class RelacaoAcaoUsuarioResponsavelAdmin(admin.ModelAdmin):
    list_display = ['idacaousuarioresponsavel', 'get_acao', 'get_responsavel', 'created_at']
    list_filter = ['created_at']
    search_fields = [
        'idacao__strapelido',
        'idusuarioresponsavel__idusuario__name',
        'idusuarioresponsavel__strorgao'
    ]
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['idacao', 'idusuarioresponsavel']
    
    def get_acao(self, obj):
        return obj.idacao.strapelido
    get_acao.short_description = 'Ação'
    get_acao.admin_order_field = 'idacao__strapelido'
    
    def get_responsavel(self, obj):
        return f"{obj.idusuarioresponsavel.idusuario.name} ({obj.idusuarioresponsavel.strorgao})"
    get_responsavel.short_description = 'Responsável'


# Outros admins...

@admin.register(TipoEntraveAlerta)
class TipoEntraveAlertaAdmin(admin.ModelAdmin):
    list_display = ['idtipoentravealerta', 'strdescricaotipoentravealerta', 'created_at']
    search_fields = ['strdescricaotipoentravealerta']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Acoes)
class AcoesAdmin(admin.ModelAdmin):
    list_display = ['idacao', 'strapelido', 'idvigenciapngi', 'datdataentrega', 'idtipoentravealerta']
    list_filter = ['idvigenciapngi', 'idtipoentravealerta', 'datdataentrega']
    search_fields = ['strapelido', 'strdescricaoacao']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['idvigenciapngi', 'idtipoentravealerta']


@admin.register(AcaoPrazo)
class AcaoPrazoAdmin(admin.ModelAdmin):
    list_display = ['idacaoprazo', 'idacao', 'strprazo', 'isacaoprazoativo', 'created_at']
    list_filter = ['isacaoprazoativo', 'created_at']
    search_fields = ['idacao__strapelido', 'strprazo']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['idacao']


@admin.register(AcaoDestaque)
class AcaoDestaqueAdmin(admin.ModelAdmin):
    list_display = ['idacaodestaque', 'idacao', 'datdatadestaque', 'created_at']
    list_filter = ['datdatadestaque', 'created_at']
    search_fields = ['idacao__strapelido']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['idacao']


@admin.register(TipoAnotacaoAlinhamento)
class TipoAnotacaoAlinhamentoAdmin(admin.ModelAdmin):
    list_display = ['idtipoanotacaoalinhamento', 'strdescricaotipoanotacaoalinhamento', 'created_at']
    search_fields = ['strdescricaotipoanotacaoalinhamento']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AcaoAnotacaoAlinhamento)
class AcaoAnotacaoAlinhamentoAdmin(admin.ModelAdmin):
    list_display = [
        'idacaoanotacaoalinhamento',
        'idacao',
        'idtipoanotacaoalinhamento',
        'datdataanotacaoalinhamento',
        'strnumeromonitoramento'
    ]
    list_filter = ['idtipoanotacaoalinhamento', 'datdataanotacaoalinhamento']
    search_fields = [
        'idacao__strapelido',
        'strdescricaoanotacaoalinhamento',
        'strnumeromonitoramento'
    ]
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['idacao', 'idtipoanotacaoalinhamento']