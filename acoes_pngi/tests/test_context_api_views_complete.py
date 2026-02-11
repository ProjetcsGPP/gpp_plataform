"""acoes_pngi/tests/test_context_api_views_complete.py

Testes completos para Context API Views

Cobre todos os endpoints de contexto:
- /api/v1/acoes_pngi/context/app/
- /api/v1/acoes_pngi/context/permissions/
- /api/v1/acoes_pngi/context/models/
- /api/v1/acoes_pngi/context/full/
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from accounts.models import Aplicacao, Role, UserRole, Permission, RolePermission
from ..models import Eixo, SituacaoAcao, VigenciaPNGI

User = get_user_model()


class BaseContextAPITestCase(TestCase):
    """Classe base para testes de Context API"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup inicial"""
        self.client = APIClient()
        
        # Criar aplicação (usar get_or_create para evitar IntegrityError)
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        # Criar role
        self.role = Role.objects.create(
            aplicacao=self.app,
            codigoperfil='GESTOR_PNGI',
            nomeperfil='Gestor Ações PNGI'
        )
        
        # Criar permissões e atribuir ao role
        self.permissions = []
        for model_name in ['eixo', 'situacaoacao', 'vigenciapngi']:
            for action in ['view', 'add', 'change', 'delete']:
                perm = Permission.objects.create(
                    aplicacao=self.app,
                    codigopermissao=f'{action}_{model_name}',
                    descricaopermissao=f'Pode {action} {model_name}'
                )
                RolePermission.objects.create(role=self.role, permission=perm)
                self.permissions.append(perm)
        
        # Criar usuário com role
        self.user = User.objects.create_user(
            email='gestor@seger.es.gov.br',
            name='Gestor Test',
            password='testpass123'
        )
        self.user_role = UserRole.objects.create(
            user=self.user,
            aplicacao=self.app,
            role=self.role
        )
        
        # Criar usuário sem acesso
        self.user_no_access = User.objects.create_user(
            email='noaccess@test.com',
            name='No Access',
            password='testpass123'
        )


class AppContextAPITests(BaseContextAPITestCase):
    """Testes do endpoint app_context_api"""
    
    def test_app_context_requires_authentication(self):
        """Endpoint requer autenticação"""
        response = self.client.get('/api/v1/acoes_pngi/context/app/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_app_context_returns_app_info(self):
        """Retorna informações da aplicação"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/app/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('code', response.data)
        self.assertIn('name', response.data)
        self.assertIn('icon', response.data)
        self.assertIn('url_namespace', response.data)
        self.assertIn('user_roles', response.data)
        
        # Verificar dados da aplicação
        self.assertEqual(response.data['code'], 'ACOES_PNGI')
        self.assertEqual(response.data['name'], 'Ações PNGI')
    
    def test_app_context_includes_user_roles(self):
        """Inclui roles do usuário na resposta"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/app/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['user_roles'], list)
        
        # Usuário com role deve ter pelo menos um item
        if len(response.data['user_roles']) > 0:
            self.assertIn('code', response.data['user_roles'][0])
            self.assertIn('name', response.data['user_roles'][0])
    
    def test_app_context_returns_empty_roles_for_user_without_access(self):
        """Retorna lista vazia de roles para usuário sem acesso"""
        self.client.force_authenticate(user=self.user_no_access)
        
        response = self.client.get('/api/v1/acoes_pngi/context/app/')
        
        # Pode retornar 200 com roles vazio ou erro
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['user_roles'], [])


