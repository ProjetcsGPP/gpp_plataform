from django.db import models

class AppClient(models.Model):
    """
    Cliente técnico que pode chamar o db_service.
    """
    # Use string reference para evitar circular import
    aplicacao = models.OneToOneField(
        'accounts.Aplicacao', 
        on_delete=models.CASCADE
    )
    client_id = models.CharField(max_length=100, unique=True)
    client_secret_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.aplicacao.codigointerno} ({self.client_id})'

