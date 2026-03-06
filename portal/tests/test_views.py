"""
Testes Web Views - FINAL (SEM username)
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import Aplicacao, Role, UserRole


class PortalViewsTest(TestCase):
    databases = {"default"}

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        
        cls.user = User.objects.create_user(
            username="portal",  # prefixo
            email="portal@example.com",
            name="Portal User",
            password="testpass123",
        )
        
        cls.app, _ = Aplicacao.objects.get_or_create(
            codigointerno="PORTAL",
            defaults={"nomeaplicacao": "Portal GPP", "isshowinportal": True}
        )
        
        cls.role, _ = Role.objects.get_or_create(
            codigoperfil="USER_PORTAL",
            defaults={"nome": "Usuário Portal"}
        )
        
        UserRole.objects.get_or_create(
            user=cls.user, aplicacao=cls.app, role=cls.role
        )

    def setUp(self):
        self.client = Client()

    # Testes específicos (ajuste reverse names)
    def test_login_get(self):
        response = self.client.get(reverse('portal:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_post_success(self):
        response = self.client.post(reverse('portal:login'), {
            'email': 'portal@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_dashboard_unauth(self):
        response = self.client.get(reverse('portal:dashboard'))
        self.assertRedirects(response, reverse('portal:login'))

    def test_dashboard_auth(self):
        self.client.login(email='portal@example.com', password='testpass123')
        response = self.client.get(reverse('portal:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(email='portal@example.com', password='testpass123')
        response = self.client.get(reverse('portal:logout'))
        self.assertRedirects(response, reverse('portal:login'))


class PortalNavigationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_public_pages(self):
        for url in ['/', reverse('portal:login')]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertLess(response.status_code, 400)
