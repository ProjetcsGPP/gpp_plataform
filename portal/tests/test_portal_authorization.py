"""
Testes para PortalAuthorizationService - 100% Type Safe
"""

from django.test import TestCase
from django.core.cache import cache
from unittest.mock import patch

from accounts.models import Aplicacao, Role, User, UserRole

from portal.services.portal_authorization import (
    PortalAuthorizationService,
    get_portal_authorization_service,
)


class PortalAuthorizationServiceTest(TestCase):
    """Testes completos do serviço de autorização do Portal."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Configura dados de teste compartilhados."""
        User = User  # type: ignore
        
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
        
        # Aplicação visível
        cls.visible_app = Aplicacao.objects.create(
            codigointerno="VISIBLE_APP",
            nomeaplicacao="Visible App",
            base_url="http://visible.com",
            isshowinportal=True
        )
        
        # Aplicação oculta
        cls.hidden_app = Aplicacao.objects.create(
            codigointerno="HIDDEN_APP",
            nomeaplicacao="Hidden App",
            base_url="http://hidden.com",
            isshowinportal=False
        )
        
        # Role
        cls.role = Role.objects.create(
            codigoperfil="TEST_ROLE",
            nome="Test Role"
        )
        
        # UserRole
        cls.user_role = UserRole.objects.create(
            user=cls.user,
            aplicacao=cls.visible_app,
            role=cls.role
        )

    def setUp(self) -> None:
        """Limpa cache antes de cada teste."""
        cache.clear()
        self.service = get_portal_authorization_service()

    def test_user_can_access_application_with_valid_role(self) -> None:
        """Testa que usuário com role pode acessar aplicação."""
        result = self.service.user_can_access_application(
            self.user.id, 
            "VISIBLE_APP"
        )
        self.assertTrue(result)

    def test_user_cannot_access_application_without_role(self) -> None:
        """Testa que usuário sem role não pode acessar aplicação."""
        result = self.service.user_can_access_application(
            self.other_user.id, 
            "VISIBLE_APP"
        )
        self.assertFalse(result)

    def test_get_user_applications_returns_correct_apps(self) -> None:
        """Testa que retorna aplicações corretas do usuário."""
        applications = self.service.get_user_applications(self.user.id)
        
        self.assertEqual(len(applications), 1)
        self.assertEqual(applications[0]["codigo"], "VISIBLE_APP")
        self.assertEqual(applications[0]["nome"], "Visible App")

    def test_get_user_applications_filters_hidden_apps(self) -> None:
        """Testa que filtra aplicações ocultas."""
        # Adicionar role para app oculta
        UserRole.objects.create(
            user=self.user,
            aplicacao=self.hidden_app,
            role=self.role
        )
        
        applications = self.service.get_user_applications(self.user.id)
        
        # Deve retornar APENAS a aplicação visível
        self.assertEqual(len(applications), 1)
        self.assertEqual(applications[0]["codigo"], "VISIBLE_APP")

    def test_get_application_by_code_returns_correct_app(self) -> None:
        """Testa que busca aplicação por código corretamente."""
        app = self.service.get_application_by_code("VISIBLE_APP")
        
        self.assertIsNotNone(app)
        self.assertEqual(app["codigo"], "VISIBLE_APP")
        self.assertEqual(app["nome"], "Visible App")
        self.assertTrue(app["showInPortal"])

    def test_get_application_by_code_returns_none_for_invalid_code(self) -> None:
        """Testa que retorna None para código inválido."""
        app = self.service.get_application_by_code("INVALID_CODE")
        self.assertIsNone(app)

    def test_singleton_pattern_works(self) -> None:
        """Testa que get_portal_authorization_service retorna singleton."""
        service1 = get_portal_authorization_service()
        service2 = get_portal_authorization_service()
        
        self.assertIs(service1, service2)
        self.assertIsInstance(service1, PortalAuthorizationService)

    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    def test_cache_is_used(self, mock_set, mock_get) -> None:
        """Testa que o cache é utilizado corretamente."""
        mock_get.return_value = True
        
        result = self.service.user_can_access_application(1, "TEST_APP")
        
        mock_get.assert_called_once()
        mock_set.assert_not_called()  # Cache hit
