"""
Testes do backend de autenticação customizado.
"""

from django.test import TestCase
from django.contrib.auth import authenticate
from accounts.models import User


class EmailBackendTest(TestCase):
    """Testes do EmailBackend"""
    
    @classmethod
    def setUpTestData(cls):
        """Cria usuário de teste"""
        cls.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
    
    def test_authenticate_with_email(self):
        """Testa autenticação com email"""
        user = authenticate(
            username='test@example.com',
            password='testpass123'
        )
        
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')
    
    def test_authenticate_wrong_password(self):
        """Testa autenticação com senha incorreta"""
        user = authenticate(
            username='test@example.com',
            password='wrongpassword'
        )
        
        self.assertIsNone(user)
    
    def test_authenticate_nonexistent_user(self):
        """Testa autenticação de usuário inexistente"""
        user = authenticate(
            username='nonexistent@example.com',
            password='testpass123'
        )
        
        self.assertIsNone(user)
