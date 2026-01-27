"""
Testes de permissões de Acoes PNGI.
"""

from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory
from accounts.models import User, Aplicacao, Role, UserRole
from acoes_pngi.permissions import IsAcoesPNGIUser


class IsAcoesPNGIUserPermissionTest(TestCase):
    """Testes da permissão IsAcoesPNGIUser"""
    
    databases = {'default'}
    
    @classmethod
    def setUpTestData(cls):
        """Cria dados de teste"""
        # Usar get_or_create para evitar conflito com setup
        cls.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={
                'nomeaplicacao': 'Gestão de Ações PNGI',
                'isshowinportal': True
            }
        )
        
        cls.role, _ = Role.objects.get_or_create(
            codigoperfil='GESTOR_PNGI',
            aplicacao=cls.app,
            defaults={'nomeperfil': 'Gestor PNGI'}
        )
        
        cls.user_with_permission = User.objects.create_user(
            email='gestor@example.com',
            name='Gestor User',
            password='testpass123'
        )
        
        UserRole.objects.create(
            user=cls.user_with_permission,
            role=cls.role,
            aplicacao=cls.app
        )
        
        cls.user_without_permission = User.objects.create_user(
            email='user@example.com',
            name='Regular User',
            password='testpass123'
        )
    
    def setUp(self):
        """Configura factory"""
        self.factory = APIRequestFactory()
        self.permission = IsAcoesPNGIUser()
    
    def test_permission_class_exists(self):
        """Testa que classe de permissão existe"""
        self.assertIsNotNone(self.permission)
        self.assertTrue(hasattr(self.permission, 'has_permission'))
    
    def test_user_with_role_exists(self):
        """Testa que usuário com role foi criado corretamente"""
        user_roles = UserRole.objects.filter(
            user=self.user_with_permission,
            aplicacao=self.app
        )
        self.assertTrue(user_roles.exists())
        self.assertEqual(user_roles.first().role.codigoperfil, 'GESTOR_PNGI')
    
    def test_user_without_role_has_no_permissions(self):
        """Testa que usuário sem role não tem UserRole"""
        user_roles = UserRole.objects.filter(
            user=self.user_without_permission,
            aplicacao=self.app
        )
        self.assertFalse(user_roles.exists())
