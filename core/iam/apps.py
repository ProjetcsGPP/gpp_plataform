from django.apps import AppConfig


class IAMConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.iam'
    verbose_name = 'Identity and Access Management'
    
    def ready(self):
        """Initialize IAM module on Django startup"""
        # Import signals if any
        # import core.iam.signals
        pass