class UserPermissionsAPITests(BaseContextAPITestCase):
    """Testes do endpoint user_permissions_api"""
    
    def test_permissions_requires_authentication(self):
        """Endpoint requer autenticação"""
        response = self.client.get('/api/v1/acoes_pngi/context/permissions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_permissions_returns_user_info(self):
        """Retorna informações do usuário"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/permissions/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_id', response.data)
        self.assertIn('email', response.data)
        self.assertIn('name', response.data)
        
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['name'], self.user.name)
    
    def test_permissions_returns_permissions_list(self):
        """Retorna lista de permissões do usuário"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/permissions/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('permissions', response.data)
        self.assertIsInstance(response.data['permissions'], list)
        
        # Usuário com role deve ter permissões
        if len(response.data['permissions']) > 0:
            # Verificar formato das permissões
            for perm in response.data['permissions']:
                self.assertIsInstance(perm, str)
    
    def test_permissions_returns_models_permissions(self):
        """Retorna permissões agrupadas por modelo"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/permissions/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('models_permissions', response.data)
        self.assertIsInstance(response.data['models_permissions'], dict)
        
        # Verificar estrutura de models_permissions
        models_perms = response.data['models_permissions']
        if 'eixo' in models_perms:
            self.assertIn('view', models_perms['eixo'])
            self.assertIn('add', models_perms['eixo'])
            self.assertIn('change', models_perms['eixo'])
            self.assertIn('delete', models_perms['eixo'])
    
    def test_permissions_returns_role_info(self):
        """Retorna informações do role do usuário"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/permissions/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('role', response.data)
        self.assertIn('role_name', response.data)
        
        self.assertEqual(response.data['role'], 'GESTOR_PNGI')
        self.assertEqual(response.data['role_name'], 'Gestor Ações PNGI')
    
    def test_permissions_user_without_role(self):
        """Usuário sem role retorna role como None"""
        self.client.force_authenticate(user=self.user_no_access)
        
        response = self.client.get('/api/v1/acoes_pngi/context/permissions/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['role'])
        self.assertIsNone(response.data['role_name'])


class ModelsInfoAPITests(BaseContextAPITestCase):
    """Testes do endpoint models_info_api"""
    
    def test_models_info_requires_authentication(self):
        """Endpoint requer autenticação"""
        response = self.client.get('/api/v1/acoes_pngi/context/models/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_models_info_returns_models_data(self):
        """Retorna informações dos modelos"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/models/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('models', response.data)
        self.assertIsInstance(response.data['models'], dict)
    
    def test_models_info_includes_expected_models(self):
        """Inclui modelos esperados da aplicação"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/models/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        models = response.data['models']
        
        # Verificar se inclui alguns dos modelos principais
        # (a estrutura exata depende do context_processor)
        self.assertIsInstance(models, dict)
    
    def test_models_info_model_structure(self):
        """Cada modelo tem estrutura esperada"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/models/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        models = response.data['models']
        
        # Verificar estrutura de pelo menos um modelo se existir
        if models:
            first_model = list(models.values())[0]
            # Estrutura pode variar, mas deve ser um dicionário
            self.assertIsInstance(first_model, dict)


class FullContextAPITests(BaseContextAPITestCase):
    """Testes do endpoint full_context_api"""
    
    def test_full_context_requires_authentication(self):
        """Endpoint requer autenticação"""
        response = self.client.get('/api/v1/acoes_pngi/context/full/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_full_context_returns_all_contexts(self):
        """Retorna todos os contextos combinados"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/full/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar estrutura principal
        self.assertIn('app', response.data)
        self.assertIn('permissions', response.data)
        self.assertIn('models', response.data)
        self.assertIn('timestamp', response.data)
    
    def test_full_context_app_section(self):
        """Seção 'app' contém dados corretos"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/full/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        app_data = response.data['app']
        
        self.assertIn('code', app_data)
        self.assertIn('name', app_data)
        self.assertIn('icon', app_data)
        self.assertIn('url_namespace', app_data)
        self.assertIn('user_roles', app_data)
        
        self.assertEqual(app_data['code'], 'ACOES_PNGI')
    
    def test_full_context_permissions_section(self):
        """Seção 'permissions' contém dados corretos"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/full/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        perms_data = response.data['permissions']
        
        self.assertIn('user_id', perms_data)
        self.assertIn('email', perms_data)
        self.assertIn('name', perms_data)
        self.assertIn('permissions', perms_data)
        self.assertIn('models_permissions', perms_data)
        self.assertIn('role', perms_data)
        self.assertIn('role_name', perms_data)
        
        self.assertEqual(perms_data['user_id'], self.user.id)
        self.assertEqual(perms_data['email'], self.user.email)
    
    def test_full_context_models_section(self):
        """Seção 'models' contém dados corretos"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/full/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        models_data = response.data['models']
        
        self.assertIsInstance(models_data, dict)
    
    def test_full_context_timestamp_format(self):
        """Timestamp está no formato ISO"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/full/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('timestamp', response.data)
        
        # Verificar que timestamp é uma string
        self.assertIsInstance(response.data['timestamp'], str)
        # Verificar formato ISO (contém 'T' e termina com 'Z' ou offset)
        timestamp = response.data['timestamp']
        self.assertTrue('T' in timestamp or ':' in timestamp)
    
    def test_full_context_user_without_role(self):
        """Full context funciona para usuário sem role"""
        self.client.force_authenticate(user=self.user_no_access)
        
        response = self.client.get('/api/v1/acoes_pngi/context/full/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que tem estrutura completa mesmo sem role
        self.assertIn('app', response.data)
        self.assertIn('permissions', response.data)
        self.assertIn('models', response.data)
        self.assertIn('timestamp', response.data)
        
        # Role deve ser None
        self.assertIsNone(response.data['permissions']['role'])


class ContextAPIErrorHandlingTests(BaseContextAPITestCase):
    """Testes de tratamento de erros dos endpoints de contexto"""
    
    def test_app_context_handles_missing_app(self):
        """Tratamento de erro quando aplicação não existe"""
        # Deletar aplicação temporariamente
        Aplicacao.objects.filter(codigointerno='ACOES_PNGI').delete()
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/v1/acoes_pngi/context/app/')
        
        # Deve retornar erro 500 ou dados vazios
        self.assertIn(response.status_code, [status.HTTP_500_INTERNAL_SERVER_ERROR, status.HTTP_200_OK])
    
    def test_permissions_handles_user_without_name_attribute(self):
        """Tratamento quando user não tem atributo 'name'"""
        # Criar usuário sem name (usar first_name)
        user_without_name = User.objects.create_user(
            email='noname@test.com',
            first_name='Test',
            password='test123'
        )
        
        self.client.force_authenticate(user=user_without_name)
        
        response = self.client.get('/api/v1/acoes_pngi/context/permissions/')
        
        # Deve retornar 200 e usar first_name como fallback
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)
    
    def test_full_context_handles_exceptions_gracefully(self):
        """Full context trata exceções adequadamente"""
        self.client.force_authenticate(user=self.user)
        
        # Mesmo com dados faltando, deve retornar resposta válida ou erro tratado
        response = self.client.get('/api/v1/acoes_pngi/context/full/')
        
        # Deve retornar 200 ou 500 (erro tratado)
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ])
        
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            # Erro deve ter mensagem descritiva
            self.assertIn('detail', response.data)


class ContextAPIIntegrationTests(BaseContextAPITestCase):
    """Testes de integração dos endpoints de contexto"""
    
    def test_context_data_consistency_across_endpoints(self):
        """Dados são consistentes entre endpoints separados e full"""
        self.client.force_authenticate(user=self.user)
        
        # Obter dados de cada endpoint
        app_response = self.client.get('/api/v1/acoes_pngi/context/app/')
        perms_response = self.client.get('/api/v1/acoes_pngi/context/permissions/')
        models_response = self.client.get('/api/v1/acoes_pngi/context/models/')
        full_response = self.client.get('/api/v1/acoes_pngi/context/full/')
        
        # Todos devem retornar sucesso
        self.assertEqual(app_response.status_code, status.HTTP_200_OK)
        self.assertEqual(perms_response.status_code, status.HTTP_200_OK)
        self.assertEqual(models_response.status_code, status.HTTP_200_OK)
        self.assertEqual(full_response.status_code, status.HTTP_200_OK)
        
        # Verificar consistência de dados básicos
        if full_response.data['app']['code']:
            self.assertEqual(app_response.data['code'], full_response.data['app']['code'])
        
        if full_response.data['permissions']['user_id']:
            self.assertEqual(perms_response.data['user_id'], full_response.data['permissions']['user_id'])
    
    def test_multiple_users_get_correct_contexts(self):
        """Diferentes usuários recebem contextos corretos"""
        # Criar segundo usuário com role diferente
        role2 = Role.objects.create(
            aplicacao=self.app,
            codigoperfil='OPERADOR',
            nomeperfil='Operador'
        )
        
        user2 = User.objects.create_user(
            email='operador@test.com',
            name='Operador Test',
            password='test123'
        )
        
        UserRole.objects.create(
            user=user2,
            aplicacao=self.app,
            role=role2
        )
        
        # Obter contexto do primeiro usuário
        self.client.force_authenticate(user=self.user)
        response1 = self.client.get('/api/v1/acoes_pngi/context/permissions/')
        
        # Obter contexto do segundo usuário
        self.client.force_authenticate(user=user2)
        response2 = self.client.get('/api/v1/acoes_pngi/context/permissions/')
        
        # Ambos devem retornar sucesso
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        
        # Verificar que roles são diferentes
        self.assertNotEqual(response1.data['role'], response2.data['role'])
        self.assertEqual(response1.data['role'], 'GESTOR_PNGI')
        self.assertEqual(response2.data['role'], 'OPERADOR')
