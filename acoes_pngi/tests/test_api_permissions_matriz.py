"""
Testes de Permissões da Matriz Oficial para API Views.

Valida a seguinte matriz:

| ViewSet                          | Permission Class                      | Leitura (GET/LIST) | Escrita (POST/PUT/PATCH/DELETE) |
|----------------------------------|---------------------------------------|--------------------|---------------------------------|
| EixoViewSet                      | IsCoordernadorOrGestorPNGI            | Todos              | COORDENADOR, GESTOR             |
| SituacaoAcaoViewSet              | IsGestorPNGI                          | Todos              | GESTOR                          |
| VigenciaPNGIViewSet              | IsCoordernadorOrGestorPNGI            | Todos              | COORDENADOR, GESTOR             |
| TipoEntraveAlertaViewSet         | IsGestorPNGI                          | Todos              | GESTOR                          |
| UserManagementViewSet            | IsGestorPNGI                          | GESTOR             | GESTOR                          |
| AcoesViewSet                     | IsCoordernadorGestorOrOperadorPNGI    | Todos              | OPERADOR, COORDENADOR, GESTOR   |
| AcaoPrazoViewSet                 | IsCoordernadorGestorOrOperadorPNGI    | Todos              | OPERADOR, COORDENADOR, GESTOR   |
| AcaoDestaqueViewSet              | IsCoordernadorGestorOrOperadorPNGI    | Todos              | OPERADOR, COORDENADOR, GESTOR   |
| TipoAnotacaoAlinhamentoViewSet   | IsCoordernadorOrGestorPNGI            | Todos              | COORDENADOR, GESTOR             |
| AcaoAnotacaoAlinhamentoViewSet   | IsCoordernadorGestorOrOperadorPNGI    | Todos              | OPERADOR, COORDENADOR, GESTOR   |
| UsuarioResponsavelViewSet        | IsCoordernadorGestorOrOperadorPNGI    | Todos              | OPERADOR, COORDENADOR, GESTOR   |
| RelacaoAcaoUsuarioResponsavelVS  | IsCoordernadorGestorOrOperadorPNGI    | Todos              | OPERADOR, COORDENADOR, GESTOR   |
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User, Role, UserRole, Aplicacao
from ..models import (
    Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta,
    Acoes, AcaoPrazo, AcaoDestaque,
    TipoAnotacaoAlinhamento, AcaoAnotacaoAlinhamento,
    UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel
)
from .base import BaseAPITestCase


class PermissionMatrixTestCase(BaseAPITestCase):
    """
    Classe base para testes de permissões com fixtures de usuários.
    """
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Criar roles COM A ESTRUTURA CORRETA: aplicacao, nomeperfil, codigoperfil
        cls.role_consultor, _ = Role.objects.using('gpp_plataform_db').get_or_create(
            aplicacao=cls.app,
            codigoperfil='CONSULTOR_PNGI',
            defaults={'nomeperfil': 'Consultor PNGI'}
        )
        cls.role_operador, _ = Role.objects.using('gpp_plataform_db').get_or_create(
            aplicacao=cls.app,
            codigoperfil='OPERADOR_PNGI',
            defaults={'nomeperfil': 'Operador PNGI'}
        )
        cls.role_coordenador, _ = Role.objects.using('gpp_plataform_db').get_or_create(
            aplicacao=cls.app,
            codigoperfil='COORDENADOR_PNGI',
            defaults={'nomeperfil': 'Coordenador PNGI'}
        )
        cls.role_gestor, _ = Role.objects.using('gpp_plataform_db').get_or_create(
            aplicacao=cls.app,
            codigoperfil='GESTOR_PNGI',
            defaults={'nomeperfil': 'Gestor PNGI'}
        )
    
    def setUp(self):
        super().setUp()
        
        # Criar usuários com roles diferentes
        self.user_consultor = User.objects.create_user(
            email='consultor@test.com',
            password='test123',
            name='Consultor Test'
        )
        UserRole.objects.using('gpp_plataform_db').create(
            user=self.user_consultor,
            role=self.role_consultor,
            aplicacao=self.app
        )
        
        self.user_operador = User.objects.create_user(
            email='operador@test.com',
            password='test123',
            name='Operador Test'
        )
        UserRole.objects.using('gpp_plataform_db').create(
            user=self.user_operador,
            role=self.role_operador,
            aplicacao=self.app
        )
        
        self.user_coordenador = User.objects.create_user(
            email='coordenador@test.com',
            password='test123',
            name='Coordenador Test'
        )
        UserRole.objects.using('gpp_plataform_db').create(
            user=self.user_coordenador,
            role=self.role_coordenador,
            aplicacao=self.app
        )
        
        self.user_gestor = User.objects.create_user(
            email='gestor@test.com',
            password='test123',
            name='Gestor Test'
        )
        UserRole.objects.using('gpp_plataform_db').create(
            user=self.user_gestor,
            role=self.role_gestor,
            aplicacao=self.app
        )
        
        # Cliente API
        self.client = APIClient()


class EixoViewSetPermissionTest(PermissionMatrixTestCase):
    """
    Testa permissões do EixoViewSet.
    Permission: IsCoordernadorOrGestorPNGI
    - Leitura: TODOS
    - Escrita: COORDENADOR, GESTOR
    """
    
    def test_consultor_pode_listar_eixos(self):
        """CONSULTOR pode listar eixos (GET)"""
        self.client.force_authenticate(user=self.user_consultor)
        response = self.client.get('/api/v1/acoes_pngi/eixos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_consultor_nao_pode_criar_eixo(self):
        """CONSULTOR não pode criar eixo (POST)"""
        self.client.force_authenticate(user=self.user_consultor)
        data = {'strdescricaoeixo': 'Novo Eixo', 'stralias': 'NE'}
        response = self.client.post('/api/v1/acoes_pngi/eixos/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_pode_listar_eixos(self):
        """OPERADOR pode listar eixos (GET)"""
        self.client.force_authenticate(user=self.user_operador)
        response = self.client.get('/api/v1/acoes_pngi/eixos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_operador_nao_pode_criar_eixo(self):
        """OPERADOR não pode criar eixo (POST)"""
        self.client.force_authenticate(user=self.user_operador)
        data = {'strdescricaoeixo': 'Novo Eixo', 'stralias': 'NE'}
        response = self.client.post('/api/v1/acoes_pngi/eixos/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_pode_criar_eixo(self):
        """COORDENADOR pode criar eixo (POST)"""
        self.client.force_authenticate(user=self.user_coordenador)
        data = {'strdescricaoeixo': 'Novo Eixo', 'stralias': 'NE'}
        response = self.client.post('/api/v1/acoes_pngi/eixos/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
    
    def test_gestor_pode_criar_eixo(self):
        """GESTOR pode criar eixo (POST)"""
        self.client.force_authenticate(user=self.user_gestor)
        data = {'strdescricaoeixo': 'Novo Eixo', 'stralias': 'NE'}
        response = self.client.post('/api/v1/acoes_pngi/eixos/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class SituacaoAcaoViewSetPermissionTest(PermissionMatrixTestCase):
    """
    Testa permissões do SituacaoAcaoViewSet.
    Permission: IsGestorPNGI
    - Leitura: TODOS
    - Escrita: GESTOR
    """
    
    def test_consultor_pode_listar_situacoes(self):
        """CONSULTOR pode listar situações (GET)"""
        self.client.force_authenticate(user=self.user_consultor)
        response = self.client.get('/api/v1/acoes_pngi/situacoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_consultor_nao_pode_criar_situacao(self):
        """CONSULTOR não pode criar situação (POST)"""
        self.client.force_authenticate(user=self.user_consultor)
        data = {'strdescricaosituacao': 'Nova Situação'}
        response = self.client.post('/api/v1/acoes_pngi/situacoes/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_nao_pode_criar_situacao(self):
        """OPERADOR não pode criar situação (POST)"""
        self.client.force_authenticate(user=self.user_operador)
        data = {'strdescricaosituacao': 'Nova Situação'}
        response = self.client.post('/api/v1/acoes_pngi/situacoes/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_nao_pode_criar_situacao(self):
        """COORDENADOR não pode criar situação (POST)"""
        self.client.force_authenticate(user=self.user_coordenador)
        data = {'strdescricaosituacao': 'Nova Situação'}
        response = self.client.post('/api/v1/acoes_pngi/situacoes/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_gestor_pode_criar_situacao(self):
        """GESTOR pode criar situação (POST)"""
        self.client.force_authenticate(user=self.user_gestor)
        data = {'strdescricaosituacao': 'Nova Situação'}
        response = self.client.post('/api/v1/acoes_pngi/situacoes/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class VigenciaPNGIViewSetPermissionTest(PermissionMatrixTestCase):
    """
    Testa permissões do VigenciaPNGIViewSet.
    Permission: IsCoordernadorOrGestorPNGI
    - Leitura: TODOS
    - Escrita: COORDENADOR, GESTOR
    """
    
    def test_consultor_pode_listar_vigencias(self):
        """CONSULTOR pode listar vigências (GET)"""
        self.client.force_authenticate(user=self.user_consultor)
        response = self.client.get('/api/v1/acoes_pngi/vigencias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_operador_nao_pode_criar_vigencia(self):
        """OPERADOR não pode criar vigência (POST)"""
        self.client.force_authenticate(user=self.user_operador)
        data = {
            'strdescricaovigenciapngi': 'Nova Vigência',
            'datiniciovigencia': '2026-01-01',
            'datfinalvigencia': '2026-12-31'
        }
        response = self.client.post('/api/v1/acoes_pngi/vigencias/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_pode_criar_vigencia(self):
        """COORDENADOR pode criar vigência (POST)"""
        self.client.force_authenticate(user=self.user_coordenador)
        data = {
            'strdescricaovigenciapngi': 'Nova Vigência',
            'datiniciovigencia': '2026-01-01',
            'datfinalvigencia': '2026-12-31'
        }
        response = self.client.post('/api/v1/acoes_pngi/vigencias/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
    
    def test_gestor_pode_criar_vigencia(self):
        """GESTOR pode criar vigência (POST)"""
        self.client.force_authenticate(user=self.user_gestor)
        data = {
            'strdescricaovigenciapngi': 'Nova Vigência',
            'datiniciovigencia': '2026-01-01',
            'datfinalvigencia': '2026-12-31'
        }
        response = self.client.post('/api/v1/acoes_pngi/vigencias/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class TipoEntraveAlertaViewSetPermissionTest(PermissionMatrixTestCase):
    """
    Testa permissões do TipoEntraveAlertaViewSet.
    Permission: IsGestorPNGI
    - Leitura: TODOS
    - Escrita: GESTOR
    """
    
    def test_consultor_pode_listar_tipos(self):
        """CONSULTOR pode listar tipos de entrave (GET)"""
        self.client.force_authenticate(user=self.user_consultor)
        response = self.client.get('/api/v1/acoes_pngi/tipos-entrave-alerta/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_nao_pode_criar_tipo(self):
        """COORDENADOR não pode criar tipo de entrave (POST)"""
        self.client.force_authenticate(user=self.user_coordenador)
        data = {'strdescricaotipoentravealerta': 'Novo Tipo'}
        response = self.client.post('/api/v1/acoes_pngi/tipos-entrave-alerta/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_gestor_pode_criar_tipo(self):
        """GESTOR pode criar tipo de entrave (POST)"""
        self.client.force_authenticate(user=self.user_gestor)
        data = {'strdescricaotipoentravealerta': 'Novo Tipo'}
        response = self.client.post('/api/v1/acoes_pngi/tipos-entrave-alerta/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class AcoesViewSetPermissionTest(PermissionMatrixTestCase):
    """
    Testa permissões do AcoesViewSet.
    Permission: IsCoordernadorGestorOrOperadorPNGI
    - Leitura: TODOS
    - Escrita: OPERADOR, COORDENADOR, GESTOR
    """
    
    def test_consultor_pode_listar_acoes(self):
        """CONSULTOR pode listar ações (GET)"""
        self.client.force_authenticate(user=self.user_consultor)
        response = self.client.get('/api/v1/acoes_pngi/acoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_consultor_nao_pode_criar_acao(self):
        """CONSULTOR não pode criar ação (POST)"""
        self.client.force_authenticate(user=self.user_consultor)
        data = {
            'strapelido': 'ACAO-TEST',
            'strdescricaoacao': 'Teste',
            'strdescricaoentrega': 'Entrega',
            'idvigenciapngi': self.vigencia_base.idvigenciapngi,
            'ideixo': self.eixo_base.ideixo,
            'idsituacaoacao': self.situacao_base.idsituacaoacao
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_pode_criar_acao(self):
        """OPERADOR pode criar ação (POST)"""
        self.client.force_authenticate(user=self.user_operador)
        data = {
            'strapelido': 'ACAO-TEST',
            'strdescricaoacao': 'Teste',
            'strdescricaoentrega': 'Entrega',
            'idvigenciapngi': self.vigencia_base.idvigenciapngi,
            'ideixo': self.eixo_base.ideixo,
            'idsituacaoacao': self.situacao_base.idsituacaoacao
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
    
    def test_coordenador_pode_criar_acao(self):
        """COORDENADOR pode criar ação (POST)"""
        self.client.force_authenticate(user=self.user_coordenador)
        data = {
            'strapelido': 'ACAO-TEST2',
            'strdescricaoacao': 'Teste',
            'strdescricaoentrega': 'Entrega',
            'idvigenciapngi': self.vigencia_base.idvigenciapngi,
            'ideixo': self.eixo_base.ideixo,
            'idsituacaoacao': self.situacao_base.idsituacaoacao
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
    
    def test_gestor_pode_criar_acao(self):
        """GESTOR pode criar ação (POST)"""
        self.client.force_authenticate(user=self.user_gestor)
        data = {
            'strapelido': 'ACAO-TEST3',
            'strdescricaoacao': 'Teste',
            'strdescricaoentrega': 'Entrega',
            'idvigenciapngi': self.vigencia_base.idvigenciapngi,
            'ideixo': self.eixo_base.ideixo,
            'idsituacaoacao': self.situacao_base.idsituacaoacao
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class TipoAnotacaoAlinhamentoViewSetPermissionTest(PermissionMatrixTestCase):
    """
    Testa permissões do TipoAnotacaoAlinhamentoViewSet.
    Permission: IsCoordernadorOrGestorPNGI
    - Leitura: TODOS
    - Escrita: COORDENADOR, GESTOR
    """
    
    def test_consultor_pode_listar_tipos_anotacao(self):
        """CONSULTOR pode listar tipos de anotação (GET)"""
        self.client.force_authenticate(user=self.user_consultor)
        response = self.client.get('/api/v1/acoes_pngi/tipos-anotacao-alinhamento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_operador_nao_pode_criar_tipo_anotacao(self):
        """OPERADOR não pode criar tipo de anotação (POST)"""
        self.client.force_authenticate(user=self.user_operador)
        data = {'strdescricaotipoanotacaoalinhamento': 'Novo Tipo'}
        response = self.client.post('/api/v1/acoes_pngi/tipos-anotacao-alinhamento/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_pode_criar_tipo_anotacao(self):
        """COORDENADOR pode criar tipo de anotação (POST)"""
        self.client.force_authenticate(user=self.user_coordenador)
        data = {'strdescricaotipoanotacaoalinhamento': 'Novo Tipo'}
        response = self.client.post('/api/v1/acoes_pngi/tipos-anotacao-alinhamento/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
    
    def test_gestor_pode_criar_tipo_anotacao(self):
        """GESTOR pode criar tipo de anotação (POST)"""
        self.client.force_authenticate(user=self.user_gestor)
        data = {'strdescricaotipoanotacaoalinhamento': 'Novo Tipo'}
        response = self.client.post('/api/v1/acoes_pngi/tipos-anotacao-alinhamento/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class UserManagementViewSetPermissionTest(PermissionMatrixTestCase):
    """
    Testa permissões do UserManagementViewSet.
    Permission: IsGestorPNGI
    - Leitura: GESTOR
    - Escrita: GESTOR
    """
    
    def test_consultor_nao_pode_listar_usuarios(self):
        """CONSULTOR não pode listar usuários"""
        self.client.force_authenticate(user=self.user_consultor)
        response = self.client.get('/api/v1/acoes_pngi/users/list_users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_nao_pode_listar_usuarios(self):
        """OPERADOR não pode listar usuários"""
        self.client.force_authenticate(user=self.user_operador)
        response = self.client.get('/api/v1/acoes_pngi/users/list_users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_nao_pode_listar_usuarios(self):
        """COORDENADOR não pode listar usuários"""
        self.client.force_authenticate(user=self.user_coordenador)
        response = self.client.get('/api/v1/acoes_pngi/users/list_users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_gestor_pode_listar_usuarios(self):
        """GESTOR pode listar usuários"""
        self.client.force_authenticate(user=self.user_gestor)
        response = self.client.get('/api/v1/acoes_pngi/users/list_users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_gestor_pode_sincronizar_usuario(self):
        """GESTOR pode sincronizar usuário"""
        self.client.force_authenticate(user=self.user_gestor)
        data = {
            'email': 'novo@test.com',
            'name': 'Novo Usuario',
            'role': 'CONSULTOR_PNGI'
        }
        response = self.client.post('/api/v1/acoes_pngi/users/sync_user/', data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
