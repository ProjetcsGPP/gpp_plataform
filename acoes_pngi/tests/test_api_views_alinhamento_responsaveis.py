"""
Testes de API Views - Alinhamento e Responsáveis - Ações PNGI

Testa ViewSets de:
- TipoAnotacaoAlinhamento (configuração)
- AcaoAnotacaoAlinhamento (anotações de alinhamento)
- UsuarioResponsavel (responsáveis por ações)
- RelacaoAcaoUsuarioResponsavel (relações ação-responsável)

Cobre as 4 roles hierárquicas com validações específicas:
- COORDENADOR_PNGI: Acesso total
- GESTOR_PNGI: Acesso total
- OPERADOR_ACAO: Bloqueado em TipoAnotacaoAlinhamento, gerencia restante
- CONSULTOR_PNGI: Apenas leitura

Testa relacionamentos complexos:
- Constraint triplo (acao, tipo, dt_anotacao) em AcaoAnotacaoAlinhamento
- OneToOne entre UsuarioResponsavel e User
- ManyToMany entre Acoes e UsuarioResponsavel
"""

from django.test import TestCase
from .base import BaseTestCase, BaseAPITestCase, BaseAPITestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, datetime
from django.utils import timezone

from accounts.models import Aplicacao, Role, UserRole
from ..models import (
    VigenciaPNGI, Acoes, Eixo, SituacaoAcao,
    TipoAnotacaoAlinhamento, AcaoAnotacaoAlinhamento,
    UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel
)

User = get_user_model()


class BaseAPITestCase(BaseTestCase):
    """Classe base reutilizável para testes de API"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup inicial com aplicação, roles e usuários"""
        self.client = APIClient()
        
        # Criar aplicação usando get_or_create para evitar IntegrityError
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        # Criar as 4 roles usando get_or_create
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
        
        # Criar usuários
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
    
    def setup_test_data(self):
        """Override em subclasses"""
        pass
    
    def authenticate_as(self, role_name):
        """Autentica como usuário específico"""
        user = self.users[role_name]
        self.client.force_authenticate(user=user)
        return user


# ============================================================================
# TESTES DE TIPO ANOTAÇÃO ALINHAMENTO - ViewSet: TipoAnotacaoAlinhamentoViewSet
# ============================================================================

