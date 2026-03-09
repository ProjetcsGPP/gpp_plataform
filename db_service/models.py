from django.db import models

class AppClient(models.Model):
    """
    Cliente técnico que pode chamar o db_service.
    """
    # Use string reference para evitar circular import

    aplicacao = models.OneToOneField(
        'accounts.Aplicacao', 
        on_delete=models.CASCADE,
        db_column='aplicacao_id'  # ← ADICIONAR
    )
    client_id = models.CharField(max_length=100, unique=True)
    client_secret_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'db_service_appclient'  # ← ADICIONAR
        
    def __str__(self):
        return f'{self.aplicacao.codigointerno} ({self.client_id})'

