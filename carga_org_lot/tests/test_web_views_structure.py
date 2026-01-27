"""
Testes para estrutura de views
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


class WebViewsStructureTest(TestCase):
    """Testa organização de views"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser_web@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_imports_from_web_views(self):
        """Testa imports de web_views"""
        from ..views.web_views import carga_dashboard
        self.assertTrue(callable(carga_dashboard))
    
    def test_imports_from_api_views(self):
        """Testa imports de api_views"""
        from ..views.api_views import PatriarcaViewSet
        self.assertIsNotNone(PatriarcaViewSet)
    
    def test_backward_compatibility_imports(self):
        """Testa compatibilidade retroativa de imports"""
        from ..views import PatriarcaViewSet, carga_dashboard
        self.assertIsNotNone(PatriarcaViewSet)
        self.assertTrue(callable(carga_dashboard))
    
    def test_login_redirect_unauthenticated(self):
        """Testa redirecionamento para login sem autenticação"""
        self.client.logout()
        response = self.client.get('/carga_org_lot/dashboard/')
        self.assertEqual(response.status_code, 302)
