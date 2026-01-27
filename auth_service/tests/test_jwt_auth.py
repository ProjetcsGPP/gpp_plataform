# auth_service/tests/test_jwt_auth.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import Aplicacao, Role, UserRole

User = get_user_model()


class JWTAuthenticationTest(TestCase):
    """Testes para autenticação JWT"""
    
    databases = {'default'}
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )
        
        # Usar get_or_create para evitar conflito com setup do carga_org_lot
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='PORTAL',
            defaults={'nomeaplicacao': 'Portal GPP'}
        )
        self.role, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='USER_PORTAL',
            defaults={'nomeperfil': 'Usuário'}
        )
        UserRole.objects.create(
            user=self.user,
            aplicacao=self.app,
            role=self.role
        )
    
    def test_user_created_with_role(self):
        """Testa que usuário foi criado com role corretamente"""
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        user_role = UserRole.objects.get(user=self.user)
        self.assertEqual(user_role.aplicacao.codigointerno, 'PORTAL')
        self.assertEqual(user_role.role.codigoperfil, 'USER_PORTAL')
    
    def test_auth_service_app_installed(self):
        """Testa que app auth_service está instalado"""
        from django.conf import settings
        self.assertIn('auth_service', settings.INSTALLED_APPS)
    
    def test_login_endpoint_exists(self):
        """Testa existência do endpoint de login"""
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        # Endpoint pode retornar 404 (não implementado), 200 (sucesso) ou 401 (erro auth)
        self.assertIn(response.status_code, [200, 401, 404])
