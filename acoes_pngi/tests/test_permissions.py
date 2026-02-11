"""
Testes de permissões de Acoes PNGI.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from unittest.mock import Mock

from ..permissions import IsAcoesPNGIUser, CanViewAcoesPngi, CanEditAcoesPngi

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
        
        # Simular token JWT com role - formato esperado pela permissão
        roles_list = [{
            'application__code': 'ACOES_PNGI',
            'role__code': role_code
        }]
        
        request.auth = Mock()
        request.auth.payload = {
            'roles': roles_list,
            'aplicacao': 'ACOES_PNGI'
        }
        # Garantir que ao acessar request.auth['roles'] retorne a lista de dicts
        request.auth.__getitem__ = Mock(return_value=roles_list)
        request.auth.get = Mock(side_effect=lambda key, default=None: {
            'roles': roles_list,
            'aplicacao': 'ACOES_PNGI'
        }.get(key, default))
        
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
        
        # Mock sem roles válidas
        roles_list = []
        request.auth = Mock()
        request.auth.payload = {'roles': roles_list}
        request.auth.__getitem__ = Mock(return_value=roles_list)
        request.auth.get = Mock(side_effect=lambda key, default=None: {
            'roles': roles_list,
            'aplicacao': 'ACOES_PNGI'
        }.get(key, default))
        
        # Deve tentar fallback no banco (sem mockar, deve falhar)
        result = permission.has_permission(request, self.view)
        self.assertFalse(result)
    
    def test_permission_with_wrong_application(self):
        """Teste com role de outra aplicação"""
        permission = IsAcoesPNGIUser()
        request = self.factory.get('/')
        request.user = self.user
        
        # Role de outra aplicação
        roles_list = [{
            'application__code': 'OUTRA_APP',
            'role__code': 'GESTOR_PNGI'
        }]
        request.auth = Mock()
        request.auth.payload = {'roles': roles_list}
        request.auth.__getitem__ = Mock(return_value=roles_list)
        request.auth.get = Mock(side_effect=lambda key, default=None: {
            'roles': roles_list
        }.get(key, default))
        
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
    
    def test_view_with_coordenador(self):
        """Coordenador pode visualizar"""
        permission = CanViewAcoesPngi()
        request = self.create_request_with_role('COORDENADOR_PNGI')
        
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
    
    def test_edit_with_consultor_should_fail(self):
        """Consultor NÃO pode editar"""
        permission = CanEditAcoesPngi()
        request = self.create_request_with_role('CONSULTOR_PNGI')
        
        self.assertFalse(permission.has_permission(request, self.view))
    
    def test_permission_class_exists(self):
        """Testa que classe de permissão existe"""
        permission = CanEditAcoesPngi()
        self.assertIsNotNone(permission)
        self.assertTrue(hasattr(permission, 'has_permission'))
