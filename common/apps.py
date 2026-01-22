"""
Configuração da aplicação Common.
Contém utilitários, serializers e serviços compartilhados entre aplicações.
"""

from django.apps import AppConfig


class CommonConfig(AppConfig):
    """
    Configuração da aplicação Common.
    Responsável por fornecer funcionalidades compartilhadas.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    verbose_name = 'Common Utilities'
