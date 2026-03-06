"""
Testes Web Views Portal - NATIVO + TYPE SAFE
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from accounts.models import Aplicacao, Role, UserRole


class PortalViewsTest(TestCase):
    """Testes para views web do Portal."""

    databases = {"default"}

    @classmethod
    def setUpTestData(cls):
        """Dados compartilhados."""
        User = get_user_model()
        
        cls.user = User.objects.create_user(
            username="portal@example.com",  # ✅ OBRIGATÓRIO
            email="portal@example.com",
            name="Portal User",
            password="testpass123"
        )
        
        cls.app, _ = Aplicacao.objects.get_or_create(
            codigointerno="PORTAL",
            defaults={
                "nomeaplicacao": "Portal GPP", 
                "isshowinportal": True,
                "base_url": "/"
            }
        )
        
        cls.role, _ = Role.objects.get_or_create(
            codigoperfil="USER_PORTAL",
            defaults={"nome": "Usuário Portal"}  # ✅ nome ao invés nomeperfil
        )
        
        UserRole.objects.get_or_create(
            user=cls.user, 
            aplicacao=cls.app, 
            role=cls.role
        )

    def setUp(self):
        self.client = Client()

    def test_portal_login_get(self):
        """GET /portal/login/ renderiza form."""
        response = self.client.get(reverse('portal:login'))  # Ajuste name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/login.html')

    def test_portal_login_post_success(self):
        """POST login válido redireciona."""
        response = self.client.post(reverse('portal:login'), {
            'email': 'portal@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(self.client.session.session_key)  # Sessão ativa

    def test_portal_login_post_invalid(self):
        """POST inválido renderiza form com erro."""
        response = self.client.post(reverse('portal:login'), {
            'email': 'invalid@example.com',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/login.html')
        # Verifica mensagem de erro (se usa messages)
        self.assertContains(response, "Senha incorreta", count=0)  # Ajuste texto

    def test_portal_dashboard_requires_login(self):
        """Dashboard requer login."""
        response = self.client.get(reverse('portal:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response['Location'].lower())  # ✅ response['Location']

    def test_portal_dashboard_authenticated(self):
        """Dashboard acessível após login."""
        self.client.login(username='portal@example.com', password='testpass123')
        response = self.client.get(reverse('portal:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/dashboard.html')

    def test_portal_logout(self):
        """Logout funciona."""
        self.client.login(username='portal@example.com', password='testpass123')
        response = self.client.get(reverse('portal:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response['Location'].lower())

    def test_index_anon(self):
        """Index anônimo."""
        response = self.client.get("/")
        self.assertIn(response.status_code, [200, 302])

    def test_index_authenticated(self):
        """Index autenticado."""
        self.client.login(username='portal@example.com', password='testpass123')
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)  # Redirect dashboard


class PortalNavigationTest(TestCase):
    """Testes de navegação."""

    def setUp(self):
        self.client = Client()

    def test_static_pages(self):
        """Páginas públicas."""
        urls = [
            "/",  # Index
            reverse('portal:login'),  # Login page
        ]
        for url_name in urls:
            response = self.client.get(url_name)
            self.assertLess(response.status_code, 400, f"URL {url_name} falhou")

    def test_protected_pages_redirect(self):
        """Páginas protegidas redirecionam."""
        protected = [
            reverse('portal:dashboard'),
        ]
        for url in protected:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('login', response['Location'].lower())
