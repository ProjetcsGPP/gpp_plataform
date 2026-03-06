"""
Testes API Portal - AUTENTICAÇÃO NATIVA (SEM force_authenticate)
100% Django nativo + seu modelo User custom
"""

import json

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from django.test.client import Client as DjangoClient

from accounts.models import Aplicacao, Role, UserRole


class PortalAPIViewsTest(TestCase):
    """Testes nativos das API views."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Dados compartilhados."""
        User = get_user_model()
        
        # Usuário com acesso
        cls.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            name="Test User",
            password="testpass123"
        )
        
        # Usuário sem acesso
        cls.other_user = User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            name="Other User",
            password="pass123"
        )
        
        # Superusuário
        cls.superuser = User.objects.create_superuser(
            username="admin@example.com",
            email="admin@example.com",
            name="Admin GPP",
            password="admin123"
        )
        
        # Aplicações
        cls.app = Aplicacao.objects.create(
            codigointerno="TEST_APP",
            nomeaplicacao="Test App",
            base_url="http://test.com",
            isshowinportal=True
        )
        
        cls.role = Role.objects.create(codigoperfil="TEST", nome="Test")
        UserRole.objects.create(
            user=cls.user, aplicacao=cls.app, role=cls.role
        )

    def _login_user(self, username: str, password: str) -> DjangoClient:
        """Login nativo via POST /login/."""
        client = DjangoClient()
        login_data = {
            'email': username,  # Seu login usa email
            'password': password
        }
        client.post(reverse('accounts:login'), login_data)  # Ajuste URL se necessário
        return client

    # ========== 401 SEM AUTENTICAÇÃO ==========
    def test_list_unauthenticated(self) -> None:
        client = DjangoClient()
        response = client.get("/api/v1/portal/applications/")
        self.assertEqual(response.status_code, 401)

    def test_get_app_unauthenticated(self) -> None:
        client = DjangoClient()
        response = client.get("/api/v1/portal/applications/TEST_APP/")
        self.assertEqual(response.status_code, 401)

    # ========== 403 SEM PERMISSÃO ==========
    def test_list_no_portal_access(self) -> None:
        """Usuário sem apps -> CanAccessPortal falha."""
        client = self._login_user("other@example.com", "pass123")
        response = client.get("/api/v1/portal/applications/")
        self.assertEqual(response.status_code, 403)

    def test_get_app_no_permission(self) -> None:
        """Sem role na app -> CanViewApplication falha."""
        client = self._login_user("other@example.com", "pass123")
        response = client.get("/api/v1/portal/applications/TEST_APP/")
        self.assertEqual(response.status_code, 403)

    # ========== 200 COM PERMISSÃO ==========
    def test_list_returns_apps(self) -> None:
        client = self._login_user("test@example.com", "testpass123")
        response = client.get("/api/v1/portal/applications/")
        
        self.assertEqual(response.status_code, 200)
        # Para JSON response, usa content
        import json
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["codigo"], "TEST_APP")

    def test_get_app_success(self) -> None:
        client = self._login_user("test@example.com", "testpass123")
        response = client.get("/api/v1/portal/applications/TEST_APP/")
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["codigo"], "TEST_APP")

    # ========== SUPERUSER BYPASS ==========
    def test_superuser_access_all(self) -> None:
        client = self._login_user("admin@example.com", "admin123")
        
        response = client.get("/api/v1/portal/applications/TEST_APP/")
        self.assertEqual(response.status_code, 200)

    # ========== 404 ERROS ==========
    def test_nonexistent_app_404(self) -> None:
        client = self._login_user("test@example.com", "testpass123")
        response = client.get("/api/v1/portal/applications/FAKE/")
        self.assertEqual(response.status_code, 404)
