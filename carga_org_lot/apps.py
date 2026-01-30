from django.apps import AppConfig


class CargaOrgLotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carga_org_lot'
    app_code = 'CARGA_ORG_LOT'
    app_display_name = 'Carga Organograma e Lotação'
    verbose_name = 'Carga Organograma e Lotação'
    
    # Permissões customizadas da aplicação
    custom_permissions = [
        ('pode_ativar_organograma', 'Pode ativar versões de organograma'),
        ('pode_ativar_lotacao', 'Pode ativar versões de lotação'),
        ('pode_enviar_api', 'Pode enviar dados para API externa'),
        ('pode_gerar_json', 'Pode gerar arquivos JSON'),
        ('pode_processar_arquivo', 'Pode processar arquivos de upload'),
        ('pode_validar_dados', 'Pode validar dados de carga'),
        ('pode_gerar_relatorios', 'Pode gerar relatórios'),
        ('pode_gerenciar_tokens', 'Pode gerenciar tokens de envio'),
    ]
    
    def ready(self):
        """
        Executado quando a aplicação está pronta.
        Importa signals se existirem.
        """
        try:
            import carga_org_lot.signals  # noqa
        except ImportError:
            pass
