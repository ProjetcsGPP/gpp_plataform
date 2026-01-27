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
        
        # Criar aplicação e role para testes
        self.app = Aplicacao.objects.create(
            codigointerno='PORTAL',
            nomeaplicacao='Portal GPP'
        )
        self.role = Role.objects.create(
            aplicacao=self.app,
            nomeperfil='Usuário',
            codigoperfil='USER_PORTAL'
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
