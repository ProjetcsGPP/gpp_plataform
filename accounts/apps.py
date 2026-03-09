from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """
        Importa os signals quando a app é inicializada.
        """
        import accounts.signals  # noqa
