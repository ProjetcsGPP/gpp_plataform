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
    
    def test_permission_granted_with_role(self):
        """Testa permissão concedida para usuário com role"""
        request = self.factory.get('/api/v1/acoes_pngi/')
        request.user = self.user_with_permission
        
        # Simula middleware
        request.app_context = {
            'code': 'ACOES_PNGI',
            'instance': self.app,
            'name': 'Gestão de Ações PNGI'
        }
        
        has_permission = self.permission.has_permission(request, None)
        self.assertTrue(has_permission)
    
    def test_permission_denied_without_role(self):
        """Testa permissão negada para usuário sem role"""
        request = self.factory.get('/api/v1/acoes_pngi/')
        request.user = self.user_without_permission
        
        request.app_context = {
            'code': 'ACOES_PNGI',
            'instance': self.app,
            'name': 'Gestão de Ações PNGI'
        }
        
        has_permission = self.permission.has_permission(request, None)
        self.assertFalse(has_permission)
