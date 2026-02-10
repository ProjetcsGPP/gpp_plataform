"""
Testes de permissões de Acoes PNGI.
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.views import APIView
from unittest.mock import Mock, patch

from ..permissions import IsAcoesPNGIUser

User = get_user_model()


class BasePermissionTest(TestCase):
    """Classe base para testes de permissões"""
    
    def setUp(self):
        """Setup inicial para testes"""
        self.factory = APIRequestFactory()
        self.view = APIView()
        
        # Criar usuário de teste
        self.user = User.objects.create_user(
            email="teste@seger.es.gov.br",
            name="Usuário Teste",
            password="senha123"
        )
    
    def create_request_with_role(self, role_code):
        """Cria request com role específico no token JWT"""
        request = self.factory.get('/')
        request.user = self.user
        
        # Simular token JWT com role
        request.auth = Mock()
        request.auth.payload = {
            'roles': [role_code],
            'aplicacao': 'ACOES_PNGI'
        }
        
        return request


class IsAcoesPNGIUserTest(BasePermissionTest):
    """Testes da permissão base IsAcoesPNGIUser"""
    
    def test_permission_with_valid_role(self):
        """Teste com role válido"""
        permission = IsAcoesPNGIUser()
        request = self.create_request_with_role('GESTOR_PNGI')
        
        self.assertTrue(permission.has_permission(request, self.view))
    
    def test_permission_coordenador(self):
        """Teste com role COORDENADOR_PNGI"""
        permission = IsAcoesPNGIUser()
        request = self.create_request_with_role('COORDENADOR_PNGI')
        
        self.assertTrue(permission.has_permission(request, self.view))
    
    def test_permission_consultor(self):
        """Teste com role CONSULTOR_PNGI"""
        permission = IsAcoesPNGIUser()
        request = self.create_request_with_role('CONSULTOR_PNGI')
        
        self.assertTrue(permission.has_permission(request, self.view))
    
    def test_permission_without_role(self):
        """Teste sem role válido"""
        permission = IsAcoesPNGIUser()
        request = self.factory.get('/')
        request.user = self.user
        request.auth = Mock()
        request.auth.payload = {'roles': []}
        
        # Deve tentar fallback no banco (sem mockar, deve falhar)
        result = permission.has_permission(request, self.view)
        self.assertFalse(result)


class CanViewAcoesPngiTest(BasePermissionTest):
    """Testes da permissão CanViewAcoesPngi"""
    
    def test_view_with_gestor(self):
        """Gestor pode visualizar"""
        permission = CanViewAcoesPngi()
        request = self.create_request_with_role('GESTOR_PNGI')
        
        self.assertTrue(permission.has_permission(request, self.view))
    
    def test_view_with_consultor(self):
        """Consultor pode visualizar"""
        permission = CanViewAcoesPngi()
        request = self.create_request_with_role('CONSULTOR_PNGI')
        
        self.assertTrue(permission.has_permission(request, self.view))
    
    def test_view_with_operador(self):
        """Operador pode visualizar"""
        permission = CanViewAcoesPngi()
        request = self.create_request_with_role('OPERADOR_ACAO')
        
        self.assertTrue(permission.has_permission(request, self.view))


class CanEditAcoesPngiTest(BasePermissionTest):
    """Testes da permissão CanEditAcoesPngi"""
    
    def test_edit_with_coordenador(self):
        """Coordenador pode editar"""
        permission = CanEditAcoesPngi()
        request = self.create_request_with_role('COORDENADOR_PNGI')
        
        self.assertTrue(permission.has_permission(request, self.view))
    
    def test_edit_with_gestor(self):
        """Gestor pode editar"""
        permission = CanEditAcoesPngi()
        request = self.create_request_with_role('GESTOR_PNGI')
        
        self.assertTrue(permission.has_permission(request, self.view))
    
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
