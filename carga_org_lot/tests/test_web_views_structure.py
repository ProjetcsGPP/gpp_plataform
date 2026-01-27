"""
Testes para estrutura de Web Views
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

User = get_user_model()


class WebViewsStructureTest(TestCase):
    """Testes para verificar estrutura das web views"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser_web',
            password='testpass123'
        )
    
    def test_imports_from_web_views(self):
        """Testa imports de web_views"""
        try:
            from ..views.web_views import (
                carga_login,
                carga_dashboard,
                patriarca_list,
                organograma_list,
                lotacao_list,
                carga_list
            )
            self.assertTrue(callable(carga_login))
            self.assertTrue(callable(carga_dashboard))
            self.assertTrue(callable(patriarca_list))
        except ImportError as e:
            self.fail(f"Erro ao importar web views: {e}")
    
    def test_imports_from_api_views(self):
        """Testa imports de api_views"""
        try:
            from ..views.api_views import (
                PatriarcaViewSet,
                OrganogramaVersaoViewSet,
                LotacaoVersaoViewSet,
                CargaPatriarcaViewSet,
                LotacaoJsonOrgaoViewSet,
                TokenEnvioCargaViewSet
            )
            from rest_framework.viewsets import ModelViewSet
            self.assertTrue(issubclass(PatriarcaViewSet, ModelViewSet))
            self.assertTrue(issubclass(LotacaoJsonOrgaoViewSet, ModelViewSet))
        except ImportError as e:
            self.fail(f"Erro ao importar API views: {e}")
    
    def test_backward_compatibility_imports(self):
        """Testa compatibilidade retroativa de imports"""
        try:
            # Imports antigos devem continuar funcionando
            from ..views import (
                carga_login,
                PatriarcaViewSet,
                LotacaoJsonOrgaoViewSet
            )
            self.assertTrue(callable(carga_login))
        except ImportError as e:
            self.fail(f"Erro na compatibilidade retroativa: {e}")
    
    def test_login_redirect_unauthenticated(self):
        """Testa redirecionamento para login sem autenticação"""
        response = self.client.get('/carga_org_lot/')
        # Deve redirecionar para login ou retornar 403/302
        self.assertIn(response.status_code, [302, 403, 401])
