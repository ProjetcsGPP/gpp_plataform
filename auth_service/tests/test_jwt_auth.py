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
    
    def test_login_success(self):
        """Testa login com sucesso"""
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_missing_fields(self):
        """Testa login sem campos obrigatórios"""
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
