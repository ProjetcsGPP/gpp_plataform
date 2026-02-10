"""
Testes do Sistema de Permissões - Ações PNGI
Testa as 4 classes de permissões hierárquicas.
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.views import APIView
from unittest.mock import Mock, patch

from ..permissions import (
    IsAcoesPNGIUser,
    CanViewAcoesPngi,
    CanEditAcoesPngi,
    CanManageAcoesPngi
)

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
    
    def test_edit_with_operador(self):
        """Operador pode editar"""
        permission = CanEditAcoesPngi()
        request = self.create_request_with_role('OPERADOR_ACAO')
        
        self.assertTrue(permission.has_permission(request, self.view))
    
    def test_edit_with_consultor(self):
        """Consultor NÃO pode editar"""
        permission = CanEditAcoesPngi()
        request = self.create_request_with_role('CONSULTOR_PNGI')
        
        # Consultor não está em EDIT_ROLES
        result = permission.has_permission(request, self.view)
        self.assertFalse(result)


class CanManageAcoesPngiTest(BasePermissionTest):
    """Testes da permissão CanManageAcoesPngi"""
    
    def test_manage_with_coordenador(self):
        """Coordenador pode gerenciar"""
        permission = CanManageAcoesPngi()
        request = self.create_request_with_role('COORDENADOR_PNGI')
        
        self.assertTrue(permission.has_permission(request, self.view))
    
    def test_manage_with_gestor(self):
        """Gestor pode gerenciar"""
        permission = CanManageAcoesPngi()
        request = self.create_request_with_role('GESTOR_PNGI')
        
        self.assertTrue(permission.has_permission(request, self.view))
    
    def test_manage_with_operador(self):
        """Operador NÃO pode gerenciar"""
        permission = CanManageAcoesPngi()
        request = self.create_request_with_role('OPERADOR_ACAO')
        
        # Operador não está em MANAGE_ROLES
        result = permission.has_permission(request, self.view)
        self.assertFalse(result)
    
    def test_manage_with_consultor(self):
        """Consultor NÃO pode gerenciar"""
        permission = CanManageAcoesPngi()
        request = self.create_request_with_role('CONSULTOR_PNGI')
        
        result = permission.has_permission(request, self.view)
        self.assertFalse(result)


class PermissionHierarchyTest(BasePermissionTest):
    """Testes da hierarquia de permissões"""
    
    def test_hierarchy_coordenador(self):
        """Coordenador tem todas as permissões"""
        request = self.create_request_with_role('COORDENADOR_PNGI')
        
        self.assertTrue(CanViewAcoesPngi().has_permission(request, self.view))
        self.assertTrue(CanEditAcoesPngi().has_permission(request, self.view))
        self.assertTrue(CanManageAcoesPngi().has_permission(request, self.view))
    
    def test_hierarchy_gestor(self):
        """Gestor tem view, edit e manage"""
        request = self.create_request_with_role('GESTOR_PNGI')
        
        self.assertTrue(CanViewAcoesPngi().has_permission(request, self.view))
        self.assertTrue(CanEditAcoesPngi().has_permission(request, self.view))
        self.assertTrue(CanManageAcoesPngi().has_permission(request, self.view))
    
    def test_hierarchy_operador(self):
        """Operador tem view e edit, mas não manage"""
        request = self.create_request_with_role('OPERADOR_ACAO')
        
        self.assertTrue(CanViewAcoesPngi().has_permission(request, self.view))
        self.assertTrue(CanEditAcoesPngi().has_permission(request, self.view))
        self.assertFalse(CanManageAcoesPngi().has_permission(request, self.view))
    
    def test_hierarchy_consultor(self):
        """Consultor tem apenas view"""
        request = self.create_request_with_role('CONSULTOR_PNGI')
        
        self.assertTrue(CanViewAcoesPngi().has_permission(request, self.view))
        self.assertFalse(CanEditAcoesPngi().has_permission(request, self.view))
        self.assertFalse(CanManageAcoesPngi().has_permission(request, self.view))
