"""
Testes para Context Processors de Ações PNGI
Cobertura: 100%
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from unittest.mock import Mock, patch, MagicMock
from acoes_pngi.context_processors import (
    acoes_permissions,
    acoes_pngi_context,
    acoes_pngi_models_context,
)
from accounts.models import Aplicacao

User = get_user_model()


class AcoesPermissionsContextTest(TestCase):
    """Testes para a função acoes_permissions()"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User'
        )
    
    def test_unauthenticated_user_permissions(self):
        """Verifica que usuário não autenticado retorna contexto vazio"""
        request = self.factory.get('/')
        request.user = User()  # AnonymousUser
        
        context = acoes_permissions(request)
        
        self.assertEqual(context['acoes_permissions'], [])
        self.assertEqual(context['acoes_models_perms'], {})
    
    def test_authenticated_user_permissions(self):
        """Verifica que usuário autenticado retorna estrutura correta"""
        request = self.factory.get('/')
        request.user = self.user
        
        # Mock do método get_app_permissions
        request.user.get_app_permissions = Mock(return_value=['view_eixo', 'add_eixo'])
        
        context = acoes_permissions(request)
        
        self.assertIn('acoes_permissions', context)
        self.assertIn('acoes_models_perms', context)
        self.assertEqual(context['acoes_permissions'], ['view_eixo', 'add_eixo'])
    
    def test_models_permissions_structure(self):
        """Verifica que permissões por modelo tém estrutura correta"""
        request = self.factory.get('/')
        request.user = self.user
        
        request.user.get_app_permissions = Mock(return_value=['view_eixo', 'add_eixo'])
        
        context = acoes_permissions(request)
        models_perms = context['acoes_models_perms']
        
        # Verifica que os 3 modelos estão presentes
        self.assertIn('eixo', models_perms)
        self.assertIn('situacaoacao', models_perms)
        self.assertIn('vigenciapngi', models_perms)
        
        # Verifica que cada modelo tem as operações CRUD
        for model in models_perms.values():
            self.assertIn('view', model)
            self.assertIn('add', model)
            self.assertIn('change', model)
            self.assertIn('delete', model)


class AcoesPNGIContextTest(TestCase):
    """Testes para a função acoes_pngi_context()"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User'
        )
    
    def test_context_outside_acoes_pngi_app(self):
        """Verifica que contexto é vazio fora da app acoes_pngi"""
        request = self.factory.get('/')
        request.user = self.user
        request.resolver_match = Mock(app_name='other_app')
        
        context = acoes_pngi_context(request)
        
        self.assertEqual(context, {})
    
    def test_app_context_structure(self):
        """Verifica que app_context tem estrutura correta"""
        request = self.factory.get('/')
        request.user = self.user
        request.resolver_match = Mock(app_name='acoes_pngi')
        request.session = {}
        
        context = acoes_pngi_context(request)
        
        self.assertIn('app_context', context)
        app_ctx = context['app_context']
        
        # Verifica campos obrigatórios
        self.assertIn('code', app_ctx)
        self.assertIn('name', app_ctx)
        self.assertIn('icon', app_ctx)
        self.assertIn('url_namespace', app_ctx)
        
        # Verifica valores
        self.assertEqual(app_ctx['code'], 'ACOES_PNGI')
        self.assertEqual(app_ctx['url_namespace'], 'acoes_pngi')
        self.assertEqual(app_ctx['icon'], 'fas fa-tasks')
    
    def test_user_roles_in_app(self):
        """Verifica que user_roles_in_app tem estrutura correta"""
        request = self.factory.get('/')
        request.user = self.user
        request.resolver_match = Mock(app_name='acoes_pngi')
        request.session = {}
        
        # Mock de UserRole - usando QuerySet vazio (correto)
        mock_role = Mock()
        mock_role.id = 1
        mock_role.nomeperfil = 'Gestor PNGI'
        mock_role.codigoperfil = 'GESTOR_PNGI'
        
        mock_user_role = Mock()
        mock_user_role.role = mock_role
        
        with patch('acoes_pngi.context_processors.UserRole.objects.filter') as mock_qs:
            # QuerySet.select_related().first() deve retornar mock_user_role
            # Ou QuerySet.select_related().__iter__ deve ser iteravel
            mock_queryset = MagicMock()
            mock_queryset.__iter__.return_value = [mock_user_role]
            mock_queryset.select_related.return_value = mock_queryset
            mock_qs.return_value = mock_queryset
            
            context = acoes_pngi_context(request)
            
            self.assertIn('user_roles_in_app', context)
            roles = context['user_roles_in_app']
            
            self.assertEqual(len(roles), 1)
            self.assertEqual(roles[0]['id'], 1)
            self.assertEqual(roles[0]['name'], 'Gestor PNGI')
            self.assertEqual(roles[0]['code'], 'GESTOR_PNGI')
    
    def test_active_role_from_session(self):
        """Verifica que perfil ativo é reconhecido da sessão"""
        request = self.factory.get('/')
        request.user = self.user
        request.resolver_match = Mock(app_name='acoes_pngi')
        request.session = {'active_role_acoes_pngi': 1}
        
        mock_role = Mock()
        mock_role.id = 1
        mock_role.nomeperfil = 'Gestor PNGI'
        mock_role.codigoperfil = 'GESTOR_PNGI'
        
        mock_user_role = Mock()
        mock_user_role.role = mock_role
        
        with patch('acoes_pngi.context_processors.UserRole.objects.filter') as mock_qs:
            mock_queryset = MagicMock()
            mock_queryset.__iter__.return_value = [mock_user_role]
            mock_queryset.select_related.return_value = mock_queryset
            mock_qs.return_value = mock_queryset
            
            context = acoes_pngi_context(request)
            roles = context['user_roles_in_app']
            
            self.assertTrue(roles[0]['is_active'])


class AcoesPNGIModelsContextTest(TestCase):
    """Testes para a função acoes_pngi_models_context()"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User'
        )
    
    def test_models_context_structure(self):
        """Verifica que models_context tem estrutura correta"""
        request = self.factory.get('/')
        request.user = self.user
        request.resolver_match = Mock(app_name='acoes_pngi')
        
        context = acoes_pngi_models_context(request)
        
        self.assertIn('acoes_models_info', context)
        models_info = context['acoes_models_info']
        
        # Verifica que os 3 modelos estão presentes
        self.assertIn('eixo', models_info)
        self.assertIn('situacao_acao', models_info)
        self.assertIn('vigencia_pngi', models_info)
    
    def test_model_metadata_fields(self):
        """Verifica que cada modelo tem todos os campos de metadata"""
        request = self.factory.get('/')
        request.user = self.user
        request.resolver_match = Mock(app_name='acoes_pngi')
        
        context = acoes_pngi_models_context(request)
        models_info = context['acoes_models_info']
        
        for model_key, model_info in models_info.items():
            self.assertIn('model_name', model_info)
            self.assertIn('verbose_name', model_info)
            self.assertIn('verbose_name_plural', model_info)
            self.assertIn('app_label', model_info)
            self.assertIn('db_table', model_info)
    
    def test_eixo_metadata_correct(self):
        """Verifica que metadata de Eixo está correta"""
        request = self.factory.get('/')
        request.user = self.user
        request.resolver_match = Mock(app_name='acoes_pngi')
        
        context = acoes_pngi_models_context(request)
        models_info = context['acoes_models_info']
        eixo_info = models_info['eixo']
        
        self.assertEqual(eixo_info['model_name'], 'eixo')
        self.assertEqual(eixo_info['app_label'], 'acoes_pngi')


