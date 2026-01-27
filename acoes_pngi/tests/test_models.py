# acoes_pngi/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AcoesPNGIBasicTest(TestCase):
    """Testes básicos para Acoes PNGI"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def test_app_installed(self):
        """Testa que app acoes_pngi está instalada"""
        from django.conf import settings
        self.assertIn('acoes_pngi', settings.INSTALLED_APPS)
    
    def test_database_configured(self):
        """Testa que database gpp_plataform_db está configurado"""
        from django.conf import settings
        self.assertIn('gpp_plataform_db', settings.DATABASES)
