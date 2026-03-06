"""acoes_pngi/tests/test_diagnostic_simple.py

Teste diagnóstico simples sem imports complexos.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import get_resolver, resolve
from rest_framework.test import APIClient

from accounts.models import Aplicacao, Role, UserRole

from ..models import Acoes
from .base import BaseTestCase

User = get_user_model()


class SimpleDiagnosticTest(BaseTestCase):
    """Teste diagnóstico ultra simples"""

    databases = {"default", "gpp_plataform_db"}

    def setUp(self):
        """Setup mínimo"""
        self.client = APIClient()

        # Criar aplicação e role
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno="ACOES_PNGI", defaults={"nomeaplicacao": "Ações PNGI"}
        )

        self.role, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil="GESTOR_PNGI",
            defaults={"nomeperfil": "Gestor PNGI"},
        )

        # Criar usuário
        self.user = User.objects.create_user(
            email="simple@test.com", password="test123", name="Simple User"
        )
        UserRole.objects.create(user=self.user, aplicacao=self.app, role=self.role)

        # Criar vigência e ação
        self.acao = Acoes.objects.create(
            strapelido="ACAO-SIMPLE",
            strdescricaoacao="Ação Simples",
            strdescricaoentrega="Entrega",
            idvigenciapngi=self.vigencia_base,
            ideixo=self.eixo_base,
            idsituacaoacao=self.situacao_base,
        )

    def test_url_resolution(self):
        """Verifica se as URLs podem ser resolvidas"""
        print("\n" + "=" * 70)
        print("🔍 TESTE: URL Resolution")
        print("=" * 70)

        test_urls = [
            "/api/v1/acoes_pngi/acoes/",
            "/api/v1/acoes_pngi/acoes-prazo/",
            "/api/v1/acoes_pngi/acoes-destaque/",
        ]

        for url in test_urls:
            print(f"\n📍 Testando: {url}")
            try:
                match = resolve(url)
                print("   ✅ RESOLVIDA")
                print(f"   - View name: {match.view_name}")
                print(f"   - URL name: {match.url_name}")
                print(f"   - Namespace: {match.namespace or 'None'}")
            except Exception as e:
                print(f"   ✖ ERRO: {type(e).__name__}: {e}")
                self.fail(f"URL {url} não pode ser resolvida: {e}")

        print("\n" + "=" * 70 + "\n")

    def test_api_request_unauthenticated(self):
        """Testa requisição sem autenticação"""
        print("\n" + "=" * 70)
        print("🔍 TESTE: API Request (Unauthenticated)")
        print("=" * 70)

        response = self.client.get("/api/v1/acoes_pngi/acoes/")

        print(f"\n👉 Status: {response.status_code}")
        print(f"   Content-Type: {response.get('Content-Type', 'N/A')}")

        if response.status_code == 404:
            print("\n   🚨 PROBLEMA: URL retorna 404")
            print("   👉 Isso indica que o URLconf NÃO está sendo carregado!")
            self.fail("URL retorna 404 - URLconf não carregado corretamente")
        elif response.status_code in [401, 403]:
            print("\n   ✅ OK: Autenticação exigida (esperado)")
        else:
            print(f"\n   ⚠️  Status inesperado: {response.status_code}")

        print("\n" + "=" * 70 + "\n")


def test_api_request_authenticated(self):
    """Testa requisição com autenticação"""
    print("\n" + "=" * 70)
    print("🔍 TESTE: API Request (Authenticated)")
    print("=" * 70)

    self.client.force_authenticate(user=self.user)
    response = self.client.get("/api/v1/acoes_pngi/acoes/")

    print(f"\n👉 Status: {response.status_code}")
    print(f"   Usuário: {self.user.email}")
    print(f"   Content-Type: {response.get('Content-Type', 'N/A')}")

    if response.status_code == 404:
        print("\n   🚨 PROBLEMA CRÍTICO: URL retorna 404 mesmo autenticado!")
        print("   👉 URLconf definitivamente NÃO está carregado!")

        # Listar todas as URLs registradas
        print("\n   📍 URLs disponíveis no resolver:")
        resolver = get_resolver()

        def list_patterns(patterns, prefix="", depth=0):
            indent = "      " + "  " * depth  # ✅ DEFINIDO DENTRO DA FUNÇÃO

            for pattern in patterns:
                if hasattr(pattern, "url_patterns"):
                    new_prefix = prefix + str(pattern.pattern)
                    print(f"{indent}{new_prefix}")
                    list_patterns(pattern.url_patterns, new_prefix, depth + 1)
                elif "acoes" in str(pattern.pattern).lower():
                    full = prefix + str(pattern.pattern)
                    print(f"{indent}{full}")

            # ERRO MOVIDO PARA FORA da função list_patterns
            try:
                list_patterns(resolver.url_patterns)
            except Exception as e:
                print(f"   Erro ao listar: {e}")

        list_patterns(resolver.url_patterns)
        self.fail("URL retorna 404 - URLconf não está carregado")

    elif response.status_code == 403:
        print("\n   ⚠️  Permissão negada (403)")
        print("   Pode ser problema de permissões customizadas")

    elif response.status_code == 200:
        print("\n   ✅ SUCESSO! API está funcionando!")
        results = getattr(response.data, "results", [])
        print(f"   Total de ações: {len(results)}")

    else:
        print(f"\n   ⚠️  Status inesperado: {response.status_code}")

    print("\n" + "=" * 70 + "\n")

    def test_installed_apps(self):
        """Verifica se os apps estão instalados"""
        print("\n" + "=" * 70)
        print("🔍 TESTE: INSTALLED_APPS")
        print("=" * 70)

        required_apps = [
            "acoes_pngi",
            "rest_framework",
            "accounts",
        ]

        print("\n📦 Apps necessários:")
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                print(f"   ✅ {app}")
            else:
                print(f"   ✖ {app} - FALTANDO!")
                self.fail(f"App {app} não está em INSTALLED_APPS")

        print("\n" + "=" * 70 + "\n")
        self.assertTrue(True)
