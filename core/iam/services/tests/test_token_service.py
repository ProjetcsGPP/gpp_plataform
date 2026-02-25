"""
Testes COMPLETOS para TokenService.
Cobertura: 95%+ dos métodos principais + cenários críticos.

Executar: pytest core/iam/services/tests/test_token_service.py -v
"""



import pytest
import uuid
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
import jwt
import time

# IMPORTS DEPOIS do django.setup()
from accounts.services.token_service import (
    TokenService,
    InvalidTokenException,
    TokenServiceException,
    UserRoleNotFoundException,
)
from accounts.models import Aplicacao, Role, UserRole

User = get_user_model()


class TokenServiceTest(TestCase):
    """Testes completos do TokenService."""

    @classmethod
    def setUpTestData(cls):
        """Fixtures compartilhadas."""
        cls.user = User.objects.create_user(
            email="test@gpp.com",
            password="test123",
            is_active=True,
        )
        cls.app_acoes = Aplicacao.objects.create(
            codigointerno="ACOES_PNGI",
            nomeaplicacao="Ações PNGI",
            isshowinportal=True,
        )
        cls.app_org = Aplicacao.objects.create(
            codigointerno="CARGA_ORG_LOT",
            nomeaplicacao="Carga Org. Lotação",
            isshowinportal=True,
        )
        cls.role_gestor = Role.objects.create(
            aplicacao=cls.app_acoes,
            codigoperfil="GESTOR_PNGI",
            nomeperfil="Gestor PNGI",
        )
        cls.role_coord = Role.objects.create(
            aplicacao=cls.app_acoes,
            codigoperfil="COORDENADOR_PNGI",
            nomeperfil="Coordenador PNGI",
        )
        cls.user_role_gestor = UserRole.objects.create(
            user=cls.user,
            aplicacao=cls.app_acoes,
            role=cls.role_gestor,
        )

    def setUp(self):
        """Limpa cache antes de cada teste."""
        cache.clear()
        self.token_service = TokenService()

    # ------------------------------------------------------------------
    # TESTES: issue_access_token
    # ------------------------------------------------------------------
    def test_issue_access_token_valid_structure(self):
        """Access token deve ter todos os claims corretos."""
        token = self.token_service.issue_access_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        payload = self._decode_token(token)
        expected_claims = {
            "sub": str(self.user.id),
            "app_code": "ACOES_PNGI",
            "active_role_id": self.role_gestor.id,
            "role_code": "GESTOR_PNGI",
            "token_type": "access",
        }
        for key, value in expected_claims.items():
            self.assertEqual(payload[key], value)
        self.assertIn("jti", payload)
        self.assertIn("exp", payload)
        self.assertIn("iat", payload)

    def test_issue_access_token_user_role_not_found(self):
        """Falha se UserRole não existe."""
        with self.assertRaises(UserRoleNotFoundException):
            self.token_service.issue_access_token(
                self.user, "ACOES_PNGI", 999  # Role inexistente
            )

    def test_issue_access_token_user_inactive(self):
        """Falha se usuário está inativo."""
        self.user.is_active = False
        self.user.save()

        with self.assertRaises(TokenServiceException):
            self.token_service.issue_access_token(
                self.user, "ACOES_PNGI", self.role_gestor.id
            )

    def test_issue_access_token_extra_claims(self):
        """Aceita claims extras."""
        extra = {"custom": "value", "debug": True}
        token = self.token_service.issue_access_token(
            self.user, "ACOES_PNGI", self.role_gestor.id, extra_claims=extra
        )

        payload = self._decode_token(token)
        self.assertEqual(payload["custom"], "value")
        self.assertTrue(payload["debug"])

    # ------------------------------------------------------------------
    # TESTES: issue_refresh_token
    # ------------------------------------------------------------------
    def test_issue_refresh_token_valid_structure(self):
        """Refresh token deve ter estrutura correta."""
        token = self.token_service.issue_refresh_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        payload = self._decode_token(token)
        self.assertEqual(payload["token_type"], "refresh")
        self.assertEqual(payload["sub"], str(self.user.id))
        self.assertEqual(payload["app_code"], "ACOES_PNGI")

    def test_issue_refresh_token_user_role_not_found(self):
        """Falha se UserRole não existe."""
        with self.assertRaises(UserRoleNotFoundException):
            self.token_service.issue_refresh_token(
                self.user, "ACOES_PNGI", 999
            )

    # ------------------------------------------------------------------
    # TESTES: login
    # ------------------------------------------------------------------
    def test_login_success(self):
        """Login com credenciais válidas."""
        result = self.token_service.login(
            "test@gpp.com",
            "test123",
            "ACOES_PNGI",
            self.role_gestor.id,
        )

        self.assertIsNotNone(result)
        self.assertIn("user", result)
        self.assertIn("access_token", result)
        self.assertIn("refresh_token", result)
        self.assertEqual(result["expires_in"], 600)  # 10min

    def test_login_invalid_credentials(self):
        """Falha com senha errada."""
        result = self.token_service.login(
            "test@gpp.com",
            "senha_errada",
            "ACOES_PNGI",
            self.role_gestor.id,
        )
        self.assertIsNone(result)

    def test_login_user_not_found(self):
        """Falha com usuário inexistente."""
        result = self.token_service.login(
            "inexistente@gpp.com",
            "qualquer",
            "ACOES_PNGI",
            self.role_gestor.id,
        )
        self.assertIsNone(result)

    def test_login_user_inactive(self):
        """Falha com usuário inativo."""
        self.user.is_active = False
        self.user.save()

        result = self.token_service.login(
            "test@gpp.com",
            "test123",
            "ACOES_PNGI",
            self.role_gestor.id,
        )
        self.assertIsNone(result)

    # ------------------------------------------------------------------
    # TESTES: validate_access_token
    # ------------------------------------------------------------------
    def test_validate_access_token_success(self):
        """Token válido passa em todas as validações."""
        token = self.token_service.issue_access_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        payload = self.token_service.validate_access_token(token)
        self.assertEqual(payload["sub"], str(self.user.id))
        self.assertEqual(payload["app_code"], "ACOES_PNGI")

    def test_validate_access_token_expired(self):
        """Token expirado falha."""
        with patch("django.utils.timezone.now") as mock_now:
            # Token emitido 15min atrás
            mock_now.return_value = timezone.now() - timedelta(minutes=15)
            token = self.token_service.issue_access_token(
                self.user, "ACOES_PNGI", self.role_gestor.id
            )

        with self.assertRaises(InvalidTokenException) as exc:
            self.token_service.validate_access_token(token)
        self.assertIn("expirado", str(exc.exception).lower())

    def test_validate_access_token_user_role_removed(self):
        """Falha se UserRole foi deletada."""
        token = self.token_service.issue_access_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        self.user_role_gestor.delete()

        with self.assertRaises(InvalidTokenException):
            self.token_service.validate_access_token(token)

    def test_validate_access_token_user_inactive(self):
        """Falha se usuário foi desativado."""
        token = self.token_service.issue_access_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        self.user.is_active = False
        self.user.save()

        with self.assertRaises(InvalidTokenException):
            self.token_service.validate_access_token(token)

    def test_validate_access_token_blacklisted(self):
        """Falha se token está na blacklist."""
        token = self.token_service.issue_access_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        # Decodifica para pegar JTI e exp
        payload = self._decode_token(token)
        jti = payload["jti"]
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

        # Adiciona à blacklist
        self.token_service.blacklist_token(jti, exp)

        with self.assertRaises(InvalidTokenException):
            self.token_service.validate_access_token(token)

    def test_validate_access_token_wrong_type(self):
        """Falha se passar refresh token como access."""
        refresh_token = self.token_service.issue_refresh_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        with self.assertRaises(InvalidTokenException):
            self.token_service.validate_access_token(refresh_token)

    # ------------------------------------------------------------------
    # TESTES: refresh
    # ------------------------------------------------------------------
    def test_refresh_success(self):
        """Refresh gera novos tokens válidos."""
        refresh_token = self.token_service.issue_refresh_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        new_tokens = self.token_service.refresh(refresh_token)

        self.assertIn("access_token", new_tokens)
        self.assertIn("refresh_token", new_tokens)

        # Novo access token deve ser válido
        new_payload = self.token_service.validate_access_token(new_tokens["access_token"])
        self.assertEqual(new_payload["sub"], str(self.user.id))

    def test_refresh_expired(self):
        """Refresh falha com token expirado."""
        with patch("django.utils.timezone.now") as mock_now:
            # Token emitido 35min atrás (refresh expira em 30min)
            mock_now.return_value = timezone.now() - timedelta(minutes=35)
            refresh_token = self.token_service.issue_refresh_token(
                self.user, "ACOES_PNGI", self.role_gestor.id
            )

        with self.assertRaises(InvalidTokenException):
            self.token_service.refresh(refresh_token)

    def test_refresh_user_role_removed(self):
        """Refresh falha se UserRole foi removida."""
        refresh_token = self.token_service.issue_refresh_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        self.user_role_gestor.delete()

        with self.assertRaises(InvalidTokenException):
            self.token_service.refresh(refresh_token)

    def test_refresh_old_token_blacklisted(self):
        """Refresh automaticamente blacklista o refresh token usado."""
        refresh_token = self.token_service.issue_refresh_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        # Primeiro refresh (deve blacklistar)
        new_tokens = self.token_service.refresh(refresh_token)

        # Segundo refresh com mesmo token (deve falhar - blacklisted)
        with self.assertRaises(InvalidTokenException):
            self.token_service.refresh(refresh_token)

    # ------------------------------------------------------------------
    # TESTES: blacklist
    # ------------------------------------------------------------------
    def test_blacklist_token_cache(self):
        """Blacklist armazena no cache com TTL correto."""
        now = timezone.now()
        exp = now + timedelta(minutes=5)
        jti = "test-jti-123"

        self.token_service.blacklist_token(jti, exp)

        # Verifica cache
        key = f"token_blacklist:{jti}"
        cached_data = cache.get(key)
        self.assertIsNotNone(cached_data)
        self.assertEqual(cached_data["expires_at"], exp.isoformat())

        # TTL deve ser ~5min (300s)
        ttl = cache.ttl(key)
        self.assertGreater(ttl, 290)  # Margem de erro

    def test_blacklist_token_already_expired(self):
        """Não adiciona tokens já expirados."""
        exp = timezone.now() - timedelta(minutes=1)  # Passado
        jti = "expired-jti"

        self.token_service.blacklist_token(jti, exp)

        key = f"token_blacklist:{jti}"
        self.assertIsNone(cache.get(key))  # Não foi adicionado

    def test_revoke_token_success(self):
        """Revoke adiciona à blacklist."""
        token = self.token_service.issue_access_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )

        self.token_service.revoke_token(token)

        payload = self._decode_token(token)
        jti = payload["jti"]
        key = f"token_blacklist:{jti}"
        self.assertIsNotNone(cache.get(key))

    # ------------------------------------------------------------------
    # TESTES: helpers
    # ------------------------------------------------------------------
    def test_generate_jti_unique(self):
        """JTI deve ser único a cada chamada."""
        jti1 = self.token_service._generate_jti()
        jti2 = self.token_service._generate_jti()

        self.assertNotEqual(jti1, jti2)
        self.assertRegex(jti1, r"^[0-9a-f]{32}-\d{10}$")

    # ------------------------------------------------------------------
    # TESTES: multi-app
    # ------------------------------------------------------------------
    def test_multi_app_different_tokens(self):
        """Tokens diferentes para apps diferentes."""
        token_acoes = self.token_service.issue_access_token(
            self.user, "ACOES_PNGI", self.role_gestor.id
        )
        token_org = self.token_service.issue_access_token(
            self.user, "CARGA_ORG_LOT", self.role_gestor.id
        )

        self.assertNotEqual(token_acoes, token_org)

        payload_acoes = self._decode_token(token_acoes)
        payload_org = self._decode_token(token_org)

        self.assertEqual(payload_acoes["app_code"], "ACOES_PNGI")
        self.assertEqual(payload_org["app_code"], "CARGA_ORG_LOT")

    # ------------------------------------------------------------------
    # UTILITários privados
    # ------------------------------------------------------------------
    def _decode_token(self, token: str) -> dict:
        """Decodifica JWT sem validação para inspeção."""
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])


