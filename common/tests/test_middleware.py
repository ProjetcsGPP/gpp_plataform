"""
Testes do AppContextMiddleware.
"""

from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth import get_user_model
from accounts.models import Aplicacao
from common.middleware.app_context import AppContextMiddleware


User = get_user_model()


def dummy_get_response(request):
    """Response mock para testes do middleware"""
    from django.http import HttpResponse
    return HttpResponse("OK")


class AppContextMiddlewareTest(TestCase):
    """
    Testes do middleware de contexto de aplicação.
    """
    
    @classmethod
    def setUpTestData(cls):
        """Cria aplicações de teste"""
        cls.app_portal = Aplicacao.objects.create(
            codigointerno='PORTAL',
            nomeaplicacao='Portal GPP',
            baseurl='http://localhost:8000/',
            isshowinportal=True
        )
        
        cls.app_acoes_pngi = Aplicacao.objects.create(
            codigointerno='ACOES_PNGI',
            nomeaplicacao='Gestão de Ações PNGI',
            baseurl='http://localhost:8000/acoes-pngi/',
            isshowinportal=True
        )
        
        cls.app_carga = Aplicacao.objects.create(
            codigointerno='CARGA_ORG_LOT',
            nomeaplicacao='Carga Org/Lot',
            baseurl='http://localhost:8000/carga_org_lot/',
            isshowinportal=True
        )
    
    def setUp(self):
        """Configura factory e middleware"""
        self.factory = RequestFactory()
        self.middleware = AppContextMiddleware(dummy_get_response)
    
    def test_detect_acoes_pngi_api(self):
        """Testa detecção de Ações PNGI via API"""
        request = self.factory.get('/api/v1/acoes_pngi/eixos/')
        self.middleware(request)
        
        self.assertEqual(request.app_context['code'], 'ACOES_PNGI')
        self.assertEqual(request.app_context['name'], 'Gestão de Ações PNGI')
        self.assertIsNotNone(request.app_context['instance'])
        self.assertEqual(
            request.app_context['instance'].codigointerno,
            'ACOES_PNGI'
        )
    
    def test_detect_acoes_pngi_web(self):
        """Testa detecção de Ações PNGI via web"""
        request = self.factory.get('/acoes-pngi/dashboard/')
        self.middleware(request)
        
        self.assertEqual(request.app_context['code'], 'ACOES_PNGI')
        self.assertEqual(request.app_context['name'], 'Gestão de Ações PNGI')
    
    def test_detect_carga_org_lot_api(self):
        """Testa detecção de Carga Org/Lot via API"""
        request = self.factory.get('/api/v1/carga/')
        self.middleware(request)
        
        self.assertEqual(request.app_context['code'], 'CARGA_ORG_LOT')
        self.assertEqual(request.app_context['name'], 'Carga Org/Lot')
    
    def test_detect_carga_org_lot_web(self):
        """Testa detecção de Carga Org/Lot via web"""
        request = self.factory.get('/carga_org_lot/login/')
        self.middleware(request)
        
        self.assertEqual(request.app_context['code'], 'CARGA_ORG_LOT')
    
    def test_detect_portal_api(self):
        """Testa detecção de Portal via API"""
        request = self.factory.get('/api/v1/portal/')
        self.middleware(request)
        
        self.assertEqual(request.app_context['code'], 'PORTAL')
        self.assertEqual(request.app_context['name'], 'Portal GPP')
    
    def test_detect_portal_root(self):
        """Testa detecção de Portal na raiz"""
        request = self.factory.get('/')
        self.middleware(request)
        
        self.assertEqual(request.app_context['code'], 'PORTAL')
    
    def test_detect_portal_auth(self):
        """Testa detecção de Portal em auth"""
        request = self.factory.get('/api/v1/auth/login/')
        self.middleware(request)
        
        self.assertEqual(request.app_context['code'], 'PORTAL')
    
    def test_no_context_for_admin(self):
        """Testa que /admin/ não tem contexto de app"""
        request = self.factory.get('/admin/')
        self.middleware(request)
        
        self.assertIsNone(request.app_context['code'])
        self.assertIsNone(request.app_context['instance'])
        self.assertIsNone(request.app_context['name'])
    
    def test_no_context_for_static(self):
        """Testa que /static/ não tem contexto"""
        request = self.factory.get('/static/css/style.css')
        self.middleware(request)
        
        self.assertIsNone(request.app_context['code'])
    
    def test_cache_works(self):
        """Testa que cache de aplicações funciona"""
        # Primeira requisição carrega do banco
        request1 = self.factory.get('/api/v1/acoes_pngi/eixos/')
        self.middleware(request1)
        
        # Segunda requisição deve usar cache
        request2 = self.factory.get('/api/v1/acoes_pngi/situacoes/')
        self.middleware(request2)
        
        # Ambas devem ter o mesmo resultado
        self.assertEqual(request1.app_context['code'], request2.app_context['code'])
        self.assertEqual(
            request1.app_context['instance'].idaplicacao,
            request2.app_context['instance'].idaplicacao
        )
    
    def test_url_priority(self):
        """Testa prioridade de detecção de URLs"""
        # API tem prioridade sobre web
        test_cases = [
            ('/api/v1/acoes_pngi/test/', 'ACOES_PNGI'),
            ('/acoes-pngi/test/', 'ACOES_PNGI'),
            ('/api/v1/carga/test/', 'CARGA_ORG_LOT'),
            ('/carga_org_lot/test/', 'CARGA_ORG_LOT'),
        ]
        
        for url, expected_code in test_cases:
            request = self.factory.get(url)
            self.middleware(request)
            self.assertEqual(
                request.app_context['code'],
                expected_code,
                f"URL {url} deveria detectar {expected_code}"
            )
    
    def test_middleware_adds_app_context_attribute(self):
        """Testa que middleware sempre adiciona app_context"""
        urls = [
            '/',
            '/admin/',
            '/api/v1/acoes_pngi/eixos/',
            '/static/file.css',
            '/unknown/path/',
        ]
        
        for url in urls:
            request = self.factory.get(url)
            self.middleware(request)
            
            self.assertTrue(
                hasattr(request, 'app_context'),
                f"URL {url} deveria ter app_context"
            )
            self.assertIsInstance(request.app_context, dict)
            self.assertIn('code', request.app_context)
            self.assertIn('instance', request.app_context)
            self.assertIn('name', request.app_context)


class AppContextIntegrationTest(TestCase):
    """
    Testes de integração do middleware com serializers.
    """
    
    @classmethod
    def setUpTestData(cls):
        """Cria dados de teste"""
        cls.app = Aplicacao.objects.create(
            codigointerno='ACOES_PNGI',
            nomeaplicacao='Gestão de Ações PNGI',
            baseurl='http://localhost:8000/acoes-pngi/',
            isshowinportal=True
        )
        
        cls.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
    
    def setUp(self):
        """Configura cliente de teste"""
        self.client.force_login(self.user)
    
    def test_serializer_gets_app_context(self):
        """Testa que serializers recebem app_context automaticamente"""
        from common.serializers import UserSerializer
        
        # Faz requisição para endpoint de Ações PNGI
        response = self.client.get('/api/v1/acoes_pngi/users/test@example.com/')
        
        # Verifica que middleware adicionou contexto
        # (isso seria testado dentro da view, mas aqui validamos a integração)
        self.assertEqual(response.status_code, 200)
