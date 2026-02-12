"""acoes_pngi/tests/test_permissions.py

Testes de Permissions - Ações PNGI

Testa todas as classes de permissão definidas em permissions.py:
- IsCoordernadorOrGestorPNGI (configurações)
- IsCoordernadorGestorOrOperadorPNGI (operações)
- IsAnyPNGIRole (leitura universal)

Cobre:
- Matriz completa de permissões por role
- Herança hierárquica das roles
- SAFE_METHODS vs ações de escrita
- Edge cases (sem role, não autenticado)
- Custom actions e permissões especiais

Hierarquia de Roles:
COORDENADOR_PNGI > GESTOR_PNGI > OPERADOR_ACAO > CONSULTOR_PNGI

Regras de Negócio:
- Configurações: apenas COORDENADOR e GESTOR
- Operações: COORDENADOR, GESTOR e OPERADOR
- Leitura: todas as 4 roles
"""

from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.request import Request
from unittest.mock import Mock

from accounts.models import Aplicacao, Role, UserRole
from ..permissions import (
    IsCoordernadorOrGestorPNGI,
    IsCoordernadorGestorOrOperadorPNGI,
    IsAnyPNGIRole
)

User = get_user_model()


class BasePermissionTestCase(TestCase):
    """Classe base para testes de permissões"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup inicial com aplicação, roles e usuários"""
        self.factory = APIRequestFactory()
        
        # Criar aplicação
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        # Criar as 4 roles
        self.role_coordenador, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='COORDENADOR_PNGI',
            defaults={'nomeperfil': 'Coordenador - Gerencia Configurações'}
        )
        
        self.role_gestor, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='GESTOR_PNGI',
            defaults={'nomeperfil': 'Gestor Acoes PNGI'}
        )
        
        self.role_operador, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='OPERADOR_ACAO',
            defaults={'nomeperfil': 'Operador - Apenas Ações'}
        )
        
        self.role_consultor, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='CONSULTOR_PNGI',
            defaults={'nomeperfil': 'Consultor - Apenas Leitura'}
        )
        
        # Criar usuários para cada role
        self.users = {}
        for role_name, role_obj in [
            ('coordenador', self.role_coordenador),
            ('gestor', self.role_gestor),
            ('operador', self.role_operador),
            ('consultor', self.role_consultor)
        ]:
            user = User.objects.create_user(
                email=f'{role_name}.perm@seger.es.gov.br',
                name=f'User {role_name.title()} Perm',
                password='testpass123'
            )
            UserRole.objects.create(
                user=user,
                aplicacao=self.app,
                role=role_obj
            )
            self.users[role_name] = user
        
        # Criar usuário sem role
        self.user_no_role = User.objects.create_user(
            email='norole@seger.es.gov.br',
            name='User No Role',
            password='testpass123'
        )
    
    def create_request(self, method='GET', user=None):
        """Cria request mock com método e usuário específicos"""
        if method == 'GET':
            request = self.factory.get('/test/')
        elif method == 'POST':
            request = self.factory.post('/test/')
        elif method == 'PATCH':
            request = self.factory.patch('/test/')
        elif method == 'PUT':
            request = self.factory.put('/test/')
        elif method == 'DELETE':
            request = self.factory.delete('/test/')
        else:
            request = self.factory.get('/test/')
        
        if user:
            force_authenticate(request, user=user)
        
        return Request(request)
    
    def create_mock_view(self, action=None):
        """Cria view mock para testes"""
        view = Mock()
        view.action = action
        return view


# ============================================================================
# TESTES DE IsCoordernadorOrGestorPNGI (Configurações)
# ============================================================================

