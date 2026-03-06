from django.apps import AppConfig

# portal/apps.py - Adicione:
class PortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portal'
    
    def ready(self):
        """Registra signals e inicializa services."""
        import portal.services  # Inicializa singleton
        from . import permissions  # Registra permissões