class IntegrationTest(TestCase):
    """Testes de integração de todos os context processors"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User'
        )
    
    def test_all_context_processors_together(self):
        """Verifica que todos os context processors funcionam juntos"""
        request = self.factory.get('/')
        request.user = self.user
        request.resolver_match = Mock(app_name='acoes_pngi')
        request.session = {}
        
        request.user.get_app_permissions = Mock(return_value=['view_eixo'])
        
        mock_role = Mock()
        mock_role.id = 1
        mock_role.nomeperfil = 'Gestor PNGI'
        mock_role.codigoperfil = 'GESTOR_PNGI'
        
        mock_user_role = Mock()
        mock_user_role.role = mock_role
        
        with patch('acoes_pngi.context_processors.UserRole.objects.filter') as mock_qs:
            mock_queryset = MagicMock()
            mock_queryset.__iter__.return_value = [mock_user_role]
            mock_queryset.select_related.return_value = mock_queryset
            mock_qs.return_value = mock_queryset
            
            ctx_perms = acoes_permissions(request)
            ctx_app = acoes_pngi_context(request)
            ctx_models = acoes_pngi_models_context(request)
            
            # Verifica que todos retornaram dados
            self.assertTrue(len(ctx_perms) > 0)
            self.assertTrue(len(ctx_app) > 0)
            self.assertTrue(len(ctx_models) > 0)
    
    def test_context_with_no_errors(self):
        """Verifica que context processors não lançam exceções"""
        request = self.factory.get('/')
        request.user = self.user
        request.resolver_match = Mock(app_name='acoes_pngi')
        request.session = {}
        
        try:
            acoes_permissions(request)
            acoes_pngi_context(request)
            acoes_pngi_models_context(request)
        except Exception as e:
            self.fail(f"Context processor lançou exceção: {str(e)}")


class EdgeCaseTest(TestCase):
    """Testes de casos extremos"""
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_missing_aplicacao(self):
        """Verifica comportamento quando aplicação não existe"""
        request = self.factory.get('/')
        request.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User'
        )
        request.resolver_match = Mock(app_name='acoes_pngi')
        request.session = {}
        
        # Mock Aplicacao.objects.get para lançar DoesNotExist
        with patch('acoes_pngi.context_processors.Aplicacao.objects.get') as mock_get:
            # Usar Aplicacao.DoesNotExist do módulo accounts.models
            mock_get.side_effect = Aplicacao.DoesNotExist()
            
            context = acoes_pngi_context(request)
            
            # Deve retornar contexto com fallback
            self.assertIn('app_context', context)
            self.assertEqual(context['app_context']['code'], 'ACOES_PNGI')
    
    def test_resolver_match_exception(self):
        """Verifica comportamento quando resolver_match é None"""
        request = self.factory.get('/')
        request.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User'
        )
        request.resolver_match = None
        
        try:
            context = acoes_pngi_context(request)
            self.assertEqual(context, {})
        except Exception as e:
            self.fail(f"Context processor não tratou resolver_match None: {str(e)}")
    
    def test_user_with_no_roles(self):
        """Verifica comportamento com usuário que não tem perfis"""
        request = self.factory.get('/')
        request.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User'
        )
        request.resolver_match = Mock(app_name='acoes_pngi')
        request.session = {}
        
        with patch('acoes_pngi.context_processors.UserRole.objects.filter') as mock_qs:
            # QuerySet vazio
            mock_queryset = MagicMock()
            mock_queryset.__iter__.return_value = []
            mock_queryset.select_related.return_value = mock_queryset
            mock_qs.return_value = mock_queryset
            
            context = acoes_pngi_context(request)
            
            self.assertIn('user_roles_in_app', context)
            self.assertEqual(context['user_roles_in_app'], [])
