"""
Testes para o sistema automatizado de permissões do acoes_pngi.
"""
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.core.cache import cache

from accounts.models import Aplicacao, Role, RolePermission, UserRole
from acoes_pngi.context_processors import acoes_permissions
from acoes_pngi.utils.permissions import (
    get_user_app_permissions,
    user_can_manage_model,
    get_model_permissions,
    clear_user_permissions_cache,
)

User = get_user_model()


class AcoesPermissionsTestCase(TestCase):
    """Testes para o sistema de permissões automatizado."""

    def setUp(self):
        """Configurar ambiente de teste."""
        # Limpar cache antes de cada teste
        cache.clear()
        
        # Usar get_or_create para evitar conflitos com dados do __init__.py
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        # Criar roles com o campo correto: aplicacao (não idaplicacao)
        self.admin_role, _ = Role.objects.get_or_create(
            nomeperfil='Admin PNGI',
            codigoperfil='ADMIN_PNGI',
            defaults={'aplicacao': self.app}
        )
        self.viewer_role, _ = Role.objects.get_or_create(
            nomeperfil='Viewer PNGI',
            codigoperfil='VIEWER_PNGI',
            defaults={'aplicacao': self.app}
        )
        
        # Criar usuários
        self.admin_user = User.objects.create_user(
            username='admin_pngi',
            email='admin@pngi.gov.br',
            password='admin123'
        )
        
        self.viewer_user = User.objects.create_user(
            username='viewer_pngi',
            email='viewer@pngi.gov.br',
            password='viewer123'
        )
        
        # Criar UserRole para vincular usuários aos roles
        UserRole.objects.create(
            user=self.admin_user,
            aplicacao=self.app,
            role=self.admin_role
        )
        
        UserRole.objects.create(
            user=self.viewer_user,
            aplicacao=self.app,
            role=self.viewer_role
        )
        
        # Criar permissões para o app acoes_pngi
        from acoes_pngi.models import Eixo, SituacaoAcao
        
        # Obter content types
        eixo_ct = ContentType.objects.get_for_model(Eixo)
        situacao_ct = ContentType.objects.get_for_model(SituacaoAcao)
        
        # Permissões para Eixo
        self.perm_add_eixo = Permission.objects.get(
            content_type=eixo_ct,
            codename='add_eixo'
        )
        self.perm_change_eixo = Permission.objects.get(
            content_type=eixo_ct,
            codename='change_eixo'
        )
        self.perm_delete_eixo = Permission.objects.get(
            content_type=eixo_ct,
            codename='delete_eixo'
        )
        self.perm_view_eixo = Permission.objects.get(
            content_type=eixo_ct,
            codename='view_eixo'
        )
        
        # Permissões para SituacaoAcao
        self.perm_view_situacao = Permission.objects.get(
            content_type=situacao_ct,
            codename='view_situacaoacao'
        )
        
        # Associar todas as permissões ao Admin
        RolePermission.objects.get_or_create(
            role=self.admin_role,
            permission=self.perm_add_eixo
        )
        RolePermission.objects.get_or_create(
            role=self.admin_role,
            permission=self.perm_change_eixo
        )
        RolePermission.objects.get_or_create(
            role=self.admin_role,
            permission=self.perm_delete_eixo
        )
        RolePermission.objects.get_or_create(
            role=self.admin_role,
            permission=self.perm_view_eixo
        )
        
        # Associar apenas view ao Viewer
        RolePermission.objects.get_or_create(
            role=self.viewer_role,
            permission=self.perm_view_eixo
        )
        RolePermission.objects.get_or_create(
            role=self.viewer_role,
            permission=self.perm_view_situacao
        )
        
        # Factory para criar requests
        self.factory = RequestFactory()
    
    def tearDown(self):
        """Limpar cache após cada teste."""
        cache.clear()
    
    def test_admin_has_all_permissions(self):
        """Admin deve ter todas as permissões."""
        request = self.factory.get('/')
        request.user = self.admin_user
        
        context = acoes_permissions(request)
        
        self.assertTrue(context['can_add_eixo'])
        self.assertTrue(context['can_change_eixo'])
        self.assertTrue(context['can_delete_eixo'])
        self.assertTrue(context['can_view_eixo'])
        self.assertTrue(context['can_manage_eixo'])  # Agregada
    
    def test_viewer_has_limited_permissions(self):
        """Viewer deve ter apenas permissão de visualização."""
        request = self.factory.get('/')
        request.user = self.viewer_user
        
        context = acoes_permissions(request)
        
        self.assertFalse(context['can_add_eixo'])
        self.assertFalse(context['can_change_eixo'])
        self.assertFalse(context['can_delete_eixo'])
        self.assertTrue(context['can_view_eixo'])
        self.assertFalse(context['can_manage_eixo'])  # Agregada
    
    def test_unauthenticated_user_no_permissions(self):
        """Usuário não autenticado não deve ter permissões."""
        from django.contrib.auth.models import AnonymousUser
        
        request = self.factory.get('/')
        request.user = AnonymousUser()
        
        context = acoes_permissions(request)
        
        self.assertFalse(context['can_add_eixo'])
        self.assertFalse(context['can_change_eixo'])
        self.assertFalse(context['can_delete_eixo'])
        self.assertFalse(context['can_view_eixo'])
    
    def test_get_user_app_permissions(self):
        """Testar função helper de permissões."""
        perms = get_user_app_permissions(self.admin_user)
        
        self.assertIn('add_eixo', perms)
        self.assertIn('change_eixo', perms)
        self.assertIn('delete_eixo', perms)
        self.assertIn('view_eixo', perms)
    
    def test_user_can_manage_model(self):
        """Testar verificação de gerenciamento de modelo."""
        # Admin pode gerenciar
        self.assertTrue(user_can_manage_model(self.admin_user, 'eixo'))
        
        # Viewer não pode gerenciar (só view)
        self.assertFalse(user_can_manage_model(self.viewer_user, 'eixo'))
    
    def test_get_model_permissions(self):
        """Testar obtenção de permissões de modelo."""
        perms = get_model_permissions(self.admin_user, 'eixo')
        
        self.assertTrue(perms['can_add'])
        self.assertTrue(perms['can_change'])
        self.assertTrue(perms['can_delete'])
        self.assertTrue(perms['can_view'])
        
        viewer_perms = get_model_permissions(self.viewer_user, 'eixo')
        self.assertFalse(viewer_perms['can_add'])
        self.assertTrue(viewer_perms['can_view'])
    
    def test_permissions_caching(self):
        """Testar cache de permissões."""
        # Primeira chamada - deve buscar do BD e cachear
        perms1 = get_user_app_permissions(self.admin_user)
        
        # Segunda chamada - deve vir do cache
        perms2 = get_user_app_permissions(self.admin_user)
        
        self.assertEqual(perms1, perms2)
        
        # Verificar que está em cache
        cache_key = f'user_permissions_{self.admin_user.id}'
        cached_perms = cache.get(cache_key)
        self.assertIsNotNone(cached_perms)
    
    def test_clear_permissions_cache(self):
        """Testar limpeza de cache."""
        # Cachear permissões
        get_user_app_permissions(self.admin_user)
        
        cache_key = f'user_permissions_{self.admin_user.id}'
        self.assertIsNotNone(cache.get(cache_key))
        
        # Limpar cache
        clear_user_permissions_cache(self.admin_user)
        
        # Verificar que foi limpo
        self.assertIsNone(cache.get(cache_key))
