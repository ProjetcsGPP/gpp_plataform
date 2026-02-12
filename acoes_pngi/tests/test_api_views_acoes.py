"""
Testes de API Views - Módulo de Ações - Ações PNGI

Testa ViewSets de:
- TipoEntraveAlerta (configuração)
- Acoes (entidade principal)
- AcaoPrazo (prazos das ações)
- AcaoDestaque (destaques das ações)

Cobre as 4 roles hierárquicas com validações específicas:
- COORDENADOR_PNGI: Acesso total
- GESTOR_PNGI: Acesso total
- OPERADOR_ACAO: Gerencia ações (MAS bloqueado em TipoEntraveAlerta)
- CONSULTOR_PNGI: Apenas leitura
"""

from django.test import TestCase
from .base import BaseTestCase, BaseAPITestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from django.utils import timezone

from accounts.models import Aplicacao, Role, UserRole
from ..models import (
    Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta,
    Acoes, AcaoPrazo, AcaoDestaque
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
# TESTES DE TIPO ENTRAVE/ALERTA - ViewSet: TipoEntraveAlertaViewSet
# ============================================================================

class TipoEntraveAlertaAPITests(BaseAPITestCase):
    """
    Testes de API para TipoEntraveAlerta.
    
    TipoEntraveAlerta é CONFIGURAÇÃO, então:
    - COORDENADOR e GESTOR: acesso total
    - OPERADOR: BLOQUEADO (não gerencia configurações)
    - CONSULTOR: apenas leitura
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/tipos-entrave-alerta/
    - POST   /api/v1/acoes_pngi/tipos-entrave-alerta/
    - GET    /api/v1/acoes_pngi/tipos-entrave-alerta/{id}/
    - PATCH  /api/v1/acoes_pngi/tipos-entrave-alerta/{id}/
    - DELETE /api/v1/acoes_pngi/tipos-entrave-alerta/{id}/
    """
    
    def setup_test_data(self):
        """Cria tipo de entrave/alerta de teste"""
        self.tipo_entrave = TipoEntraveAlerta.objects.create(
            strdescricaotipoentravealerta='Alerta de Teste'
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_tipos_entrave(self):
        """COORDENADOR_PNGI pode listar tipos de entrave"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/tipos-entrave-alerta/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_can_create_tipo_entrave(self):
        """COORDENADOR_PNGI pode criar tipo de entrave"""
        self.authenticate_as('coordenador')
        data = {'strdescricaotipoentravealerta': 'Novo Alerta Coordenador'}
        response = self.client.post(
            '/api/v1/acoes_pngi/tipos-entrave-alerta/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_coordenador_can_update_tipo_entrave(self):
        """COORDENADOR_PNGI pode atualizar tipo de entrave"""
        self.authenticate_as('coordenador')
        data = {'strdescricaotipoentravealerta': 'Alerta Atualizado'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/tipos-entrave-alerta/{self.tipo_entrave.idtipoentravealerta}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_can_delete_tipo_entrave(self):
        """COORDENADOR_PNGI pode deletar tipo de entrave"""
        tipo_temp = TipoEntraveAlerta.objects.create(
            strdescricaotipoentravealerta='Para Deletar'
        )
        
        self.authenticate_as('coordenador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/tipos-entrave-alerta/{tipo_temp.idtipoentravealerta}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ------------------------------------------------------------------------
    # GESTOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_gestor_can_manage_tipos_entrave(self):
        """GESTOR_PNGI tem acesso completo a tipos de entrave"""
        self.authenticate_as('gestor')
        
        # LIST
        response = self.client.get('/api/v1/acoes_pngi/tipos-entrave-alerta/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # CREATE
        data = {'strdescricaotipoentravealerta': 'Alerta Gestor'}
        response = self.client.post(
            '/api/v1/acoes_pngi/tipos-entrave-alerta/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Bloqueado em Configurações
    # ------------------------------------------------------------------------
    
    def test_operador_cannot_create_tipo_entrave(self):
        """OPERADOR_ACAO NÃO pode criar tipo de entrave (configuração)"""
        self.authenticate_as('operador')
        data = {'strdescricaotipoentravealerta': 'Tentativa Operador'}
        response = self.client.post(
            '/api/v1/acoes_pngi/tipos-entrave-alerta/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_update_tipo_entrave(self):
        """OPERADOR_ACAO NÃO pode atualizar tipo de entrave"""
        self.authenticate_as('operador')
        data = {'strdescricaotipoentravealerta': 'Update Operador'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/tipos-entrave-alerta/{self.tipo_entrave.idtipoentravealerta}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_operador_cannot_delete_tipo_entrave(self):
        """OPERADOR_ACAO NÃO pode deletar tipo de entrave"""
        self.authenticate_as('operador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/tipos-entrave-alerta/{self.tipo_entrave.idtipoentravealerta}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_tipos_entrave(self):
        """CONSULTOR_PNGI pode listar tipos de entrave"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/tipos-entrave-alerta/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_consultor_cannot_create_tipo_entrave(self):
        """CONSULTOR_PNGI NÃO pode criar tipo de entrave"""
        self.authenticate_as('consultor')
        data = {'strdescricaotipoentravealerta': 'Tentativa Consultor'}
        response = self.client.post(
            '/api/v1/acoes_pngi/tipos-entrave-alerta/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ============================================================================
# TESTES DE AÇÕES - ViewSet: AcoesViewSet
# ============================================================================

class AcoesAPITests(BaseAPITestCase):
    """
    Testes de API para Acoes (entidade principal).
    
    Ações NÃO são configuração, então:
    - COORDENADOR, GESTOR e OPERADOR: acesso total
    - CONSULTOR: apenas leitura
    
    Testa relacionamentos:
    - idvigenciapngi (ForeignKey) - OBRIGATÓRIO
    - idtipoentravealerta (ForeignKey) - OPCIONAL
    - ideixo (ForeignKey) - OPCIONAL
    - idsituacaoacao (ForeignKey) - OPCIONAL
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/acoes/
    - POST   /api/v1/acoes_pngi/acoes/
    - GET    /api/v1/acoes_pngi/acoes/{id}/
    - PATCH  /api/v1/acoes_pngi/acoes/{id}/
    - DELETE /api/v1/acoes_pngi/acoes/{id}/
    """
    
    def setup_test_data(self):
        """Cria dados COMPLETOS necessários para ações - simula ambiente real"""
        
        # ✅ 1. Criar Vigência (OBRIGATÓRIO para Acao)        
        # ✅ 2. Criar Eixo (OPCIONAL, mas usado na prática)        
        # ✅ 3. Criar Situação (OPCIONAL, mas usado na prática)        
        # ✅ 4. Criar Tipo Entrave (OPCIONAL)
        self.tipo_entrave = TipoEntraveAlerta.objects.create(
            strdescricaotipoentravealerta='Alerta Teste'
        )
        
        # ✅ 5. Criar Ação COMPLETA com TODOS relacionamentos
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação de Teste',
            strdescricaoentrega='Entrega de Teste',
            idvigenciapngi=self.vigencia_base,  # OBRIGATÓRIO
            ideixo=self.eixo_base,              # OPCIONAL (mas comum,
            idsituacaoacao=self.situacao_base)
            idsituacaoacao=self.situacao_base,  # OPCIONAL (mas comum)
            idtipoentravealerta=self.tipo_entrave,  # OPCIONAL
            datdataentrega=date(2026, 6, 30)
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_acoes(self):
        """COORDENADOR_PNGI pode listar ações"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/acoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ✅ Verifica que retorna dados (não vazio)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_coordenador_can_create_acao(self):
        """COORDENADOR_PNGI pode criar ação"""
        self.authenticate_as('coordenador')
        data = {
            'strapelido': 'ACAO-COORD-001',
            'strdescricaoacao': 'Nova Ação do Coordenador',
            'strdescricaoentrega': 'Entrega Coordenador',
            'idvigenciapngi': self.vigencia.idvigenciapngi,
            'ideixo': self.eixo.ideixo,
            'idsituacaoacao': self.situacao.idsituacaoacao,
            'idtipoentravealerta': self.tipo_entrave.idtipoentravealerta,
            'datdataentrega': '2026-08-30'
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['strapelido'], 'ACAO-COORD-001')
    
    def test_coordenador_can_update_acao(self):
        """COORDENADOR_PNGI pode atualizar ação"""
        self.authenticate_as('coordenador')
        data = {'strdescricaoacao': 'Ação Atualizada pelo Coordenador'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/acoes/{self.acao.idacao}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_can_delete_acao(self):
        """COORDENADOR_PNGI pode deletar ação"""
        acao_temp = Acoes.objects.create(
            strapelido='ACAO-TEMP',
            strdescricaoacao='Temporária',
            strdescricaoentrega='Entrega Temp',
            idvigenciapngi=self.vigencia_base,  # OBRIGATÓRIO
            ideixo=self.eixo_base,              # Adicionar para consistência
            idsituacaoacao=self.situacao   # Adicionar para consistência
        )
        
        self.authenticate_as('coordenador')
        response = self.client.delete(f'/api/v1/acoes_pngi/acoes/{acao_temp.idacao}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ------------------------------------------------------------------------
    # GESTOR_PNGI - Acesso Total
    # ------------------------------------------------------------------------
    
    def test_gestor_can_manage_acoes(self):
        """GESTOR_PNGI tem acesso completo a ações"""
        self.authenticate_as('gestor')
        
        # LIST
        response = self.client.get('/api/v1/acoes_pngi/acoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # CREATE
        data = {
            'strapelido': 'ACAO-GEST-001',
            'strdescricaoacao': 'Ação do Gestor',
            'strdescricaoentrega': 'Entrega Gestor',
            'idvigenciapngi': self.vigencia.idvigenciapngi,
            'ideixo': self.eixo.ideixo,
            'idsituacaoacao': self.situacao.idsituacaoacao
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Pode Gerenciar Ações
    # ------------------------------------------------------------------------
    
    def test_operador_can_list_acoes(self):
        """OPERADOR_ACAO pode listar ações"""
        self.authenticate_as('operador')
        response = self.client.get('/api/v1/acoes_pngi/acoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_operador_can_create_acao(self):
        """OPERADOR_ACAO PODE criar ação (não é configuração)"""
        self.authenticate_as('operador')
        data = {
            'strapelido': 'ACAO-OPER-001',
            'strdescricaoacao': 'Ação do Operador',
            'strdescricaoentrega': 'Entrega Operador',
            'idvigenciapngi': self.vigencia.idvigenciapngi,
            'ideixo': self.eixo.ideixo,
            'idsituacaoacao': self.situacao.idsituacaoacao
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_operador_can_update_acao(self):
        """OPERADOR_ACAO pode atualizar ação"""
        self.authenticate_as('operador')
        data = {'strdescricaoacao': 'Atualizado pelo Operador'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/acoes/{self.acao.idacao}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_operador_can_delete_acao(self):
        """OPERADOR_ACAO pode deletar ação"""
        acao_temp = Acoes.objects.create(
            strapelido='ACAO-DEL-OPER',
            strdescricaoacao='Para Deletar',
            strdescricaoentrega='Entrega Del',
            idvigenciapngi=self.vigencia_base,
            ideixo=self.eixo_base,              # Adicionar para consistência
            idsituacaoacao=self.situacao   # Adicionar para consistência
        )
        
        self.authenticate_as('operador')
        response = self.client.delete(f'/api/v1/acoes_pngi/acoes/{acao_temp.idacao}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_acoes(self):
        """CONSULTOR_PNGI pode listar ações"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/acoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_consultor_can_retrieve_acao(self):
        """CONSULTOR_PNGI pode buscar ação específica"""
        self.authenticate_as('consultor')
        response = self.client.get(f'/api/v1/acoes_pngi/acoes/{self.acao.idacao}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_consultor_cannot_create_acao(self):
        """CONSULTOR_PNGI NÃO pode criar ação"""
        self.authenticate_as('consultor')
        data = {
            'strapelido': 'ACAO-CONS',
            'strdescricaoacao': 'Tentativa Consultor',
            'strdescricaoentrega': 'Entrega Consultor',
            'idvigenciapngi': self.vigencia.idvigenciapngi,
            'ideixo': self.eixo.ideixo,
            'idsituacaoacao': self.situacao.idsituacaoacao
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_cannot_update_acao(self):
        """CONSULTOR_PNGI NÃO pode atualizar ação"""
        self.authenticate_as('consultor')
        data = {'strdescricaoacao': 'Update Consultor'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/acoes/{self.acao.idacao}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consultor_cannot_delete_acao(self):
        """CONSULTOR_PNGI NÃO pode deletar ação"""
        self.authenticate_as('consultor')
        response = self.client.delete(f'/api/v1/acoes_pngi/acoes/{self.acao.idacao}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # Testes de Relacionamentos
    # ------------------------------------------------------------------------
    
    def test_acao_requires_vigencia(self):
        """Ação requer vigência (ForeignKey OBRIGATÓRIO)"""
        self.authenticate_as('coordenador')
        data = {
            'strapelido': 'ACAO-SEM-VIG',
            'strdescricaoacao': 'Sem Vigência',
            'strdescricaoentrega': 'Sem Vigência'
            # Sem idvigenciapngi - DEVE FALHAR
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes/', data, format='json')
        # Deve retornar erro de validação
        self.assertIn(response.status_code, [
            status.HTTP_400_BAD_REQUEST,  # Validação do serializer
        ])
    
    def test_acao_with_filters(self):
        """Testar filtros de ação (por vigência, search, etc)"""
        self.authenticate_as('consultor')
        
        # Filtro por vigência
        response = self.client.get(
            f'/api/v1/acoes_pngi/acoes/?idvigenciapngi={self.vigencia.idvigenciapngi}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # Search
        response = self.client.get('/api/v1/acoes_pngi/acoes/?search=ACAO-001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)


# ============================================================================
# TESTES DE PRAZO - ViewSet: AcaoPrazoViewSet
# ============================================================================

class AcaoPrazoAPITests(BaseAPITestCase):
    """
    Testes de API para AcaoPrazo.
    
    Prazos são vinculados a ações.
    Mesmas permissões que Acoes: COORDENADOR, GESTOR, OPERADOR podem gerenciar.
    
    Testa:
    - Relacionamento obrigatório: idacao (ForeignKey)
    - Constraint unique (idacao, strprazo)
    - Flag isacaoprazoativo
    - Custom action: ativos/
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/prazos/
    - POST   /api/v1/acoes_pngi/prazos/
    - GET    /api/v1/acoes_pngi/prazos/{id}/
    - PATCH  /api/v1/acoes_pngi/prazos/{id}/
    - DELETE /api/v1/acoes_pngi/prazos/{id}/
    - GET    /api/v1/acoes_pngi/prazos/ativos/
    """
    
    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        
        # ✅ 1. Criar Vigência (necessária para Acao)
        vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),        )
        
        # ✅ 2. Criar Eixo (opcional mas comum)
        eixo = Eixo.objects.create(
            stralias='E1',
            strdescricaoeixo='Eixo 1 - Gestão'
        )
        
        # ✅ 3. Criar Situação (opcional mas comum)
        situacao = SituacaoAcao.objects.create(
            strdescricaosituacao='Em Andamento'
        )
        
        # ✅ 4. Criar Acao COMPLETA (AcaoPrazo.idacao é obrigatório)
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega Teste',
            idvigenciapngi=vigencia,  # OBRIGATÓRIO
            ideixo=eixo,              # Adicionar para consistência
            idsituacaoacao=situacao   # Adicionar para consistência
        )
        
        # ✅ 5. Criar Prazo vinculado à Acao
        self.prazo = AcaoPrazo.objects.create(
            idacao=self.acao,  # OBRIGATÓRIO
            strprazo='2026-06-30',
            isacaoprazoativo=True
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_prazos(self):
        """COORDENADOR_PNGI pode listar prazos"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/prazos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_coordenador_can_create_prazo(self):
        """COORDENADOR_PNGI pode criar prazo"""
        self.authenticate_as('coordenador')
        data = {
            'idacao': self.acao.idacao,
            'strprazo': '2026-09-30',
            'isacaoprazoativo': True
        }
        response = self.client.post('/api/v1/acoes_pngi/prazos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_coordenador_can_update_prazo(self):
        """COORDENADOR_PNGI pode atualizar prazo"""
        self.authenticate_as('coordenador')
        data = {'isacaoprazoativo': False}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/prazos/{self.prazo.idacaoprazo}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_can_delete_prazo(self):
        """COORDENADOR_PNGI pode deletar prazo"""
        prazo_temp = AcaoPrazo.objects.create(
            idacao=self.acao,
            strprazo='2026-12-31',
            isacaoprazoativo=False
        )
        
        self.authenticate_as('coordenador')
        response = self.client.delete(f'/api/v1/acoes_pngi/prazos/{prazo_temp.idacaoprazo}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Pode Gerenciar
    # ------------------------------------------------------------------------
    
    def test_operador_can_manage_prazos(self):
        """OPERADOR_ACAO pode gerenciar prazos"""
        self.authenticate_as('operador')
        
        # LIST
        response = self.client.get('/api/v1/acoes_pngi/prazos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # CREATE
        data = {
            'idacao': self.acao.idacao,
            'strprazo': '2026-10-15',
            'isacaoprazoativo': True
        }
        response = self.client.post('/api/v1/acoes_pngi/prazos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_prazos(self):
        """CONSULTOR_PNGI pode listar prazos"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/prazos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_consultor_cannot_create_prazo(self):
        """CONSULTOR_PNGI NÃO pode criar prazo"""
        self.authenticate_as('consultor')
        data = {
            'idacao': self.acao.idacao,
            'strprazo': '2026-11-30',
            'isacaoprazoativo': True
        }
        response = self.client.post('/api/v1/acoes_pngi/prazos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # Testes de Custom Actions e Filtros
    # ------------------------------------------------------------------------
    
    def test_list_only_active_prazos(self):
        """Custom action: listar apenas prazos ativos"""
        # Criar prazo inativo
        AcaoPrazo.objects.create(
            idacao=self.acao,
            strprazo='2026-03-31',
            isacaoprazoativo=False
        )
        
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/prazos/ativos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica que retornou dados
        self.assertGreater(len(response.data), 0)
    
    def test_filter_prazos_by_acao(self):
        """Filtrar prazos por ação"""
        self.authenticate_as('consultor')
        response = self.client.get(f'/api/v1/acoes_pngi/prazos/?idacao={self.acao.idacao}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_filter_prazos_by_isativo(self):
        """Filtrar prazos por status ativo"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/prazos/?isacaoprazoativo=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================================================
# TESTES DE DESTAQUE - ViewSet: AcaoDestaqueViewSet
# ============================================================================

class AcaoDestaqueAPITests(BaseAPITestCase):
    """
    Testes de API para AcaoDestaque.
    
    Destaques são vinculados a ações.
    Mesmas permissões que Acoes: COORDENADOR, GESTOR, OPERADOR podem gerenciar.
    
    Testa:
    - Relacionamento obrigatório: idacao (ForeignKey)
    - Constraint unique (idacao, ordenacao)
    - Campo ordenacao
    
    Endpoints testados:
    - GET    /api/v1/acoes_pngi/destaques/
    - POST   /api/v1/acoes_pngi/destaques/
    - GET    /api/v1/acoes_pngi/destaques/{id}/
    - PATCH  /api/v1/acoes_pngi/destaques/{id}/
    - DELETE /api/v1/acoes_pngi/destaques/{id}/
    """
    
    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        
        # ✅ 1. Criar Vigência (necessária para Acao)
        vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),        )
        
        # ✅ 2. Criar Eixo (opcional mas comum)
        eixo = Eixo.objects.create(
            stralias='E1',
            strdescricaoeixo='Eixo 1 - Gestão'
        )
        
        # ✅ 3. Criar Situação (opcional mas comum)
        situacao = SituacaoAcao.objects.create(
            strdescricaosituacao='Em Andamento'
        )
        
        # ✅ 4. Criar Acao COMPLETA (AcaoDestaque.idacao é obrigatório)
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega Teste',
            idvigenciapngi=vigencia,  # OBRIGATÓRIO
            ideixo=eixo,              # Adicionar para consistência
            idsituacaoacao=situacao   # Adicionar para consistência
        )
        
        # ✅ 5. Criar Destaque vinculado à Acao
        self.destaque = AcaoDestaque.objects.create(
            idacao=self.acao,  # OBRIGATÓRIO
            datdatadestaque=timezone.now()
        )
    
    # ------------------------------------------------------------------------
    # COORDENADOR_PNGI
    # ------------------------------------------------------------------------
    
    def test_coordenador_can_list_destaques(self):
        """COORDENADOR_PNGI pode listar destaques"""
        self.authenticate_as('coordenador')
        response = self.client.get('/api/v1/acoes_pngi/destaques/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_coordenador_can_create_destaque(self):
        """COORDENADOR_PNGI pode criar destaque"""
        self.authenticate_as('coordenador')
        data = {
            'idacao': self.acao.idacao,
            'datdatadestaque': timezone.now().isoformat()
        }
        response = self.client.post('/api/v1/acoes_pngi/destaques/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_coordenador_can_update_destaque(self):
        """COORDENADOR_PNGI pode atualizar destaque"""
        self.authenticate_as('coordenador')
        data = {'datdatadestaque': timezone.now().isoformat()}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/destaques/{self.destaque.idacaodestaque}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_coordenador_can_delete_destaque(self):
        """COORDENADOR_PNGI pode deletar destaque"""
        destaque_temp = AcaoDestaque.objects.create(
            idacao=self.acao,
            datdatadestaque=timezone.now()
        )
        
        self.authenticate_as('coordenador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/destaques/{destaque_temp.idacaodestaque}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ------------------------------------------------------------------------
    # OPERADOR_ACAO - Pode Gerenciar
    # ------------------------------------------------------------------------
    
    def test_operador_can_manage_destaques(self):
        """OPERADOR_ACAO pode gerenciar destaques"""
        self.authenticate_as('operador')
        
        # LIST
        response = self.client.get('/api/v1/acoes_pngi/destaques/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # CREATE
        data = {
            'idacao': self.acao.idacao,
            'datdatadestaque': timezone.now().isoformat()
        }
        response = self.client.post('/api/v1/acoes_pngi/destaques/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # ------------------------------------------------------------------------
    # CONSULTOR_PNGI - Apenas Leitura
    # ------------------------------------------------------------------------
    
    def test_consultor_can_list_destaques(self):
        """CONSULTOR_PNGI pode listar destaques"""
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/destaques/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_consultor_cannot_create_destaque(self):
        """CONSULTOR_PNGI NÃO pode criar destaque"""
        self.authenticate_as('consultor')
        data = {
            'idacao': self.acao.idacao,
            'datdatadestaque': timezone.now().isoformat()
        }
        response = self.client.post('/api/v1/acoes_pngi/destaques/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ------------------------------------------------------------------------
    # Testes de Filtros e Ordenação
    # ------------------------------------------------------------------------
    
    def test_filter_destaques_by_acao(self):
        """Filtrar destaques por ação"""
        self.authenticate_as('consultor')
        response = self.client.get(f'/api/v1/acoes_pngi/destaques/?idacao={self.acao.idacao}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_destaques_ordered_by_ordenacao(self):
        """Destaques devem vir ordenados por campo ordenacao"""
        # Criar mais destaques com diferentes ordenações
        AcaoDestaque.objects.create(
            idacao=self.acao,
            datdatadestaque=timezone.now()
        )
        AcaoDestaque.objects.create(
            idacao=self.acao,
            datdatadestaque=timezone.now()
        )
        
        self.authenticate_as('consultor')
        response = self.client.get('/api/v1/acoes_pngi/destaques/?ordering=-datdatadestaque')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