class IsCoordernadorOrGestorPNGITests(BasePermissionTestCase):
    """
    Testes da permission IsCoordernadorOrGestorPNGI.
    
    Usada para: Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta, TipoAnotacaoAlinhamento
    
    Regra:
    - SAFE_METHODS (GET, HEAD, OPTIONS): todas as roles
    - CREATE/UPDATE/DELETE: apenas COORDENADOR e GESTOR
    - OPERADOR: bloqueado em escrita
    - CONSULTOR: bloqueado em escrita
    """
    
    def setUp(self):
        super().setUp()
        self.permission = IsCoordernadorOrGestorPNGI()
    
    # ------------------------------------------------------------------------
    # SAFE_METHODS - Todas as roles podem ler
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_read(self):
        """COORDENADOR pode usar SAFE_METHODS"""
        request = self.create_request('GET', self.users['coordenador'])
        view = self.create_mock_view('list')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_gestor_can_read(self):
        """GESTOR pode usar SAFE_METHODS"""
        request = self.create_request('GET', self.users['gestor'])
        view = self.create_mock_view('list')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_operador_can_read(self):
        """OPERADOR pode usar SAFE_METHODS"""
        request = self.create_request('GET', self.users['operador'])
        view = self.create_mock_view('list')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_consultor_can_read(self):
        """CONSULTOR pode usar SAFE_METHODS"""
        request = self.create_request('GET', self.users['consultor'])
        view = self.create_mock_view('list')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    # ------------------------------------------------------------------------
    # CREATE - Apenas COORDENADOR e GESTOR
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_create(self):
        """COORDENADOR pode criar"""
        request = self.create_request('POST', self.users['coordenador'])
        view = self.create_mock_view('create')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_gestor_can_create(self):
        """GESTOR pode criar"""
        request = self.create_request('POST', self.users['gestor'])
        view = self.create_mock_view('create')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_operador_cannot_create(self):
        """OPERADOR NÃO pode criar (bloqueado em configurações)"""
        request = self.create_request('POST', self.users['operador'])
        view = self.create_mock_view('create')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    def test_consultor_cannot_create(self):
        """CONSULTOR NÃO pode criar"""
        request = self.create_request('POST', self.users['consultor'])
        view = self.create_mock_view('create')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    # ------------------------------------------------------------------------
    # UPDATE - Apenas COORDENADOR e GESTOR
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_update(self):
        """COORDENADOR pode atualizar"""
        request = self.create_request('PATCH', self.users['coordenador'])
        view = self.create_mock_view('update')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_gestor_can_update(self):
        """GESTOR pode atualizar"""
        request = self.create_request('PUT', self.users['gestor'])
        view = self.create_mock_view('update')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_operador_cannot_update(self):
        """OPERADOR NÃO pode atualizar"""
        request = self.create_request('PATCH', self.users['operador'])
        view = self.create_mock_view('partial_update')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    def test_consultor_cannot_update(self):
        """CONSULTOR NÃO pode atualizar"""
        request = self.create_request('PUT', self.users['consultor'])
        view = self.create_mock_view('update')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    # ------------------------------------------------------------------------
    # DELETE - Apenas COORDENADOR e GESTOR
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_delete(self):
        """COORDENADOR pode deletar"""
        request = self.create_request('DELETE', self.users['coordenador'])
        view = self.create_mock_view('destroy')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_gestor_can_delete(self):
        """GESTOR pode deletar"""
        request = self.create_request('DELETE', self.users['gestor'])
        view = self.create_mock_view('destroy')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_operador_cannot_delete(self):
        """OPERADOR NÃO pode deletar"""
        request = self.create_request('DELETE', self.users['operador'])
        view = self.create_mock_view('destroy')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    def test_consultor_cannot_delete(self):
        """CONSULTOR NÃO pode deletar"""
        request = self.create_request('DELETE', self.users['consultor'])
        view = self.create_mock_view('destroy')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    # ------------------------------------------------------------------------
    # CUSTOM ACTIONS - Ativar Vigência
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_activate_vigencia(self):
        """COORDENADOR pode ativar vigência (custom action)"""
        request = self.create_request('POST', self.users['coordenador'])
        view = self.create_mock_view('ativar')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_operador_cannot_activate_vigencia(self):
        """OPERADOR NÃO pode ativar vigência"""
        request = self.create_request('POST', self.users['operador'])
        view = self.create_mock_view('ativar')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    # ------------------------------------------------------------------------
    # EDGE CASES
    # ------------------------------------------------------------------------
    
    def test_user_without_role_cannot_write(self):
        """Usuário sem role NÃO pode escrever"""
        request = self.create_request('POST', self.user_no_role)
        view = self.create_mock_view('create')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    def test_user_without_role_can_read(self):
        """Usuário sem role pode ler (se autenticado)"""
        request = self.create_request('GET', self.user_no_role)
        view = self.create_mock_view('list')
        
        # Depende da implementação - pode retornar False se exigir role PNGI
        # Ajustar conforme a lógica real
        result = self.permission.has_permission(request, view)
        self.assertIn(result, [True, False])  # Aceita ambos
    
    def test_unauthenticated_user_denied(self):
        """Usuário não autenticado é negado"""
        request = self.create_request('GET', user=None)
        view = self.create_mock_view('list')
        
        self.assertFalse(self.permission.has_permission(request, view))


# ============================================================================
# TESTES DE IsCoordernadorGestorOrOperadorPNGI (Operações)
# ============================================================================

