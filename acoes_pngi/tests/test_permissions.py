"""
Testes para o sistema de permissões automatizado.
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from accounts.models import Role, UserRole, RolePermission, Aplicacao
from acoes_pngi.context_processors import acoes_permissions, get_user_app_permissions
from acoes_pngi.utils.permissions import (
    get_user_permissions_cached,
    user_can_manage_model,
    get_model_permissions,
    clear_user_permissions_cache
)
from acoes_pngi.models import Eixo

User = get_user_model()


class AcoesPermissionsTestCase(TestCase):
    """Testes para context processor de permissões."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar aplicação
        self.app = Aplicacao.objects.create(
            nomeaplicacao='Ações PNGI',
            codigointerno='ACOES_PNGI'
        )
        
        # Criar roles
        self.admin_role = Role.objects.create(
            nomeperfil='Administrador PNGI',
            codigoperfil='ADMIN_PNGI',
            aplicacao=self.app
        )
        
        self.viewer_role = Role.objects.create(
            nomeperfil='Visualizador PNGI',
            codigoperfil='VIEWER_PNGI',
            aplicacao=self.app
        )
        
        # Obter content type de Eixo
        eixo_ct = ContentType.objects.get_for_model(Eixo)
        
        # Criar permissões
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
        
        # Atribuir todas as permissões ao admin
        for perm in [self.perm_add_eixo, self.perm_change_eixo, 
                     self.perm_delete_eixo, self.perm_view_eixo]:
            RolePermission.objects.create(
                role=self.admin_role,
                permission=perm
            )
        
        # Atribuir apenas view ao viewer
        RolePermission.objects.create(
            role=self.viewer_role,
            permission=self.perm_view_eixo
        )
        
        # Criar usuários
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='test123',
            cpf='12345678901'
        )
        
        self.viewer_user = User.objects.create_user(
            email='viewer@test.com',
            password='test123',
            cpf='98765432100'
        )
        
        # Atribuir roles
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
        
        self.factory = RequestFactory()
    
    def test_admin_has_all_permissions(self):
        """Admin deve ter todas as permissões."""
        request = self.factory.get('/')
        request.user = self.admin_user
        
        context = acoes_permissions(request)
        
        self.assertTrue(context['has_acoes_access'])
        self.assertEqual(context['acoes_role'], 'ADMIN_PNGI')
        self.assertTrue(context['can_add_eixo'])
        self.assertTrue(context['can_change_eixo'])
        self.assertTrue(context['can_delete_eixo'])
        self.assertTrue(context['can_view_eixo'])
        self.assertTrue(context['can_manage_eixo'])
        self.assertTrue(context['can_full_eixo'])
    
    def test_viewer_has_limited_permissions(self):
        """Viewer deve ter apenas permissão de visualização."""
        request = self.factory.get('/')
        request.user = self.viewer_user
        
        context = acoes_permissions(request)
        
        self.assertTrue(context['has_acoes_access'])
        self.assertEqual(context['acoes_role'], 'VIEWER_PNGI')
        self.assertFalse(context.get('can_add_eixo', False))
        self.assertFalse(context.get('can_change_eixo', False))
        self.assertFalse(context.get('can_delete_eixo', False))
        self.assertTrue(context['can_view_eixo'])
        self.assertFalse(context.get('can_manage_eixo', False))
        self.assertFalse(context.get('can_full_eixo', False))
    
    def test_unauthenticated_user_no_permissions(self):
        """Usuário não autenticado não deve ter permissões."""
        from django.contrib.auth.models import AnonymousUser
        
        request = self.factory.get('/')
        request.user = AnonymousUser()
        
        context = acoes_permissions(request)
        
        self.assertFalse(context['has_acoes_access'])
        self.assertIsNone(context['acoes_role'])
    
    def test_get_user_app_permissions(self):
        """Testar função helper de permissões."""
        perms = get_user_app_permissions(self.admin_user, 'ACOES_PNGI')
        
        self.assertIn('add_eixo', perms)
        self.assertIn('change_eixo', perms)
        self.assertIn('delete_eixo', perms)
        self.assertIn('view_eixo', perms)
        self.assertEqual(len(perms), 4)
    
    def test_permissions_caching(self):
        """Testar cache de permissões."""
        # Primeira chamada - deve buscar do BD
        perms1 = get_user_permissions_cached(self.admin_user)
        
        # Segunda chamada - deve buscar do cache
        perms2 = get_user_permissions_cached(self.admin_user)
        
        self.assertEqual(perms1, perms2)
        self.assertEqual(len(perms1), 4)
    
    def test_clear_permissions_cache(self):
        """Testar limpeza de cache."""
        # Popular cache
        get_user_permissions_cached(self.admin_user)
        
        # Limpar cache
        clear_user_permissions_cache(self.admin_user)
        
        # Verificar que busca novamente do BD
        perms = get_user_permissions_cached(self.admin_user)
        self.assertEqual(len(perms), 4)
    
    def test_user_can_manage_model(self):
        """Testar verificação de gerenciamento de modelo."""
        self.assertTrue(user_can_manage_model(self.admin_user, 'eixo'))
        self.assertFalse(user_can_manage_model(self.viewer_user, 'eixo'))
    
    def test_get_model_permissions(self):
        """Testar obtenção de permissões de modelo."""
        perms = get_model_permissions(self.admin_user, 'eixo')
        
        self.assertTrue(perms['can_add'])
        self.assertTrue(perms['can_change'])
        self.assertTrue(perms['can_delete'])
        self.assertTrue(perms['can_view'])
        self.assertTrue(perms['can_manage'])
