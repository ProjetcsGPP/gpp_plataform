"""
Testes de API Views - Ações PNGI

Testa todos os ViewSets da API com as 4 roles hierárquicas:
- COORDENADOR_PNGI: Acesso total + gerencia configurações
- GESTOR_PNGI: Acesso total às ações
- OPERADOR_ACAO: Apenas operações em ações (sem configurações)
- CONSULTOR_PNGI: Apenas leitura (sem escrita)

Cobre:
- CRUD completo (List, Create, Retrieve, Update, Delete)
- Validações de permissões por role
- Custom actions dos ViewSets
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from unittest.mock import Mock, patch

from accounts.models import Aplicacao, Role, UserRole, RolePermission
from ..models import (
    Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta,
    Acoes, AcaoPrazo, AcaoDestaque,
    TipoAnotacaoAlinhamento, AcaoAnotacaoAlinhamento,
    UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel
)

User = get_user_model()


class BaseAPITestCase(TestCase):
    """
    Classe base para testes de API com setup de roles e autenticação.
    
    Configura:
    - Aplicação ACOES_PNGI
    - 4 roles hierárquicas
    - 4 usuários (um para cada role)
    - Permissões (RolePermission) vinculando Roles a Permissions
    - Cliente API
    """
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup inicial com aplicação, roles, permissões e usuários"""
        self.client = APIClient()
        
        # Criar aplicação (get_or_create para evitar duplicação)
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        # Criar as 4 roles hierárquicas (get_or_create)
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
        
        # ✨ NOVO: Criar permissões (RolePermission)
        self.setup_permissions()
        
        # Criar usuários para cada role
        self.users = {}
        for role_name, role_obj in [
            ('coordenador', self.role_coordenador),
            ('gestor', self.role_gestor),
            ('operador', self.role_operador),
            ('consultor', self.role_consultor)
        ]:
            user = User.objects.create_user(
                email=f'{role_name}@seger.es.gov.br',
                name=f'User {role_name.title()}',
                password='testpass123'
            )
            UserRole.objects.create(
                user=user,
                aplicacao=self.app,
                role=role_obj
            )
            self.users[role_name] = user
        
        # Criar dados de teste base
        self.setup_test_data()
    
    def setup_permissions(self):
        """
        Cria as permissões (RolePermission) vinculando Roles a Permissions.
        
        NOVA HIERARQUIA (Pós-inversão Coordenador ↔ Gestor):
        
        - GESTOR_PNGI: CRUD completo em TUDO (44 permissões)
          * Configs: add, change, delete, view
          * Negócio: add, change, delete, view
          * Filhas: add, change, delete, view
        
        - COORDENADOR_PNGI: view configs + CRUD negócio/filhas (29 permissões)
          * Configs: view apenas
          * Negócio: add, change, delete, view
          * Filhas: add, change, delete, view
        
        - OPERADOR_ACAO: view configs/negócio + add/view filhas (15 permissões)
          * Configs: view apenas
          * Negócio: view apenas
          * Filhas: add, view
        
        - CONSULTOR_PNGI: view em tudo (11 permissões)
          * Configs: view
          * Negócio: view
          * Filhas: view
        """
        # Classificação de modelos
        models_config = {
            'CONFIGS': [
                ('eixo', Eixo),
                ('situacaoacao', SituacaoAcao),
                ('vigenciapngi', VigenciaPNGI),
                ('tipoanotacaoalinhamento', TipoAnotacaoAlinhamento),
                ('tipoentravealerta', TipoEntraveAlerta),
            ],
            'NEGOCIO': [
                ('acoes', Acoes),
                ('usuarioresponsavel', UsuarioResponsavel),
            ],
            'FILHAS': [
                ('acaoprazo', AcaoPrazo),
                ('acaodestaque', AcaoDestaque),
                ('acaoanotacaoalinhamento', AcaoAnotacaoAlinhamento),
                ('relacaoacaousuarioresponsavel', RelacaoAcaoUsuarioResponsavel),
            ]
        }
        
        actions = ['add', 'change', 'delete', 'view']
        
        # Criar todas as permissões
        permissions_by_model = {}
        for category, model_list in models_config.items():
            for model_name, model_class in model_list:
                ct = ContentType.objects.get_for_model(model_class)
                permissions_by_model[model_name] = {}
                
                for action in actions:
                    codename = f'{action}_{model_name}'
                    perm, _ = Permission.objects.get_or_create(
                        codename=codename,
                        content_type=ct,
                        defaults={'name': f'Can {action} {model_name}'}
                    )
                    permissions_by_model[model_name][action] = perm
        
        # Hierarquia de permissões por role
        roles_hierarchy = {
            self.role_gestor: {
                'CONFIGS': ['add', 'change', 'delete', 'view'],
                'NEGOCIO': ['add', 'change', 'delete', 'view'],
                'FILHAS': ['add', 'change', 'delete', 'view'],
            },
            self.role_coordenador: {
                'CONFIGS': ['view'],
                'NEGOCIO': ['add', 'change', 'delete', 'view'],
                'FILHAS': ['add', 'change', 'delete', 'view'],
            },
            self.role_operador: {
                'CONFIGS': ['view'],
                'NEGOCIO': ['view'],
                'FILHAS': ['add', 'view'],
            },
            self.role_consultor: {
                'CONFIGS': ['view'],
                'NEGOCIO': ['view'],
                'FILHAS': ['view'],
            }
        }
        
        # Vincular permissões às roles
        for role, categories in roles_hierarchy.items():
            for category, allowed_actions in categories.items():
                model_list = models_config[category]
                
                for model_name, model_class in model_list:
                    for action in allowed_actions:
                        if action in permissions_by_model[model_name]:
                            perm = permissions_by_model[model_name][action]
                            RolePermission.objects.get_or_create(
                                role=role,
                                permission=perm
                            )

    
    def setup_test_data(self):
        """
        Override em subclasses para criar dados específicos.
        Ex: vigências, eixos, etc.
        """
        pass
    
    def authenticate_as(self, role_name):
        """
        Autentica como um usuário específico.
        
        Args:
            role_name (str): 'coordenador', 'gestor', 'operador' ou 'consultor'
        
        Returns:
            User: Usuário autenticado
        """
        user = self.users[role_name]
        self.client.force_authenticate(user=user)
        return user
    
    def logout(self):
        """Remove autenticação"""
        self.client.force_authenticate(user=None)