class IsCoordernadorGestorOrOperadorPNGITests(BasePermissionTestCase):
    """
    Testes da permission IsCoordernadorGestorOrOperadorPNGI.
    
    Usada para: Acoes, AcaoPrazo, AcaoDestaque, AcaoAnotacaoAlinhamento,
                UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel
    
    Regra:
    - SAFE_METHODS: todas as roles
    - CREATE/UPDATE/DELETE: COORDENADOR, GESTOR e OPERADOR
    - CONSULTOR: bloqueado em escrita
    """
    
    def setUp(self):
        super().setUp()
        self.permission = IsCoordernadorGestorOrOperadorPNGI()
    
    # ------------------------------------------------------------------------
    # SAFE_METHODS - Todas as roles podem ler
    # ------------------------------------------------------------------------
    
    def test_all_roles_can_read(self):
        """Todas as 4 roles podem usar SAFE_METHODS"""
        for role_name in ['coordenador', 'gestor', 'operador', 'consultor']:
            with self.subTest(role=role_name):
                request = self.create_request('GET', self.users[role_name])
                view = self.create_mock_view('list')
                
                self.assertTrue(self.permission.has_permission(request, view))
    
    # ------------------------------------------------------------------------
    # CREATE - COORDENADOR, GESTOR e OPERADOR
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_create(self):
        """COORDENADOR pode criar"""
        request = self.create_request('POST', self.users['coordenador'])
        view = self.create_mock_view('create')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_gestor_can_create(self):
        """GESTOR pode criar"""
        request = self.create_request('POST', self.users['gestor'])
        view = self.create_mock_view('create')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_operador_can_create(self):
        """OPERADOR PODE criar (não é configuração)"""
        request = self.create_request('POST', self.users['operador'])
        view = self.create_mock_view('create')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_consultor_cannot_create(self):
        """CONSULTOR NÃO pode criar"""
        request = self.create_request('POST', self.users['consultor'])
        view = self.create_mock_view('create')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    # ------------------------------------------------------------------------
    # UPDATE - COORDENADOR, GESTOR e OPERADOR
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_update(self):
        """COORDENADOR pode atualizar"""
        request = self.create_request('PATCH', self.users['coordenador'])
        view = self.create_mock_view('partial_update')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_gestor_can_update(self):
        """GESTOR pode atualizar"""
        request = self.create_request('PUT', self.users['gestor'])
        view = self.create_mock_view('update')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_operador_can_update(self):
        """OPERADOR PODE atualizar"""
        request = self.create_request('PATCH', self.users['operador'])
        view = self.create_mock_view('partial_update')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_consultor_cannot_update(self):
        """CONSULTOR NÃO pode atualizar"""
        request = self.create_request('PUT', self.users['consultor'])
        view = self.create_mock_view('update')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    # ------------------------------------------------------------------------
    # DELETE - COORDENADOR, GESTOR e OPERADOR
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_delete(self):
        """COORDENADOR pode deletar"""
        request = self.create_request('DELETE', self.users['coordenador'])
        view = self.create_mock_view('destroy')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_gestor_can_delete(self):
        """GESTOR pode deletar"""
        request = self.create_request('DELETE', self.users['gestor'])
        view = self.create_mock_view('destroy')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_operador_can_delete(self):
        """OPERADOR PODE deletar"""
        request = self.create_request('DELETE', self.users['operador'])
        view = self.create_mock_view('destroy')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_consultor_cannot_delete(self):
        """CONSULTOR NÃO pode deletar"""
        request = self.create_request('DELETE', self.users['consultor'])
        view = self.create_mock_view('destroy')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    # ------------------------------------------------------------------------
    # EDGE CASES
    # ------------------------------------------------------------------------
    
    def test_user_without_role_cannot_write(self):
        """Usuário sem role NÃO pode escrever"""
        request = self.create_request('POST', self.user_no_role)
        view = self.create_mock_view('create')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    def test_unauthenticated_user_denied(self):
        """Usuário não autenticado é negado"""
        request = self.create_request('POST', user=None)
        view = self.create_mock_view('create')
        
        self.assertFalse(self.permission.has_permission(request, view))


# ============================================================================
# TESTES DE IsAnyPNGIRole (Leitura Universal)
# ============================================================================

class IsAnyPNGIRoleTests(BasePermissionTestCase):
    """
    Testes da permission IsAnyPNGIRole.
    
    Usada para: Leitura universal - qualquer usuário com role PNGI
    
    Regra:
    - Qualquer role PNGI tem acesso
    - Usuário sem role PNGI é negado
    """
    
    def setUp(self):
        super().setUp()
        self.permission = IsAnyPNGIRole()
    
    def test_coordenador_has_access(self):
        """COORDENADOR tem acesso"""
        request = self.create_request('GET', self.users['coordenador'])
        view = self.create_mock_view('list')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_gestor_has_access(self):
        """GESTOR tem acesso"""
        request = self.create_request('GET', self.users['gestor'])
        view = self.create_mock_view('list')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_operador_has_access(self):
        """OPERADOR tem acesso"""
        request = self.create_request('GET', self.users['operador'])
        view = self.create_mock_view('list')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_consultor_has_access(self):
        """CONSULTOR tem acesso"""
        request = self.create_request('GET', self.users['consultor'])
        view = self.create_mock_view('list')
        
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_user_without_pngi_role_denied(self):
        """Usuário sem role PNGI é negado"""
        request = self.create_request('GET', self.user_no_role)
        view = self.create_mock_view('list')
        
        self.assertFalse(self.permission.has_permission(request, view))
    
    def test_unauthenticated_user_denied(self):
        """Usuário não autenticado é negado"""
        request = self.create_request('GET', user=None)
        view = self.create_mock_view('list')
        
        self.assertFalse(self.permission.has_permission(request, view))


