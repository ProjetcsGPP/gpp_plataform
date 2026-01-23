"""
Testes de views do Portal.
"""

from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User


class PortalViewsTest(TestCase):
    """Testes das views do portal"""
    
    @classmethod
    def setUpTestData(cls):
        """Cria usuário de teste"""
        cls.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
    
    def setUp(self):
        """Configura cliente"""
        self.client = Client()
    
    def test_portal_index_redirects_anonymous(self):
        """Testa que portal redireciona usuários anônimos"""
        response = self.client.get('/')
        
        # Deve redirecionar para login
        self.assertEqual(response.status_code, 302)
    
    def test_portal_index_authenticated(self):
        """Testa acesso ao portal autenticado"""
        self.client.force_login(self.user)
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