# ============================================================================
# TESTES DE EIXO - ViewSet: EixoViewSet
# ============================================================================

class EixoAPITests(BaseAPITestCase):
    """
    Testes de API para Eixo.
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/eixos/           - Listar
    - POST   /api/v1/acoes_pngi/eixos/           - Criar
    - GET    /api/v1/acoes_pngi/eixos/{id}/      - Detalhe
    - PATCH  /api/v1/acoes_pngi/eixos/{id}/      - Atualizar
    - DELETE /api/v1/acoes_pngi/eixos/{id}/      - Deletar
    - GET    /api/v1/acoes_pngi/eixos/list_light/ - Listagem otimizada
    """
    
    def setup_test_data(self):
        """Cria eixo de teste"""
        self.eixo = Eixo.objects.create(
            strdescricaoeixo='Eixo Teste Base',
            stralias='TESTE'
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_eixos(self):
        """COORDENADOR_PNGI pode listar eixos"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/eixos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Aceita tanto lista direta quanto paginada
        self.assertTrue(
            isinstance(response.data, list) or 'results' in response.data,
            "Response deve ser lista ou ter 'results'"
        )
    
    def test_coordenador_cannot_create_eixo(self):
        """COORDENADOR_PNGI NÃO pode criar eixo (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {
            'strdescricaoeixo': 'Tentativa Coordenador',
            'stralias': 'NCOOR'
        }
        response = self.client.post('/api/v1/acoes_pngi/eixos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_can_retrieve_eixo(self):
        """COORDENADOR_PNGI pode buscar eixo por ID"""
        self.authenticate_as('coordenador')
        response = self.client.get(f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stralias'], 'TESTE')
    
    def test_coordenador_cannot_update_eixo(self):
        """COORDENADOR_PNGI NÃO pode atualizar eixo (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {'strdescricaoeixo': 'Tentativa Update'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_cannot_delete_eixo(self):
        """COORDENADOR_PNGI NÃO pode deletar eixo (apenas view em configs)"""
        self.authenticate_as('coordenador')
        response = self.client.delete(f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_can_access_list_light(self):
        """COORDENADOR_PNGI pode acessar list_light"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/eixos/list_light/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # list_light sempre retorna com 'results'
        self.assertIn('results', response.data)
    
    # ------------------------------------------------------------------------
    # GESTOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_gestor_can_list_eixos(self):
        """GESTOR_PNGI pode listar eixos"""
        self.authenticate_as('gestor')
        response = self.client.get('/api/v1/acoes_pngi/eixos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_gestor_can_create_eixo(self):
        """GESTOR_PNGI pode criar eixo"""
        self.authenticate_as('gestor')
        data = {
            'strdescricaoeixo': 'Novo Eixo Gestor',
            'stralias': 'NGEST'
        }
        response = self.client.post('/api/v1/acoes_pngi/eixos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_gestor_can_update_eixo(self):
        """GESTOR_PNGI pode atualizar eixo"""
        self.authenticate_as('gestor')
        data = {'strdescricaoeixo': 'Atualizado pelo Gestor'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_gestor_can_delete_eixo(self):
        """GESTOR_PNGI pode deletar eixo"""
        eixo_temp = Eixo.objects.create(
            strdescricaoeixo='Gestor Delete',
            stralias='GDEL'
        )
        
        self.authenticate_as('gestor')
        response = self.client.delete(f'/api/v1/acoes_pngi/eixos/{eixo_temp.ideixo}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Bloqueado em Configurações
    # ------------------------------------------------------------------------
    
    def test_operador_can_view_eixos(self):
        """OPERADOR_ACAO pode visualizar eixos (mas não criar/editar)"""
        self.authenticate_as('operador')
        response = self.client.get('/api/v1/acoes_pngi/eixos/')
        # Operador TEM view_eixo agora!
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_operador_cannot_create_eixo(self):
        """OPERADOR_ACAO NÃO pode criar eixo (configuração)"""
        self.authenticate_as('operador')
        data = {
            'strdescricaoeixo': 'Tentativa Operador',
            'stralias': 'TOPER'
        }
        response = self.client.post('/api/v1/acoes_pngi/eixos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_update_eixo(self):
        """OPERADOR_ACAO NÃO pode atualizar eixo"""
        self.authenticate_as('operador')
        data = {'strdescricaoeixo': 'Tentativa Update'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_delete_eixo(self):
        """OPERADOR_ACAO NÃO pode deletar eixo"""
        self.authenticate_as('operador')
        response = self.client.delete(f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_eixos(self):
        """CONSULTOR_PNGI pode listar eixos"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/eixos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_consultor_can_retrieve_eixo(self):
        """CONSULTOR_PNGI pode buscar eixo específico"""
        self.authenticate_as('consultor')
        response = self.client.get(f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_consultor_cannot_create_eixo(self):
        """CONSULTOR_PNGI NÃO pode criar eixo"""
        self.authenticate_as('consultor')
        data = {
            'strdescricaoeixo': 'Tentativa Consultor',
            'stralias': 'TCONS'
        }
        response = self.client.post('/api/v1/acoes_pngi/eixos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_cannot_update_eixo(self):
        """CONSULTOR_PNGI NÃO pode atualizar eixo"""
        self.authenticate_as('consultor')
        data = {'strdescricaoeixo': 'Tentativa Update Consultor'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_cannot_delete_eixo(self):
        """CONSULTOR_PNGI NÃO pode deletar eixo"""
        self.authenticate_as('consultor')
        response = self.client.delete(f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_can_access_list_light(self):
        """CONSULTOR_PNGI pode acessar list_light (leitura)"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/eixos/list_light/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================================================
# TESTES DE SITUAÇÃO - ViewSet: SituacaoAcaoViewSet
# ============================================================================

class SituacaoAcaoAPITests(BaseAPITestCase):
    """
    Testes de API para SituacaoAcao.
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/situacoes/
    - POST   /api/v1/acoes_pngi/situacoes/
    - GET    /api/v1/acoes_pngi/situacoes/{id}/
    - PATCH  /api/v1/acoes_pngi/situacoes/{id}/
    - DELETE /api/v1/acoes_pngi/situacoes/{id}/
    """
    
    def setup_test_data(self):
        """Cria situação de teste"""
        self.situacao = SituacaoAcao.objects.create(
            strdescricaosituacao='EM_ANDAMENTO'
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_situacoes(self):
        """COORDENADOR_PNGI pode listar situações"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/situacoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_cannot_create_situacao(self):
        """COORDENADOR_PNGI NÃO pode criar situação (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {'strdescricaosituacao': 'CONCLUIDA'}
        response = self.client.post('/api/v1/acoes_pngi/situacoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_cannot_update_situacao(self):
        """COORDENADOR_PNGI NÃO pode atualizar situação (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {'strdescricaosituacao': 'ATUALIZADA'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/situacoes/{self.situacao.idsituacaoacao}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_cannot_delete_situacao(self):
        """COORDENADOR_PNGI NÃO pode deletar situação (apenas view em configs)"""
        self.authenticate_as('coordenador')
        response = self.client.delete(f'/api/v1/acoes_pngi/situacoes/{self.situacao.idsituacaoacao}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # GESTOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_gestor_can_manage_situacoes(self):
        """GESTOR_PNGI tem acesso completo a situações"""
        self.authenticate_as('gestor')
        
        # LIST
        response = self.client.get('/api/v1/acoes_pngi/situacoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # CREATE
        data = {'strdescricaosituacao': 'PAUSADA'}
        response = self.client.post('/api/v1/acoes_pngi/situacoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Bloqueado em Configurações
    # ------------------------------------------------------------------------
    
    def test_operador_cannot_create_situacao(self):
        """OPERADOR_ACAO NÃO pode criar situação (configuração)"""
        self.authenticate_as('operador')
        data = {'strdescricaosituacao': 'TESTE_OPER'}
        response = self.client.post('/api/v1/acoes_pngi/situacoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_update_situacao(self):
        """OPERADOR_ACAO NÃO pode atualizar situação"""
        self.authenticate_as('operador')
        data = {'strdescricaosituacao': 'ATUALIZAR'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/situacoes/{self.situacao.idsituacaoacao}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_delete_situacao(self):
        """OPERADOR_ACAO NÃO pode deletar situação"""
        self.authenticate_as('operador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/situacoes/{self.situacao.idsituacaoacao}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_situacoes(self):
        """CONSULTOR_PNGI pode listar situações"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/situacoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_consultor_cannot_create_situacao(self):
        """CONSULTOR_PNGI NÃO pode criar situação"""
        self.authenticate_as('consultor')
        data = {'strdescricaosituacao': 'TESTE_CONS'}
        response = self.client.post('/api/v1/acoes_pngi/situacoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_cannot_update_situacao(self):
        """CONSULTOR_PNGI NÃO pode atualizar situação"""
        self.authenticate_as('consultor')
        data = {'strdescricaosituacao': 'UPDATE'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/situacoes/{self.situacao.idsituacaoacao}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_cannot_delete_situacao(self):
        """CONSULTOR_PNGI NÃO pode deletar situação"""
        self.authenticate_as('consultor')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/situacoes/{self.situacao.idsituacaoacao}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ============================================================================
# TESTES DE VIGÊNCIA - ViewSet: VigenciaPNGIViewSet
# ============================================================================

class VigenciaPNGIAPITests(BaseAPITestCase):
    """
    Testes de API para VigenciaPNGI.
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/vigencias/
    - POST   /api/v1/acoes_pngi/vigencias/
    - GET    /api/v1/acoes_pngi/vigencias/{id}/
    - PATCH  /api/v1/acoes_pngi/vigencias/{id}/
    - DELETE /api/v1/acoes_pngi/vigencias/{id}/
    - GET    /api/v1/acoes_pngi/vigencias/vigencia_ativa/
    - POST   /api/v1/acoes_pngi/vigencias/{id}/ativar/
    """
    
    def setup_test_data(self):
        """Cria vigência de teste"""
        self.vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),
            datfinalvigencia=date(2026, 12, 31),
            isvigenciaativa=False
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_vigencias(self):
        """COORDENADOR_PNGI pode listar vigências"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/vigencias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_cannot_create_vigencia(self):
        """COORDENADOR_PNGI NÃO pode criar vigência (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {
            'strdescricaovigenciapngi': 'PNGI 2027',
            'datiniciovigencia': '2027-01-01',
            'datfinalvigencia': '2027-12-31',
            'isvigenciaativa': False
        }
        response = self.client.post('/api/v1/acoes_pngi/vigencias/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_cannot_update_vigencia(self):
        """COORDENADOR_PNGI NÃO pode atualizar vigência (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {'strdescricaovigenciapngi': 'PNGI 2026 - Atualizado'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_can_delete_vigencia(self):
        """COORDENADOR_PNGI NÃO pode deletar vigência (apenas view em configs)"""
        self.authenticate_as('coordenador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_coordenador_can_activate_vigencia(self):
        """COORDENADOR_PNGI pode ativar vigência"""
        self.authenticate_as('coordenador')
        response = self.client.post(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/ativar/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que foi ativada
        self.vigencia.refresh_from_db()
        self.assertTrue(self.vigencia.isvigenciaativa)
    
    def test_vigencia_ativa_returns_404_when_none_active(self):
        """vigencia_ativa/ retorna 404 quando não há vigência ativa"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/vigencias/vigencia_ativa/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ------------------------------------------------------------------------
    # GESTOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_gestor_can_manage_vigencias(self):
        """GESTOR_PNGI tem acesso completo a vigências"""
        self.authenticate_as('gestor')
        
        # LIST
        response = self.client.get('/api/v1/acoes_pngi/vigencias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # CREATE
        data = {
            'strdescricaovigenciapngi': 'Vigência Gestor',
            'datiniciovigencia': '2029-01-01',
            'datfinalvigencia': '2029-12-31',
            'isvigenciaativa': False
        }
        response = self.client.post('/api/v1/acoes_pngi/vigencias/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_gestor_can_activate_vigencia(self):
        """GESTOR_PNGI pode ativar vigência"""
        self.authenticate_as('gestor')
        response = self.client.post(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/ativar/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Bloqueado em Configurações
    # ------------------------------------------------------------------------
    
    def test_operador_cannot_create_vigencia(self):
        """OPERADOR_ACAO NÃO pode criar vigência (configuração)"""
        self.authenticate_as('operador')
        data = {
            'strdescricaovigenciapngi': 'Tentativa Operador',
            'datiniciovigencia': '2030-01-01',
            'datfinalvigencia': '2030-12-31'
        }
        response = self.client.post('/api/v1/acoes_pngi/vigencias/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_update_vigencia(self):
        """OPERADOR_ACAO NÃO pode atualizar vigência"""
        self.authenticate_as('operador')
        data = {'strdescricaovigenciapngi': 'Update Operador'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_delete_vigencia(self):
        """OPERADOR_ACAO NÃO pode deletar vigência"""
        self.authenticate_as('operador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_activate_vigencia(self):
        """OPERADOR_ACAO NÃO pode ativar vigência"""
        self.authenticate_as('operador')
        response = self.client.post(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/ativar/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_vigencias(self):
        """CONSULTOR_PNGI pode listar vigências"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/vigencias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_consultor_can_retrieve_vigencia(self):
        """CONSULTOR_PNGI pode buscar vigência específica"""
        self.authenticate_as('consultor')
        response = self.client.get(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_consultor_cannot_create_vigencia(self):
        """CONSULTOR_PNGI NÃO pode criar vigência"""
        self.authenticate_as('consultor')
        data = {
            'strdescricaovigenciapngi': 'Tentativa Consultor',
            'datiniciovigencia': '2031-01-01',
            'datfinalvigencia': '2031-12-31'
        }
        response = self.client.post('/api/v1/acoes_pngi/vigencias/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_cannot_update_vigencia(self):
        """CONSULTOR_PNGI NÃO pode atualizar vigência"""
        self.authenticate_as('consultor')
        data = {'strdescricaovigenciapngi': 'Update Consultor'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_cannot_delete_vigencia(self):
        """CONSULTOR_PNGI NÃO pode deletar vigência"""
        self.authenticate_as('consultor')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_cannot_activate_vigencia(self):
        """CONSULTOR_PNGI NÃO pode ativar vigência"""
        self.authenticate_as('consultor')
        response = self.client.post(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/ativar/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