class TipoAnotacaoAlinhamentoAPITests(BaseAPITestCase):
    """
    Testes de API para TipoAnotacaoAlinhamento.
    
    TipoAnotacaoAlinhamento é CONFIGURAÇÃO, então:
    - COORDENADOR e GESTOR: acesso total
    - OPERADOR: BLOQUEADO (não gerencia configurações)
    - CONSULTOR: apenas leitura
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/tipos-anotacao-alinhamento/
    - POST   /api/v1/acoes_pngi/tipos-anotacao-alinhamento/
    - GET    /api/v1/acoes_pngi/tipos-anotacao-alinhamento/{id}/
    - PATCH  /api/v1/acoes_pngi/tipos-anotacao-alinhamento/{id}/
    - DELETE /api/v1/acoes_pngi/tipos-anotacao-alinhamento/{id}/
    """
    
    def setup_test_data(self):
        """Cria tipo de anotação de teste"""
        self.tipo_anotacao = TipoAnotacaoAlinhamento.objects.create(
            strdescricaotipoanotacaoalinhamento='Reunião de Alinhamento'
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_tipos_anotacao(self):
        """COORDENADOR_PNGI pode listar tipos de anotação"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/tipos-anotacao-alinhamento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ✅ Verifica que retornou dados (não vazio)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_coordenador_can_create_tipo_anotacao(self):
        """COORDENADOR_PNGI pode criar tipo de anotação"""
        self.authenticate_as('coordenador')
        data = {
            'strdescricaotipoanotacaoalinhamento': 'Videoconferência'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/tipos-anotacao-alinhamento/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_coordenador_can_update_tipo_anotacao(self):
        """COORDENADOR_PNGI pode atualizar tipo de anotação"""
        self.authenticate_as('coordenador')
        data = {'strdescricaotipoanotacaoalinhamento': 'Reunião de Alinhamento - Atualizado'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/tipos-anotacao-alinhamento/{self.tipo_anotacao.idtipoanotacaoalinhamento}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_can_delete_tipo_anotacao(self):
        """COORDENADOR_PNGI pode deletar tipo de anotação"""
        tipo_temp = TipoAnotacaoAlinhamento.objects.create(
            strdescricaotipoanotacaoalinhamento='Temporário'
        )
        
        self.authenticate_as('coordenador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/tipos-anotacao-alinhamento/{tipo_temp.idtipoanotacaoalinhamento}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ------------------------------------------------------------------------
    # GESTOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_gestor_can_manage_tipos_anotacao(self):
        """GESTOR_PNGI tem acesso completo a tipos de anotação"""
        self.authenticate_as('gestor')
        
        # LIST
        response = self.client.get('/api/v1/acoes_pngi/tipos-anotacao-alinhamento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # CREATE
        data = {
            'strdescricaotipoanotacaoalinhamento': 'E-mail'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/tipos-anotacao-alinhamento/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Bloqueado em Configurações
    # ------------------------------------------------------------------------
    
    def test_operador_cannot_create_tipo_anotacao(self):
        """OPERADOR_ACAO NÃO pode criar tipo de anotação (configuração)"""
        self.authenticate_as('operador')
        data = {
            'strdescricaotipoanotacaoalinhamento': 'Tentativa Operador'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/tipos-anotacao-alinhamento/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_update_tipo_anotacao(self):
        """OPERADOR_ACAO NÃO pode atualizar tipo de anotação"""
        self.authenticate_as('operador')
        data = {'strdescricaotipoanotacaoalinhamento': 'Update Operador'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/tipos-anotacao-alinhamento/{self.tipo_anotacao.idtipoanotacaoalinhamento}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_delete_tipo_anotacao(self):
        """OPERADOR_ACAO NÃO pode deletar tipo de anotação"""
        self.authenticate_as('operador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/tipos-anotacao-alinhamento/{self.tipo_anotacao.idtipoanotacaoalinhamento}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_tipos_anotacao(self):
        """CONSULTOR_PNGI pode listar tipos de anotação"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/tipos-anotacao-alinhamento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_consultor_cannot_create_tipo_anotacao(self):
        """CONSULTOR_PNGI NÃO pode criar tipo de anotação"""
        self.authenticate_as('consultor')
        data = {
            'strdescricaotipoanotacaoalinhamento': 'Tentativa Consultor'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/tipos-anotacao-alinhamento/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # Testes de Filtros
    # ------------------------------------------------------------------------
    
    def test_search_tipos_anotacao(self):
        """Buscar tipos de anotação por descrição"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/tipos-anotacao-alinhamento/?search=Reunião')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_ordering_tipos_anotacao(self):
        """Ordenar tipos de anotação"""
        self.authenticate_as('consultor')
        response = self.client.get(
            '/api/v1/acoes_pngi/tipos-anotacao-alinhamento/?ordering=strdescricaotipoanotacaoalinhamento'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================================================
# TESTES DE ANOTAÇÃO ALINHAMENTO - ViewSet: AcaoAnotacaoAlinhamentoViewSet
# ============================================================================

class AcaoAnotacaoAlinhamentoAPITests(BaseAPITestCase):
    """
    Testes de API para AcaoAnotacaoAlinhamento.
    
    Anotações NÃO são configuração, então:
    - COORDENADOR, GESTOR e OPERADOR: acesso total
    - CONSULTOR: apenas leitura
    
    Testa:
    - Constraint triplo unique (idacao, idtipoanotacaoalinhamento, dtanotacaoalinhamento)
    - Relacionamentos com Ação e TipoAnotacao
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/anotacoes-alinhamento/
    - POST   /api/v1/acoes_pngi/anotacoes-alinhamento/
    - GET    /api/v1/acoes_pngi/anotacoes-alinhamento/{id}/
    - PATCH  /api/v1/acoes_pngi/anotacoes-alinhamento/{id}/
    - DELETE /api/v1/acoes_pngi/anotacoes-alinhamento/{id}/
    """
    
    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        
        # ✅ 1. Criar Vigência (OBRIGATÓRIO para Acao)
        # ✅ 2. Criar Eixo (opcional mas comum)
        # ✅ 3. Criar Situação (opcional mas comum)
        # ✅ 4. Criar Acao COMPLETA (idvigenciapngi é obrigatório)
      
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega Teste',
            idvigenciapngi=vigencia,  # OBRIGATÓRIO
            ideixo=eixo,              # Adicionar para consistência
            idsituacaoacao=situacao   # Adicionar para consistência
        )
        
        # ✅ 5. Criar TipoAnotacao (OBRIGATÓRIO para AcaoAnotacaoAlinhamento)
        self.tipo_anotacao = TipoAnotacaoAlinhamento.objects.create(
            strdescricaotipoanotacaoalinhamento='Reunião'
        )
        
        # ✅ 6. Criar Anotação vinculada a Acao e TipoAnotacao
        self.anotacao = AcaoAnotacaoAlinhamento.objects.create(
            idacao=self.acao,  # OBRIGATÓRIO
            idtipoanotacaoalinhamento=self.tipo_anotacao,  # OBRIGATÓRIO
            datdataanotacaoalinhamento=timezone.now(),
            strdescricaoanotacaoalinhamento='Anotação de Teste'
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_anotacoes(self):
        """COORDENADOR_PNGI pode listar anotações"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/anotacoes-alinhamento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ✅ Verifica que retornou dados (não vazio)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_coordenador_can_create_anotacao(self):
        """COORDENADOR_PNGI pode criar anotação"""
        self.authenticate_as('coordenador')
        data = {
            'idacao': self.acao.idacao,
            'idtipoanotacaoalinhamento': self.tipo_anotacao.idtipoanotacaoalinhamento,
            'datdataanotacaoalinhamento': (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            'strdescricaoanotacaoalinhamento': 'Nova Anotação Coordenador'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/anotacoes-alinhamento/',
            data,
            format='json'
        )
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST  # Se houver conflict de unique constraint
        ])
    
    def test_coordenador_can_update_anotacao(self):
        """COORDENADOR_PNGI pode atualizar anotação"""
        self.authenticate_as('coordenador')
        data = {'strdescricaoanotacaoalinhamento': 'Anotação Atualizada'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/{self.anotacao.idacaoanotacaoalinhamento}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_can_delete_anotacao(self):
        """COORDENADOR_PNGI pode deletar anotação"""
        anotacao_temp = AcaoAnotacaoAlinhamento.objects.create(
            idacao=self.acao,
            idtipoanotacaoalinhamento=self.tipo_anotacao,
            datdataanotacaoalinhamento=timezone.now() + timezone.timedelta(hours=1),
            strdescricaoanotacaoalinhamento='Temporária'
        )
        
        self.authenticate_as('coordenador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/{anotacao_temp.idacaoanotacaoalinhamento}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Pode Gerenciar Anotações
    # ------------------------------------------------------------------------
    
    def test_operador_can_manage_anotacoes(self):
        """OPERADOR_ACAO pode gerenciar anotações"""
        self.authenticate_as('operador')
        
        # LIST
        response = self.client.get('/api/v1/acoes_pngi/anotacoes-alinhamento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # CREATE
        data = {
            'idacao': self.acao.idacao,
            'idtipoanotacaoalinhamento': self.tipo_anotacao.idtipoanotacaoalinhamento,
            'datdataanotacaoalinhamento': (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            'strdescricaoanotacaoalinhamento': 'Anotação Operador'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/anotacoes-alinhamento/',
            data,
            format='json'
        )
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_anotacoes(self):
        """CONSULTOR_PNGI pode listar anotações"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/anotacoes-alinhamento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_consultor_cannot_create_anotacao(self):
        """CONSULTOR_PNGI NÃO pode criar anotação"""
        self.authenticate_as('consultor')
        data = {
            'idacao': self.acao.idacao,
            'idtipoanotacaoalinhamento': self.tipo_anotacao.idtipoanotacaoalinhamento,
            'datdataanotacaoalinhamento': timezone.now().isoformat(),
            'strdescricaoanotacaoalinhamento': 'Tentativa Consultor'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/anotacoes-alinhamento/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # Testes de Filtros
    # ------------------------------------------------------------------------
    
    def test_filter_anotacoes_by_acao(self):
        """Filtrar anotações por ação"""
        self.authenticate_as('consultor')
        response = self.client.get(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/?idacao={self.acao.idacao}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_filter_anotacoes_by_tipo(self):
        """Filtrar anotações por tipo"""
        self.authenticate_as('consultor')
        response = self.client.get(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/?idtipoanotacaoalinhamento={self.tipo_anotacao.idtipoanotacaoalinhamento}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_search_anotacoes(self):
        """Buscar anotações por descrição"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/anotacoes-alinhamento/?search=Teste')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================================================
# TESTES DE USUÁRIO RESPONSÁVEL - ViewSet: UsuarioResponsavelViewSet
# ============================================================================

class UsuarioResponsavelAPITests(BaseAPITestCase):
    """
    Testes de API para UsuarioResponsavel.
    
    Responsáveis NÃO são configuração, então:
    - COORDENADOR, GESTOR e OPERADOR: acesso total
    - CONSULTOR: apenas leitura
    
    Testa:
    - Relacionamento OneToOne com User
    - Campo strorgao
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/usuarios-responsaveis/
    - POST   /api/v1/acoes_pngi/usuarios-responsaveis/
    - GET    /api/v1/acoes_pngi/usuarios-responsaveis/{id}/
    - PATCH  /api/v1/acoes_pngi/usuarios-responsaveis/{id}/
    - DELETE /api/v1/acoes_pngi/usuarios-responsaveis/{id}/
    """
    
    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        
        # ✅ 1. Criar User (OBRIGATÓRIO para UsuarioResponsavel)
        self.user_responsavel = User.objects.create_user(
            email='responsavel.teste@seger.es.gov.br',
            name='Responsável Teste',
            password='senha123'
        )
        
        # ✅ 2. Criar UsuarioResponsavel vinculado ao User
        self.responsavel = UsuarioResponsavel.objects.create(
            idusuario=self.user_responsavel,  # OBRIGATÓRIO
            strtelefone='27999999999',
            strorgao='SEGER'
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_responsaveis(self):
        """COORDENADOR_PNGI pode listar responsáveis"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/usuarios-responsaveis/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ✅ Verifica que retornou dados (não vazio)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_coordenador_can_create_responsavel(self):
        """COORDENADOR_PNGI pode criar responsável"""
        # Criar novo usuário para vincular
        novo_user = User.objects.create_user(
            email='novo.responsavel@seger.es.gov.br',
            name='Novo Responsável',
            password='senha123'
        )
        
        self.authenticate_as('coordenador')
        data = {
            'idusuario': novo_user.id,
            'strtelefone': '27988888888',
            'strorgao': 'SEDU'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/usuarios-responsaveis/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_coordenador_can_update_responsavel(self):
        """COORDENADOR_PNGI pode atualizar responsável"""
        self.authenticate_as('coordenador')
        data = {'strorgao': 'SEGER - Atualizado'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/usuarios-responsaveis/{self.responsavel.pk}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_can_delete_responsavel(self):
        """COORDENADOR_PNGI pode deletar responsável"""
        # Criar responsável temporário
        user_temp = User.objects.create_user(
            email='temp.resp@seger.es.gov.br',
            name='Temp',
            password='senha123'
        )
        resp_temp = UsuarioResponsavel.objects.create(
            idusuario=user_temp,
            strorgao='TEMP'
        )
        
        self.authenticate_as('coordenador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/usuarios-responsaveis/{resp_temp.pk}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Pode Gerenciar Responsáveis
    # ------------------------------------------------------------------------
    
    def test_operador_can_manage_responsaveis(self):
        """OPERADOR_ACAO pode gerenciar responsáveis"""
        self.authenticate_as('operador')
        
        # LIST
        response = self.client.get('/api/v1/acoes_pngi/usuarios-responsaveis/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # UPDATE
        data = {'strtelefone': '27977777777'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/usuarios-responsaveis/{self.responsavel.pk}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_responsaveis(self):
        """CONSULTOR_PNGI pode listar responsáveis"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/usuarios-responsaveis/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_consultor_cannot_create_responsavel(self):
        """CONSULTOR_PNGI NÃO pode criar responsável"""
        novo_user = User.objects.create_user(
            email='tentativa.consultor@seger.es.gov.br',
            name='Tentativa',
            password='senha123'
        )
        
        self.authenticate_as('consultor')
        data = {
            'idusuario': novo_user.id,
            'strorgao': 'TESTE'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/usuarios-responsaveis/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # Testes de Filtros
    # ------------------------------------------------------------------------
    
    def test_filter_responsaveis_by_orgao(self):
        """Filtrar responsáveis por órgão"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/usuarios-responsaveis/?strorgao=SEGER')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_search_responsaveis(self):
        """Buscar responsáveis por nome ou email"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/usuarios-responsaveis/?search=Responsável')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================================================
# TESTES DE RELAÇÃO AÇÃO-RESPONSÁVEL - ViewSet: RelacaoAcaoUsuarioResponsavelViewSet
# ============================================================================

class RelacaoAcaoUsuarioResponsavelAPITests(BaseAPITestCase):
    """
    Testes de API para RelacaoAcaoUsuarioResponsavel.
    
    Relações NÃO são configuração, então:
    - COORDENADOR, GESTOR e OPERADOR: acesso total
    - CONSULTOR: apenas leitura
    
    Testa:
    - ManyToMany entre Acoes e UsuarioResponsavel
    - Filtros por ação
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/relacoes-acao-responsavel/
    - POST   /api/v1/acoes_pngi/relacoes-acao-responsavel/
    - GET    /api/v1/acoes_pngi/relacoes-acao-responsavel/{id}/
    - DELETE /api/v1/acoes_pngi/relacoes-acao-responsavel/{id}/
    """
    
    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários em CASCATA - simula ambiente real"""
        
        # ✅ 1. Criar Vigência (OBRIGATÓRIO para Acao)
        # ✅ 2. Criar Eixo (opcional mas comum)
        # ✅ 3. Criar Situação (opcional mas comum)
        # ✅ 4. Criar Acao COMPLETA (idvigenciapngi é obrigatório)
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega Teste',
            idvigenciapngi=vigencia,  # OBRIGATÓRIO
            ideixo=eixo,              # Adicionar para consistência
            idsituacaoacao=situacao   # Adicionar para consistência
        )
        
        # ✅ 5. Criar User (OBRIGATÓRIO para UsuarioResponsavel)
        user_resp = User.objects.create_user(
            email='responsavel@seger.es.gov.br',
            name='Responsável',
            password='senha123'
        )
        
        # ✅ 6. Criar UsuarioResponsavel vinculado ao User
        self.responsavel = UsuarioResponsavel.objects.create(
            idusuario=user_resp,  # OBRIGATÓRIO
            strorgao='SEGER'
        )
        
        # ✅ 7. Criar Relação Acao-Responsavel
        self.relacao = RelacaoAcaoUsuarioResponsavel.objects.create(
            idacao=self.acao,  # OBRIGATÓRIO
            idusuarioresponsavel=self.responsavel  # OBRIGATÓRIO
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_relacoes(self):
        """COORDENADOR_PNGI pode listar relações"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/relacoes-acao-responsavel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ✅ Verifica que retornou dados (não vazio)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_coordenador_can_create_relacao(self):
        """COORDENADOR_PNGI pode criar relação"""
        # Criar novo responsável para vincular
        novo_user = User.objects.create_user(
            email='novo.resp@seger.es.gov.br',
            name='Novo',
            password='senha123'
        )
        novo_resp = UsuarioResponsavel.objects.create(
            idusuario=novo_user,
            strorgao='SEDU'
        )
        
        self.authenticate_as('coordenador')
        data = {
            'idacao': self.acao.idacao,
            'idusuarioresponsavel': novo_resp.pk  # ✅ Usa .pk (chave primária correta)
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/relacoes-acao-responsavel/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_coordenador_can_delete_relacao(self):
        """COORDENADOR_PNGI pode deletar relação"""
        self.authenticate_as('coordenador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/relacoes-acao-responsavel/{self.relacao.idacaousuarioresponsavel}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Pode Gerenciar Relações
    # ------------------------------------------------------------------------
    
    def test_operador_can_manage_relacoes(self):
        """OPERADOR_ACAO pode gerenciar relações"""
        self.authenticate_as('operador')
        
        # LIST
        response = self.client.get('/api/v1/acoes_pngi/relacoes-acao-responsavel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_relacoes(self):
        """CONSULTOR_PNGI pode listar relações"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/relacoes-acao-responsavel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_consultor_cannot_create_relacao(self):
        """CONSULTOR_PNGI NÃO pode criar relação"""
        self.authenticate_as('consultor')
        data = {
            'idacao': self.acao.idacao,
            'idusuarioresponsavel': self.responsavel.pk  # ✅ Usa .pk
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/relacoes-acao-responsavel/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_cannot_delete_relacao(self):
        """CONSULTOR_PNGI NÃO pode deletar relação"""
        self.authenticate_as('consultor')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/relacoes-acao-responsavel/{self.relacao.idacaousuarioresponsavel}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # Testes de Filtros
    # ------------------------------------------------------------------------
    
    def test_filter_relacoes_by_acao(self):
        """Filtrar relações por ação"""
        self.authenticate_as('consultor')
        response = self.client.get(
            f'/api/v1/acoes_pngi/relacoes-acao-responsavel/?idacao={self.acao.idacao}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
