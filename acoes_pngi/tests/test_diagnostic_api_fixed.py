"""acoes_pngi/tests/test_diagnostic_api.py

Teste diagnóstico para identificar a causa raiz do erro 404.

Verifica:
1. URLconf está carregada corretamente
2. Middleware de autenticação
3. Permissões
4. Acesso direto às views
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse, get_resolver
from django.conf import settings
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from datetime import date
from django.utils import timezone

from .base import BaseTestCase

from accounts.models import Aplicacao, Role, UserRole
from ..models import Acoes, VigenciaPNGI
from ..views.api_views import AcoesViewSet

User = get_user_model()


class DiagnosticAPITest(BaseTestCase):
    """Teste diagnóstico para identificar problema 404"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup básico"""
        self.client = APIClient()
        self.factory = APIRequestFactory()
        
        # Criar aplicação e role
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        self.role, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='GESTOR_PNGI',
            defaults={'nomeperfil': 'Gestor PNGI'}
        )
        
        # Criar usuário
        self.user = User.objects.create_user(
            email='diagnostic@test.com',
            password='test123',
            name='Diagnostic User'
        )
        UserRole.objects.create(user=self.user, aplicacao=self.app, role=self.role)
        
        # Criar vigência e ação        
        self.acao = Acoes.objects.create(
            strapelido='ACAO-DIAG',
            strdescricaoacao='Ação Diagnóstica',
            strdescricaoentrega='Entrega',
            idvigenciapngi=self.vigencia_base,
            ideixo=self.eixo_base,
            idsituacaoacao=self.situacao_base)
    
    def test_01_urlconf_loaded(self):
        """1. Verificar se URLconf está carregada"""
        print("\n" + "="*70)
        print("🔍 TESTE 1: URLconf Registration")
        print("="*70)
        
        # Verificar ROOT_URLCONF
        print(f"\n📋 ROOT_URLCONF: {settings.ROOT_URLCONF}")
        
        # Listar todas as URLs registradas que contém 'acoes_pngi'
        resolver = get_resolver()
        print("\n📍 URLs registradas contendo 'acoes_pngi':")
        
        def print_urls(urlpatterns, prefix=''):
            for pattern in urlpatterns:
                if hasattr(pattern, 'url_patterns'):
                    # É um include()
                    new_prefix = prefix + str(pattern.pattern)
                    if 'acoes_pngi' in new_prefix:
                        print(f"   ✓ {new_prefix}")
                    print_urls(pattern.url_patterns, new_prefix)
                else:
                    # É uma URL simples
                    full_path = prefix + str(pattern.pattern)
                    if 'acoes_pngi' in full_path:
                        print(f"   ✓ {full_path}")
        
        try:
            print_urls(resolver.url_patterns)
        except Exception as e:
            print(f"   ✖ Erro ao listar URLs: {e}")
        
        # Tentar resolver a URL manualmente
        test_urls = [
            '/api/v1/acoes_pngi/acoes/',
            '/api/v1/acoes_pngi/acoes-prazo/',
            '/api/v1/acoes_pngi/acoes-destaque/',
        ]
        
        print("\n📍 Tentando resolver URLs de teste:")
        for url in test_urls:
            try:
                match = resolve(url)
                print(f"   ✓ {url} -> {match.func.__name__} (OK)")
            except Exception as e:
                print(f"   ✖ {url} -> ERRO: {type(e).__name__}")
        
        print("\n" + "="*70 + "\n")
    
    def test_02_middleware_chain(self):
        """2. Verificar cadeia de middleware"""
        print("\n" + "="*70)
        print("🔍 TESTE 2: Middleware Chain")
        print("="*70)
        
        print("\n🔗 Middleware instalado:")
        for i, middleware in enumerate(settings.MIDDLEWARE, 1):
            print(f"   {i}. {middleware}")
            if 'auth' in middleware.lower():
                print(f"      ⚠️  Middleware de autenticação detectado")
        
        print("\n" + "="*70 + "\n")
    
    def test_03_authentication_unauthenticated(self):
        """3a. Testar acesso sem autenticação"""
        print("\n" + "="*70)
        print("🔍 TESTE 3a: Authentication (Unauthenticated)")
        print("="*70)
        
        # Sem autenticação
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/acoes_pngi/acoes/')
        
        print(f"\n🔑 Requisição sem autenticação:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Esperado: 401 (Unauthorized) ou 403 (Forbidden)")
        print(f"   Resultado: {'✅ OK' if response.status_code in [401, 403] else '✖ PROBLEMA - retornou 404'}")
        
        if response.status_code == 404:
            print(f"\n   ⚠️  PROBLEMA IDENTIFICADO: URL não encontrada!")
            print(f"   Isso significa que o URLconf NÃO está carregado corretamente.")
        
        print("\n" + "="*70 + "\n")
    
    def test_04_authentication_authenticated(self):
        """3b. Testar acesso com autenticação"""
        print("\n" + "="*70)
        print("🔍 TESTE 3b: Authentication (Authenticated)")
        print("="*70)
        
        # Com autenticação
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/acoes_pngi/acoes/')
        
        print(f"\n🔑 Requisição com autenticação:")
        print(f"   Usuário: {self.user.email}")
        print(f"   Status Code: {response.status_code}")
        print(f"   Esperado: 200 (OK) ou 403 (Forbidden)")
        print(f"   Resultado: {'✅ OK' if response.status_code in [200, 403] else '✖ PROBLEMA'}")
        
        if response.status_code == 404:
            print(f"\n   ⚠️  PROBLEMA IDENTIFICADO: URL não encontrada!")
        elif response.status_code == 403:
            print(f"\n   ⚠️  Possível problema de permissões")
        elif response.status_code == 200:
            print(f"\n   ✅ Sucesso! A API está acessível.")
            print(f"   Total de ações retornadas: {len(response.data.get('results', []))}")
        
        print("\n" + "="*70 + "\n")
    
    def test_05_direct_view_access(self):
        """4. Testar acesso direto à view (sem URLs)"""
        print("\n" + "="*70)
        print("🔍 TESTE 4: Direct View Access")
        print("="*70)
        
        # Criar requisição diretamente para a view
        request = self.factory.get('/fake-url/')
        request.user = self.user
        
        # Instanciar ViewSet
        view = AcoesViewSet.as_view({'get': 'list'})
        
        print(f"\n🎯 Chamando view diretamente:")
        try:
            response = view(request)
            print(f"   Status Code: {response.status_code}")
            print(f"   Resultado: {'✅ View funciona!' if response.status_code == 200 else '✖ View com problema'}")
            
            if response.status_code == 200:
                print(f"\n   ✅ CONCLUSÃO: A view está funcionando!")
                print(f"   O problema é na configuração de URLs.")
        except Exception as e:
            print(f"   ✖ Erro ao chamar view: {type(e).__name__}: {e}")
        
        print("\n" + "="*70 + "\n")
    
    def test_06_rest_framework_settings(self):
        """5. Verificar configurações do Django REST Framework"""
        print("\n" + "="*70)
        print("🔍 TESTE 5: REST Framework Settings")
        print("="*70)
        
        rest_settings = getattr(settings, 'REST_FRAMEWORK', {})
        
        print(f"\n⚙️  Configurações REST_FRAMEWORK:")
        
        important_keys = [
            'DEFAULT_AUTHENTICATION_CLASSES',
            'DEFAULT_PERMISSION_CLASSES',
            'DEFAULT_RENDERER_CLASSES',
            'UNAUTHENTICATED_USER',
        ]
        
        for key in important_keys:
            value = rest_settings.get(key, 'Não configurado')
            print(f"\n   {key}:")
            if isinstance(value, (list, tuple)):
                for item in value:
                    print(f"      - {item}")
            else:
                print(f"      {value}")
        
        print("\n" + "="*70 + "\n")
    
    def test_07_final_diagnosis(self):
        """6. Diagnóstico final"""
        print("\n" + "="*70)
        print("🎯 DIAGNÓSTICO FINAL")
        print("="*70)
        
        # Testar a URL problemática
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/acoes_pngi/acoes/')
        
        print(f"\n👉 Status retornado: {response.status_code}\n")
        
        if response.status_code == 404:
            print("🚨 PROBLEMA IDENTIFICADO: 404 Not Found\n")
            print("Possíveis causas:")
            print("  1. ✖ URLconf não incluída no urls.py principal")
            print("  2. ✖ Padrão de URL incorreto")
            print("  3. ✖ App não incluído em INSTALLED_APPS")
            print("  4. ✖ Problema de importação do Router")
            
            # Verificar INSTALLED_APPS
            print(f"\n📦 INSTALLED_APPS:")
            if 'acoes_pngi' in settings.INSTALLED_APPS:
                print("  ✅ 'acoes_pngi' está em INSTALLED_APPS")
            else:
                print("  ✖ 'acoes_pngi' NÃO está em INSTALLED_APPS")
            
            if 'rest_framework' in settings.INSTALLED_APPS:
                print("  ✅ 'rest_framework' está em INSTALLED_APPS")
            else:
                print("  ✖ 'rest_framework' NÃO está em INSTALLED_APPS")
        
        elif response.status_code == 403:
            print("⚠️  PROBLEMA: 403 Forbidden\n")
            print("Possíveis causas:")
            print("  1. ✖ Permissões customizadas bloqueando acesso")
            print("  2. ✖ Usuário sem role adequada")
            print("  3. ✖ Problema no sistema de permissões")
        
        elif response.status_code == 401:
            print("⚠️  PROBLEMA: 401 Unauthorized\n")
            print("Possíveis causas:")
            print("  1. ✖ Autenticação não funcionando corretamente")
            print("  2. ✖ Token inválido ou expirado")
        
        elif response.status_code == 200:
            print("✅ TUDO FUNCIONANDO PERFEITAMENTE!\n")
            print(f"Total de ações retornadas: {len(response.data.get('results', []))}")
        
        print("\n" + "="*70 + "\n")
        
        # Este teste sempre passa - é apenas diagnóstico
        self.assertTrue(True)
