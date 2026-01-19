from django.contrib import admin
from .models import Eixo, SituacaoAcao, VigenciaPNGI


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