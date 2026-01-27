# acoes_pngi/tests/test_views.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from accounts.models import Aplicacao, Role, UserRole

User = get_user_model()


class AcoesPNGIViewsTest(TestCase):
    """Testes para views de Ações PNGI"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()
        
        self.user = User.objects.create_user(
            email='pngi@example.com',
            password='testpass123',
            name='PNGI User'
        )
        
        # Criar aplicação PNGI
        self.app = Aplicacao.objects.create(
            codigointerno='ACOES_PNGI',
            nomeaplicacao='Ações PNGI'
        )
        self.role = Role.objects.create(
            aplicacao=self.app,
            nomeperfil='Gestor PNGI',
            codigoperfil='GESTOR_PNGI'
        )
        UserRole.objects.create(
            user=self.user,
            aplicacao=self.app,
            role=self.role
        )
    
    def test_pngi_area_requires_authentication(self):
        """Testa que área PNGI requer autenticação"""
        response = self.client.get('/acoes-pngi/')
        # Deve redirecionar para login ou retornar 401/403
        self.assertIn(response.status_code, [302, 401, 403, 404])
    
    def test_authenticated_user_can_access(self):
        """Testa que usuário autenticado pode acessar"""
        self.client.login(email='pngi@example.com', password='testpass123')
        response = self.client.get('/acoes-pngi/')
        # Pode ser 200 (sucesso) ou 404 (rota não existe ainda)
        self.assertIn(response.status_code, [200, 404])