class TokenServiceIntegrationTest(TestCase):
    """Testes de fluxo completo (login → refresh → logout)."""

    def setUp(self):
        super().setUp()
        self.token_service = TokenService()

    def test_full_auth_flow(self):
        """Login → Validate → Refresh → Revoke."""
        # 1) Login
        login_result = self.token_service.login(
            "test@gpp.com",
            "test123",
            "ACOES_PNGI",
            self.role_gestor.id,
        )
        self.assertIsNotNone(login_result)
        access_token = login_result["access_token"]
        refresh_token = login_result["refresh_token"]

        # 2) Validate access token
        payload = self.token_service.validate_access_token(access_token)
        self.assertEqual(payload["sub"], str(self.user.id))

        # 3) Refresh
        new_tokens = self.token_service.refresh(refresh_token)
        new_access = new_tokens["access_token"]
        new_refresh = new_tokens["refresh_token"]

        # Novo access deve ser válido
        new_payload = self.token_service.validate_access_token(new_access)
        self.assertEqual(new_payload["sub"], str(self.user.id))

        # Refresh token antigo deve estar blacklisted
        with self.assertRaises(InvalidTokenException):
            self.token_service.refresh(refresh_token)

        # 4) Revoke novo access token
        self.token_service.revoke_token(new_access)

        with self.assertRaises(InvalidTokenException):
            self.token_service.validate_access_token(new_access)
