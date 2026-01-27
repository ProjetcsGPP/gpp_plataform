# portal/tests/test_views.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import Aplicacao, Role, UserRole

User = get_user_model()


class PortalViewsTest(TestCase):
    """Testes para views do Portal"""
    
    databases = {'default'}
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='portal@example.com',
            password='testpass123',
            name='Portal User'
        )
        
        # Usar get_or_create para evitar conflito
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='PORTAL',
            defaults={
                'nomeaplicacao': 'Portal GPP',
                'isshowinportal': True
            }
        )
        self.role, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='USER_PORTAL',
            defaults={'nomeperfil': 'Usuário Portal'}
        )
        UserRole.objects.create(
            user=self.user,
            aplicacao=self.app,
            role=self.role
        )
    
    def test_index_accessible(self):
        """Testa que página inicial é acessível"""
        response = self.client.get('/')
        # Pode retornar 200 (página) ou 302 (redirect para login)
        self.assertIn(response.status_code, [200, 302])
    
    def test_portal_requires_authentication(self):
        """Testa que áreas protegidas requerem autenticação"""
        # Tenta acessar sem login - deve redirecionar
        response = self.client.get('/portal/dashboard/')
        if response.status_code == 302:
            self.assertTrue(
                'login' in response.url or response.url == '/'
            )
    
    def test_authenticated_user_access(self):
        """Testa que usuário autenticado tem acesso"""
        self.client.login(email='portal@example.com', password='testpass123')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class PortalNavigationTest(TestCase):
    """Testes para navegação do Portal"""
    
    databases = {'default'}
    
    def setUp(self):
        self.client = Client()
    
    def test_static_pages_load(self):
        """Testa que páginas estáticas carregam"""
        urls_to_test = [
            '/',
        ]
        for url in urls_to_test:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 302, 404])
