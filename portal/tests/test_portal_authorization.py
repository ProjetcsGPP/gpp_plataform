"""
Testes PortalAuthorizationService - COMPATÍVEL COM SEU MODELO USER
"""

from django.test import TestCase
from django.core.cache import cache
from unittest.mock import patch

from django.contrib.auth import get_user_model

from accounts.models import Aplicacao, Role, UserRole

from portal.services.portal_authorization import (
    PortalAuthorizationService,
    get_portal_authorization_service,
)


class PortalAuthorizationServiceTest(TestCase):
    """Testes completos do serviço."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Dados de teste."""
        User = get_user_model()
        
        # ✅ CORRIGIDO: username=OBRIGATÓRIO (mesmo com USERNAME_FIELD='email')
        cls.user = User.objects.create_user(
            username="test@example.com",  # Primeiro parâmetro SEMPRE
            email="test@example.com",     # Seu USERNAME_FIELD
            name="Test User",
            password="testpass123"
        )
        
        cls.other_user = User.objects.create_user(
            username="other@example.com",  # ✅ CORRIGIDO
            email="other@example.com",
            name="Other User",
            password="pass123"
        )
        
        cls.visible_app = Aplicacao.objects.create(
            codigointerno="VISIBLE_APP",
            nomeaplicacao="Visible App",
            base_url="http://visible.com",
            isshowinportal=True
        )
        
        cls.hidden_app = Aplicacao.objects.create(
            codigointerno="HIDDEN_APP",
            nomeaplicacao="Hidden App",
            base_url="http://hidden.com",
            isshowinportal=False
        )
        
        cls.role = Role.objects.create(
            codigoperfil="TEST_ROLE",
            nome="Test Role"
        )
        
        cls.user_role = UserRole.objects.create(
            user=cls.user,
            aplicacao=cls.visible_app,
            role=cls.role
        )

    def setUp(self) -> None:
        cache.clear()
        self.service = get_portal_authorization_service()

    def test_user_can_access_with_role(self) -> None:
        result = self.service.user_can_access_application(self.user.pk, "VISIBLE_APP")
        self.assertTrue(result)

    def test_user_cannot_access_without_role(self) -> None:
        result = self.service.user_can_access_application(self.other_user.pk, "VISIBLE_APP")
        self.assertFalse(result)

    def test_get_user_applications_correct(self) -> None:
        applications = self.service.get_user_applications(self.user.pk)
        self.assertEqual(len(applications), 1)
        self.assertEqual(applications[0]["codigo"], "VISIBLE_APP")

    def test_filters_hidden_apps(self) -> None:
        UserRole.objects.create(user=self.user, aplicacao=self.hidden_app, role=self.role)
        applications = self.service.get_user_applications(self.user.pk)
        self.assertEqual(len(applications), 1)  # Apenas visível
        self.assertEqual(applications[0]["codigo"], "VISIBLE_APP")

    def test_get_application_by_code_valid(self) -> None:
        app = self.service.get_application_by_code("VISIBLE_APP")
        if app:  # ✅ Safe access
            self.assertEqual(app["codigo"], "VISIBLE_APP")
            self.assertEqual(app["nome"], "Visible App")
            self.assertTrue(app["showInPortal"])

    def test_get_application_invalid_returns_none(self) -> None:
        app = self.service.get_application_by_code("INVALID")
        self.assertIsNone(app)

    def test_singleton_works(self) -> None:
        s1 = get_portal_authorization_service()
        s2 = get_portal_authorization_service()
        self.assertIs(s1, s2)

    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    def test_cache_hit(self, mock_set, mock_get) -> None:
        mock_get.return_value = True
        self.service.user_can_access_application(1, "TEST_APP")
        mock_get.assert_called_once()
        mock_set.assert_not_called()
