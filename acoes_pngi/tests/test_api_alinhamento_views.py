"""acoes_pngi/tests/test_api_alinhamento_views.py

Testes completos para API Views de Alinhamento

Testa os ViewSets:
- TipoAnotacaoAlinhamentoViewSet: CRUD de Tipos de Anotação
- AcaoAnotacaoAlinhamentoViewSet: CRUD de Anotações de Alinhamento
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, datetime
from django.utils import timezone

from accounts.models import Aplicacao, Role, UserRole
from ..models import (
    TipoAnotacaoAlinhamento,
    AcaoAnotacaoAlinhamento,
    Acoes,
    VigenciaPNGI
)

User = get_user_model()


class TipoAnotacaoAlinhamentoViewSetTest(TestCase):
    """Testes para TipoAnotacaoAlinhamentoViewSet"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup com usuário autenticado e dados de teste"""
        self.client = APIClient()
        
        # Criar aplicação e role
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        self.role, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='GESTOR_PNGI',
            defaults={'nomeperfil': 'Gestor PNGI'}
        )
        
        # Criar usuário
        self.user = User.objects.create_user(
            email='gestor@test.com',
            password='test123',
            name='Gestor Teste'
        )
        UserRole.objects.create(user=self.user, aplicacao=self.app, role=self.role)
        
        # Autenticar
        self.client.force_authenticate(user=self.user)
        
        # Criar tipos de anotação
        self.tipo1 = TipoAnotacaoAlinhamento.objects.create(
            strdescricaotipoanotacaoalinhamento='Reunião de Alinhamento'
        )
        
        self.tipo2 = TipoAnotacaoAlinhamento.objects.create(
            strdescricaotipoanotacaoalinhamento='Documento de Referência'
        )
    
    def test_list_tipos_requires_authentication(self):
        """Lista de tipos requer autenticação"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/acoes_pngi/tipos-anotacao-alinhamento/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_tipos_authenticated(self):
        """Usuário autenticado pode listar tipos"""
        response = self.client.get('/api/v1/acoes_pngi/tipos-anotacao-alinhamento/')
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)
    
    def test_retrieve_tipo(self):
        """Recuperar detalhes de um tipo específico"""
        response = self.client.get(
            f'/api/v1/acoes_pngi/tipos-anotacao-alinhamento/{self.tipo1.idtipoanotacaoalinhamento}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['strdescricaotipoanotacaoalinhamento'],
            'Reunião de Alinhamento'
        )
    
    def test_create_tipo(self):
        """Criar novo tipo de anotação"""
        data = {
            'strdescricaotipoanotacaoalinhamento': 'Apresentação Técnica'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/tipos-anotacao-alinhamento/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            TipoAnotacaoAlinhamento.objects.filter(
                strdescricaotipoanotacaoalinhamento='Apresentação Técnica'
            ).exists()
        )
    
    def test_update_tipo(self):
        """Atualizar tipo existente"""
        data = {
            'strdescricaotipoanotacaoalinhamento': 'Reunião de Alinhamento Estratégico'
        }
        response = self.client.put(
            f'/api/v1/acoes_pngi/tipos-anotacao-alinhamento/{self.tipo1.idtipoanotacaoalinhamento}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tipo1.refresh_from_db()
        self.assertEqual(
            self.tipo1.strdescricaotipoanotacaoalinhamento,
            'Reunião de Alinhamento Estratégico'
        )
    
    def test_partial_update_tipo(self):
        """Atualização parcial de tipo"""
        data = {'strdescricaotipoanotacaoalinhamento': 'Reunião Atualizada'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/tipos-anotacao-alinhamento/{self.tipo1.idtipoanotacaoalinhamento}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tipo1.refresh_from_db()
        self.assertEqual(
            self.tipo1.strdescricaotipoanotacaoalinhamento,
            'Reunião Atualizada'
        )
    
    def test_delete_tipo(self):
        """Deletar tipo"""
        tipo_id = self.tipo2.idtipoanotacaoalinhamento
        response = self.client.delete(
            f'/api/v1/acoes_pngi/tipos-anotacao-alinhamento/{tipo_id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            TipoAnotacaoAlinhamento.objects.filter(idtipoanotacaoalinhamento=tipo_id).exists()
        )
    
    def test_search_tipos(self):
        """Buscar tipos por descrição"""
        response = self.client.get(
            '/api/v1/acoes_pngi/tipos-anotacao-alinhamento/?search=Reunião'
        )
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]['strdescricaotipoanotacaoalinhamento'],
            'Reunião de Alinhamento'
        )
    
    def test_ordering_tipos(self):
        """Ordenar tipos"""
        response = self.client.get(
            '/api/v1/acoes_pngi/tipos-anotacao-alinhamento/?ordering=-strdescricaotipoanotacaoalinhamento'
        )
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve vir em ordem decrescente (Reunião antes de Documento)
        self.assertEqual(
            results[0]['strdescricaotipoanotacaoalinhamento'],
            'Reunião de Alinhamento'
        )


class AcaoAnotacaoAlinhamentoViewSetTest(TestCase):
    """Testes para AcaoAnotacaoAlinhamentoViewSet"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup com usuário autenticado e dados de teste"""
        self.client = APIClient()
        
        # Criar aplicação e role
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        self.role, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='GESTOR_PNGI',
            defaults={'nomeperfil': 'Gestor PNGI'}
        )
        
        # Criar usuário
        self.user = User.objects.create_user(
            email='gestor@test.com',
            password='test123',
            name='Gestor Teste'
        )
        UserRole.objects.create(user=self.user, aplicacao=self.app, role=self.role)
        
        # Autenticar
        self.client.force_authenticate(user=self.user)
        
        # Criar vigência e ações
        self.vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),
            datfinalvigencia=date(2026, 12, 31)
        )
        
        self.acao1 = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste 1',
            strdescricaoentrega='Entrega 1',
            idvigenciapngi=self.vigencia
        )
        
        self.acao2 = Acoes.objects.create(
            strapelido='ACAO-002',
            strdescricaoacao='Ação Teste 2',
            strdescricaoentrega='Entrega 2',
            idvigenciapngi=self.vigencia
        )
        
        # Criar tipos de anotação
        self.tipo1 = TipoAnotacaoAlinhamento.objects.create(
            strdescricaotipoanotacaoalinhamento='Reunião'
        )
        
        self.tipo2 = TipoAnotacaoAlinhamento.objects.create(
            strdescricaotipoanotacaoalinhamento='Documento'
        )
        
        # Criar anotações
        self.anotacao1 = AcaoAnotacaoAlinhamento.objects.create(
            idacao=self.acao1,
            idtipoanotacaoalinhamento=self.tipo1,
            datdataanotacaoalinhamento=datetime(2026, 2, 15, 10, 0),
            strdescricaoanotacaoalinhamento='Anotação da reunião de alinhamento',
            strlinkanotacaoalinhamento='https://example.com/reuniao',
            strnumeromonitoramento='MON-001'
        )
        
        self.anotacao2 = AcaoAnotacaoAlinhamento.objects.create(
            idacao=self.acao1,
            idtipoanotacaoalinhamento=self.tipo2,
            datdataanotacaoalinhamento=datetime(2026, 1, 10, 14, 30),
            strdescricaoanotacaoalinhamento='Documento de referência'
        )
    
    def test_list_anotacoes_requires_authentication(self):
        """Lista de anotações requer autenticação"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/acoes_pngi/anotacoes-alinhamento/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_anotacoes_authenticated(self):
        """Usuário autenticado pode listar anotações"""
        response = self.client.get('/api/v1/acoes_pngi/anotacoes-alinhamento/')
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)
    
    def test_retrieve_anotacao(self):
        """Recuperar detalhes de uma anotação específica"""
        response = self.client.get(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/{self.anotacao1.idacaoanotacaoalinhamento}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['strdescricaoanotacaoalinhamento'],
            'Anotação da reunião de alinhamento'
        )
    
    def test_create_anotacao(self):
        """Criar nova anotação de alinhamento"""
        data = {
            'idacao': self.acao2.idacao,
            'idtipoanotacaoalinhamento': self.tipo1.idtipoanotacaoalinhamento,
            'datdataanotacaoalinhamento': '2026-03-01T15:00:00Z',
            'strdescricaoanotacaoalinhamento': 'Nova anotação',
            'strlinkanotacaoalinhamento': 'https://example.com/nova',
            'strnumeromonitoramento': 'MON-002'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/anotacoes-alinhamento/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            AcaoAnotacaoAlinhamento.objects.filter(
                strdescricaoanotacaoalinhamento='Nova anotação'
            ).exists()
        )
    
    def test_create_anotacao_without_optional_fields(self):
        """Criar anotação sem campos opcionais"""
        data = {
            'idacao': self.acao2.idacao,
            'idtipoanotacaoalinhamento': self.tipo2.idtipoanotacaoalinhamento,
            'datdataanotacaoalinhamento': '2026-03-05T10:00:00Z',
            'strdescricaoanotacaoalinhamento': 'Anotação mínima'
        }
        response = self.client.post(
            '/api/v1/acoes_pngi/anotacoes-alinhamento/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_anotacao(self):
        """Atualizar anotação existente"""
        data = {
            'idacao': self.acao1.idacao,
            'idtipoanotacaoalinhamento': self.tipo1.idtipoanotacaoalinhamento,
            'datdataanotacaoalinhamento': '2026-02-15T10:00:00Z',
            'strdescricaoanotacaoalinhamento': 'Anotação atualizada',
            'strlinkanotacaoalinhamento': 'https://example.com/atualizado',
            'strnumeromonitoramento': 'MON-001-UPD'
        }
        response = self.client.put(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/{self.anotacao1.idacaoanotacaoalinhamento}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.anotacao1.refresh_from_db()
        self.assertEqual(
            self.anotacao1.strdescricaoanotacaoalinhamento,
            'Anotação atualizada'
        )
    
    def test_partial_update_anotacao(self):
        """Atualização parcial de anotação"""
        data = {
            'strdescricaoanotacaoalinhamento': 'Descrição parcialmente atualizada'
        }
        response = self.client.patch(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/{self.anotacao1.idacaoanotacaoalinhamento}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.anotacao1.refresh_from_db()
        self.assertEqual(
            self.anotacao1.strdescricaoanotacaoalinhamento,
            'Descrição parcialmente atualizada'
        )
        # Outros campos não devem mudar
        self.assertEqual(self.anotacao1.strnumeromonitoramento, 'MON-001')
    
    def test_delete_anotacao(self):
        """Deletar anotação"""
        anotacao_id = self.anotacao2.idacaoanotacaoalinhamento
        response = self.client.delete(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/{anotacao_id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            AcaoAnotacaoAlinhamento.objects.filter(
                idacaoanotacaoalinhamento=anotacao_id
            ).exists()
        )
    
    def test_filter_anotacoes_by_acao(self):
        """Filtrar anotações por ação"""
        response = self.client.get(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/?idacao={self.acao1.idacao}'
        )
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)  # Ambas são da acao1
    
    def test_filter_anotacoes_by_tipo(self):
        """Filtrar anotações por tipo"""
        response = self.client.get(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/?idtipoanotacaoalinhamento={self.tipo1.idtipoanotacaoalinhamento}'
        )
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)  # Apenas anotacao1
    
    def test_filter_anotacoes_by_acao_and_tipo(self):
        """Filtrar anotações por ação E tipo"""
        response = self.client.get(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/?idacao={self.acao1.idacao}&idtipoanotacaoalinhamento={self.tipo2.idtipoanotacaoalinhamento}'
        )
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)  # Apenas anotacao2
    
    def test_search_anotacoes_by_apelido(self):
        """Buscar anotações por apelido da ação"""
        response = self.client.get(
            '/api/v1/acoes_pngi/anotacoes-alinhamento/?search=ACAO-001'
        )
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)
    
    def test_search_anotacoes_by_descricao(self):
        """Buscar anotações por descrição"""
        response = self.client.get(
            '/api/v1/acoes_pngi/anotacoes-alinhamento/?search=reunião'
        )
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]['strdescricaoanotacaoalinhamento'],
            'Anotação da reunião de alinhamento'
        )
    
    def test_search_anotacoes_by_numero_monitoramento(self):
        """Buscar anotações por número de monitoramento"""
        response = self.client.get(
            '/api/v1/acoes_pngi/anotacoes-alinhamento/?search=MON-001'
        )
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)
    
    def test_ordering_anotacoes(self):
        """Ordenar anotações por data (mais recente primeiro)"""
        response = self.client.get('/api/v1/acoes_pngi/anotacoes-alinhamento/')
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Primeiro resultado deve ser o mais recente (fevereiro)
        first_date = datetime.fromisoformat(
            results[0]['datdataanotacaoalinhamento'].replace('Z', '+00:00')
        )
        self.assertEqual(first_date.month, 2)
    
    def test_ordering_anotacoes_ascending(self):
        """Ordenar anotações por data (mais antiga primeiro)"""
        response = self.client.get(
            '/api/v1/acoes_pngi/anotacoes-alinhamento/?ordering=datdataanotacaoalinhamento'
        )
        results = getattr(response.data, 'results', [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Primeiro resultado deve ser o mais antigo (janeiro)
        first_date = datetime.fromisoformat(
            results[0]['datdataanotacaoalinhamento'].replace('Z', '+00:00')
        )
        self.assertEqual(first_date.month, 1)
    
    def test_anotacao_with_all_relationships(self):
        """Anotação com todos os relacionamentos preenchidos"""
        response = self.client.get(
            f'/api/v1/acoes_pngi/anotacoes-alinhamento/{self.anotacao1.idacaoanotacaoalinhamento}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica relacionamentos
        self.assertEqual(response.data['idacao'], self.acao1.idacao)
        self.assertEqual(
            response.data['idtipoanotacaoalinhamento'],
            self.tipo1.idtipoanotacaoalinhamento
        )
