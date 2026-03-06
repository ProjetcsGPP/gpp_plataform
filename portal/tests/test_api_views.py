"""
Testes para API views do Portal - REFATORADAS E TYPE SAFE
"""

from typing import Any
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.response import Response

from accounts.models import Aplicacao, Role, UserRole
from portal.views.api_views import (
    rest_list_applications,
    rest_check_app_access,
    rest_get_application,
)


class PortalAPIViewsTest(TestCase):
    """Testes das views API do Portal."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Configura dados de teste compartilhados."""
        User = get_user_model()
        
        # Usuário com acesso
        cls.user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="testpass123"
        )
        
        # Usuário sem acesso
        cls.other_user = User.objects.create_user(
            email="other@example.com",
            name="Other User",
            password="pass123"
        )
        
        # Aplicação
        cls.app = Aplicacao.objects.create(
            codigointerno="TEST_APP",
            nomeaplicacao="Test Application",
            base_url="http://test.com",
            isshowinportal=True
        )
        
        # Role
        cls.role = Role.objects.create(
            codigoperfil="TEST_ROLE",
            nome="Test Role"
        )
        
        # UserRole para usuário com acesso
        UserRole.objects.create(
            user=cls.user,
            aplicacao=cls.app,
            role=cls.role
        )

    def setUp(self) -> None:
        """Configura cliente para cada teste."""
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_list_applications_requires_authentication(self) -> None:
        """Testa que listagem requer autenticação."""
        response = self.client.get("/api/v1/portal/applications/")
        self.assertEqual(response.status_code, 401)

    def test_list_applications_returns_user_apps(self) -> None:
        """Testa que retorna aplicações do usuário."""
        self.client.force_authenticate(user=self.user)
        response: Response = self.client.get("/api/v1/portal/applications/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["codigo"], "TEST_APP")
        self.assertEqual(response.data[0]["nome"], "Test Application")

    def test_get_application_requires_permission(self) -> None:
        """Testa que detalhes da aplicação requerem permissão."""
        self.client.force_authenticate(user=self.other_user)
        response: Response = self.client.get("/api/v1/portal/applications/TEST_APP/")
        
        # Deve retornar 403 Forbidden (CanViewApplication falha)
        self.assertEqual(response.status_code, 403)

    def test_get_application_returns_data_with_permission(self) -> None:
        """Testa que retorna dados com permissão válida."""
        self.client.force_authenticate(user=self.user)
        response: Response = self.client.get("/api/v1/portal/applications/TEST_APP/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["codigo"], "TEST_APP")
        self.assertEqual(response.data["nome"], "Test Application")
        self.assertEqual(response.data["showInPortal"], True)

    def test_check_app_access_correctly(self) -> None:
        """Testa verificação de acesso à aplicação."""
        self.client.force_authenticate(user=self.user)
        response: Response = self.client.get("/api/v1/portal/applications/TEST_APP/access/")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["hasAccess"])
        self.assertEqual(response.data["application"]["codigo"], "TEST_APP")

    def test_check_app_access_denied(self) -> None:
        """Testa verificação de acesso negado."""
        self.client.force_authenticate(user=self.other_user)
        response: Response = self.client.get("/api/v1/portal/applications/TEST_APP/access/")
        
        self.assertEqual(response.status_code, 403)  # CanViewApplication falha

    def test_app_not_found_returns_404(self) -> None:
        """Testa aplicação não encontrada."""
        self.client.force_authenticate(user=self.user)
        response: Response = self.client.get("/api/v1/portal/applications/NONEXISTENT/")
        
        self.assertEqual(response.status_code, 404)

    def test_functional_view_test_with_factory(self) -> None:
        """Testa views funcionais usando APIRequestFactory."""
        request = self.factory.get("/api/v1/portal/applications/")
        request.user = self.user
        
        response: Response = rest_list_applications(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