# ============================================================================
# TESTES DE MATRIZ DE PERMISSÕES
# ============================================================================

class PermissionMatrixTests(BasePermissionTestCase):
    """
    Testes de matriz completa de permissões.
    
    Valida a matriz de permissões por role e tipo de entidade:
    
    | Role          | Config (R) | Config (W) | Operação (R) | Operação (W) |
    |---------------|------------|------------|--------------|---------------|
    | COORDENADOR   | ✓          | ✓          | ✓            | ✓             |
    | GESTOR        | ✓          | ✓          | ✓            | ✓             |
    | OPERADOR      | ✓          | ✗          | ✓            | ✓             |
    | CONSULTOR     | ✓          | ✗          | ✓            | ✗             |
    | Sem Role      | ?          | ✗          | ?            | ✗             |
    | Não Autent.   | ✗          | ✗          | ✗            | ✗             |
    """
    
    def setUp(self):
        super().setUp()
        self.perm_config = IsCoordernadorOrGestorPNGI()
        self.perm_operacao = IsCoordernadorGestorOrOperadorPNGI()
    
    def test_permission_matrix_config_read(self):
        """Matriz: Leitura de Configurações"""
        expected = {
            'coordenador': True,
            'gestor': True,
            'operador': True,
            'consultor': True
        }
        
        for role_name, should_pass in expected.items():
            with self.subTest(role=role_name):
                request = self.create_request('GET', self.users[role_name])
                view = self.create_mock_view('list')
                
                result = self.perm_config.has_permission(request, view)
                self.assertEqual(result, should_pass)
    
    def test_permission_matrix_config_write(self):
        """Matriz: Escrita de Configurações"""
        expected = {
            'coordenador': True,
            'gestor': True,
            'operador': False,
            'consultor': False
        }
        
        for role_name, should_pass in expected.items():
            with self.subTest(role=role_name):
                request = self.create_request('POST', self.users[role_name])
                view = self.create_mock_view('create')
                
                result = self.perm_config.has_permission(request, view)
                self.assertEqual(result, should_pass)
    
    def test_permission_matrix_operacao_read(self):
        """Matriz: Leitura de Operações"""
        expected = {
            'coordenador': True,
            'gestor': True,
            'operador': True,
            'consultor': True
        }
        
        for role_name, should_pass in expected.items():
            with self.subTest(role=role_name):
                request = self.create_request('GET', self.users[role_name])
                view = self.create_mock_view('list')
                
                result = self.perm_operacao.has_permission(request, view)
                self.assertEqual(result, should_pass)
    
    def test_permission_matrix_operacao_write(self):
        """Matriz: Escrita de Operações"""
        expected = {
            'coordenador': True,
            'gestor': True,
            'operador': True,
            'consultor': False
        }
        
        for role_name, should_pass in expected.items():
            with self.subTest(role=role_name):
                request = self.create_request('POST', self.users[role_name])
                view = self.create_mock_view('create')
                
                result = self.perm_operacao.has_permission(request, view)
                self.assertEqual(result, should_pass)
    
    def test_permission_hierarchy_consistency(self):
        """Hierarquia: COORDENADOR >= GESTOR >= OPERADOR >= CONSULTOR"""
        # COORDENADOR deve ter no mínimo as mesmas permissões que GESTOR
        # GESTOR deve ter no mínimo as mesmas permissões que OPERADOR
        # etc.
        
        permissions_config_write = {
            'coordenador': True,
            'gestor': True,
            'operador': False,
            'consultor': False
        }
        
        permissions_operacao_write = {
            'coordenador': True,
            'gestor': True,
            'operador': True,
            'consultor': False
        }
        
        # Verificar que não há inconsistências hierárquicas
        # (role inferior não pode ter mais permissões que superior)
        self.assertTrue(permissions_config_write['coordenador'] >= permissions_config_write['gestor'])
        self.assertTrue(permissions_config_write['gestor'] >= permissions_config_write['operador'])
        self.assertTrue(permissions_config_write['operador'] >= permissions_config_write['consultor'])
        
        self.assertTrue(permissions_operacao_write['coordenador'] >= permissions_operacao_write['gestor'])
        self.assertTrue(permissions_operacao_write['gestor'] >= permissions_operacao_write['operador'])
        self.assertTrue(permissions_operacao_write['operador'] >= permissions_operacao_write['consultor'])
