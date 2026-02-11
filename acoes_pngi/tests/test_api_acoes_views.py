"""acoes_pngi/tests/test_api_acoes_views.py

Testes completos para API Views de Ações

Testa os ViewSets:
- AcoesViewSet: CRUD de Ações, filtros, busca, ações customizadas
- AcaoPrazoViewSet: CRUD de Prazos, filtros
- AcaoDestaqueViewSet: CRUD de Destaques
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, datetime, timedelta

from accounts.models import Aplicacao, Role, UserRole
from ..models import (
    Acoes, AcaoPrazo, AcaoDestaque,
    VigenciaPNGI, TipoEntraveAlerta,
    UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel
)

User = get_user_model()


class AcoesViewSetTest(TestCase):
    """Testes para AcoesViewSet"""
    
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
        
        # Criar vigência
        self.vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),
            datfinalvigencia=date(2026, 12, 31),
            isvigenciaativa=True
        )
        
        # Criar tipo de entrave
        self.tipo_entrave = TipoEntraveAlerta.objects.create(
            strdescricaotipoentravealerta='Crítico'
        )
        
        # Criar ações
        self.acao1 = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Descrição da Ação 001',
            strdescricaoentrega='Entrega 001',
            idvigenciapngi=self.vigencia,
            idtipoentravealerta=self.tipo_entrave,
            datdataentrega=datetime(2026, 6, 30)
        )
        
        self.acao2 = Acoes.objects.create(
            strapelido='ACAO-002',
            strdescricaoacao='Descrição da Ação 002',
            strdescricaoentrega='Entrega 002',
            idvigenciapngi=self.vigencia
        )
    
    def test_list_acoes_requires_authentication(self):
        """Lista de ações requer autenticação"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/acoes_pngi/acoes/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_acoes_authenticated(self):
        """Usuário autenticado pode listar ações"""
        response = self.client.get('/api/v1/acoes_pngi/acoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_acao(self):
        """Recuperar detalhes de uma ação específica"""
        response = self.client.get(f'/api/v1/acoes_pngi/acoes/{self.acao1.idacao}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['strapelido'], 'ACAO-001')
    
    def test_create_acao(self):
        """Criar nova ação"""
        data = {
            'strapelido': 'ACAO-003',
            'strdescricaoacao': 'Nova Ação',
            'strdescricaoentrega': 'Nova Entrega',
            'idvigenciapngi': self.vigencia.idvigenciapngi
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Acoes.objects.filter(strapelido='ACAO-003').exists())
    
    def test_update_acao(self):
        """Atualizar ação existente"""
        data = {
            'strapelido': 'ACAO-001-UPD',
            'strdescricaoacao': 'Descrição Atualizada',
            'strdescricaoentrega': 'Entrega Atualizada',
            'idvigenciapngi': self.vigencia.idvigenciapngi
        }
        response = self.client.put(
            f'/api/v1/acoes_pngi/acoes/{self.acao1.idacao}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.acao1.refresh_from_db()
        self.assertEqual(self.acao1.strapelido, 'ACAO-001-UPD')
    
    def test_partial_update_acao(self):
        """Atualização parcial de ação"""
        data = {'strdescricaoacao': 'Descrição Parcialmente Atualizada'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/acoes/{self.acao1.idacao}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.acao1.refresh_from_db()
        self.assertEqual(self.acao1.strdescricaoacao, 'Descrição Parcialmente Atualizada')
        # Outros campos não devem mudar
        self.assertEqual(self.acao1.strapelido, 'ACAO-001')
    
    def test_delete_acao(self):
        """Deletar ação"""
        acao_id = self.acao2.idacao
        response = self.client.delete(f'/api/v1/acoes_pngi/acoes/{acao_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Acoes.objects.filter(idacao=acao_id).exists())
    
    def test_filter_acoes_by_vigencia(self):
        """Filtrar ações por vigência"""
        # Criar outra vigência e ação
        vigencia2 = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2027',
            datiniciovigencia=date(2027, 1, 1),
            datfinalvigencia=date(2027, 12, 31)
        )
        Acoes.objects.create(
            strapelido='ACAO-003',
            strdescricaoacao='Ação 2027',
            strdescricaoentrega='Entrega 2027',
            idvigenciapngi=vigencia2
        )
        
        response = self.client.get(
            f'/api/v1/acoes_pngi/acoes/?idvigenciapngi={self.vigencia.idvigenciapngi}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Apenas ações de 2026
    
    def test_filter_acoes_by_tipo_entrave(self):
        """Filtrar ações por tipo de entrave"""
        response = self.client.get(
            f'/api/v1/acoes_pngi/acoes/?idtipoentravealerta={self.tipo_entrave.idtipoentravealerta}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Apenas acao1 tem entrave
    
    def test_search_acoes(self):
        """Buscar ações por apelido/descrição"""
        response = self.client.get('/api/v1/acoes_pngi/acoes/?search=001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['strapelido'], 'ACAO-001')
    
    def test_ordering_acoes(self):
        """Ordenar ações"""
        response = self.client.get('/api/v1/acoes_pngi/acoes/?ordering=-strapelido')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve vir em ordem decrescente (002, 001)
        self.assertEqual(response.data['results'][0]['strapelido'], 'ACAO-002')
    
    def test_prazos_ativos_action(self):
        """Action customizada: prazos_ativos"""
        # Criar prazos para a ação
        AcaoPrazo.objects.create(
            idacao=self.acao1,
            strprazo='Prazo Ativo',
            isacaoprazoativo=True
        )
        AcaoPrazo.objects.create(
            idacao=self.acao1,
            strprazo='Prazo Inativo',
            isacaoprazoativo=False
        )
        
        response = self.client.get(f'/api/v1/acoes_pngi/acoes/{self.acao1.idacao}/prazos_ativos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Apenas ativo
        self.assertEqual(response.data[0]['strprazo'], 'Prazo Ativo')
    
    def test_responsaveis_list_action(self):
        """Action customizada: responsaveis_list"""
        # Criar responsável
        user2 = User.objects.create_user(
            email='responsavel@test.com',
            password='test123',
            name='Responsável Teste'
        )
        responsavel = UsuarioResponsavel.objects.create(
            idusuario=user2,
            strtelefone='27999999999',
            strorgao='SEGER'
        )
        RelacaoAcaoUsuarioResponsavel.objects.create(
            idacao=self.acao1,
            idusuarioresponsavel=responsavel
        )
        
        response = self.client.get(f'/api/v1/acoes_pngi/acoes/{self.acao1.idacao}/responsaveis_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class AcaoPrazoViewSetTest(TestCase):
    """Testes para AcaoPrazoViewSet"""
    
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
            password='test123'
        )
        UserRole.objects.create(user=self.user, aplicacao=self.app, role=self.role)
        
        # Autenticar
        self.client.force_authenticate(user=self.user)
        
        # Criar vigência e ação
        self.vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),
            datfinalvigencia=date(2026, 12, 31)
        )
        
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega',
            idvigenciapngi=self.vigencia
        )
        
        # Criar prazos
        self.prazo1 = AcaoPrazo.objects.create(
            idacao=self.acao,
            strprazo='Q1 2026',
            isacaoprazoativo=True
        )
        
        self.prazo2 = AcaoPrazo.objects.create(
            idacao=self.acao,
            strprazo='Q4 2025',
            isacaoprazoativo=False
        )
    
    def test_list_prazos_requires_authentication(self):
        """Lista de prazos requer autenticação"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/acoes_pngi/acoes-prazo/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_prazos_authenticated(self):
        """Usuário autenticado pode listar prazos"""
        response = self.client.get('/api/v1/acoes_pngi/acoes-prazo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_prazo(self):
        """Recuperar detalhes de um prazo específico"""
        response = self.client.get(f'/api/v1/acoes_pngi/acoes-prazo/{self.prazo1.idacaoprazo}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['strprazo'], 'Q1 2026')
    
    def test_create_prazo(self):
        """Criar novo prazo"""
        # Primeiro desativar o prazo ativo existente
        self.prazo1.isacaoprazoativo = False
        self.prazo1.save()
        
        data = {
            'idacao': self.acao.idacao,
            'strprazo': 'Q2 2026',
            'isacaoprazoativo': True
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes-prazo/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AcaoPrazo.objects.filter(strprazo='Q2 2026').exists())
    
    def test_update_prazo(self):
        """Atualizar prazo existente"""
        data = {
            'idacao': self.acao.idacao,
            'strprazo': 'Q1 2026 - Atualizado',
            'isacaoprazoativo': True
        }
        response = self.client.put(
            f'/api/v1/acoes_pngi/acoes-prazo/{self.prazo1.idacaoprazo}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.prazo1.refresh_from_db()
        self.assertEqual(self.prazo1.strprazo, 'Q1 2026 - Atualizado')
    
    def test_delete_prazo(self):
        """Deletar prazo"""
        prazo_id = self.prazo2.idacaoprazo
        response = self.client.delete(f'/api/v1/acoes_pngi/acoes-prazo/{prazo_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AcaoPrazo.objects.filter(idacaoprazo=prazo_id).exists())
    
    def test_filter_prazos_by_acao(self):
        """Filtrar prazos por ação"""
        response = self.client.get(f'/api/v1/acoes_pngi/acoes-prazo/?idacao={self.acao.idacao}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_prazos_by_status(self):
        """Filtrar prazos por status ativo/inativo"""
        response = self.client.get('/api/v1/acoes_pngi/acoes-prazo/?isacaoprazoativo=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['strprazo'], 'Q1 2026')
    
    def test_ativos_action(self):
        """Action customizada: ativos (apenas prazos ativos)"""
        response = self.client.get('/api/v1/acoes_pngi/acoes-prazo/ativos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['strprazo'], 'Q1 2026')


class AcaoDestaqueViewSetTest(TestCase):
    """Testes para AcaoDestaqueViewSet"""
    
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
            password='test123'
        )
        UserRole.objects.create(user=self.user, aplicacao=self.app, role=self.role)
        
        # Autenticar
        self.client.force_authenticate(user=self.user)
        
        # Criar vigência e ação
        self.vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),
            datfinalvigencia=date(2026, 12, 31)
        )
        
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega',
            idvigenciapngi=self.vigencia
        )
        
        # Criar destaques
        self.destaque1 = AcaoDestaque.objects.create(
            idacao=self.acao,
            datdatadestaque=datetime(2026, 2, 15, 10, 0)
        )
        
        self.destaque2 = AcaoDestaque.objects.create(
            idacao=self.acao,
            datdatadestaque=datetime(2026, 1, 10, 14, 30)
        )
    
    def test_list_destaques_requires_authentication(self):
        """Lista de destaques requer autenticação"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/acoes_pngi/acoes-destaque/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_destaques_authenticated(self):
        """Usuário autenticado pode listar destaques"""
        response = self.client.get('/api/v1/acoes_pngi/acoes-destaque/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_destaque(self):
        """Recuperar detalhes de um destaque específico"""
        response = self.client.get(
            f'/api/v1/acoes_pngi/acoes-destaque/{self.destaque1.idacaodestaque}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_destaque(self):
        """Criar novo destaque"""
        data = {
            'idacao': self.acao.idacao,
            'datdatadestaque': '2026-03-20T15:00:00Z'
        }
        response = self.client.post('/api/v1/acoes_pngi/acoes-destaque/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AcaoDestaque.objects.filter(idacao=self.acao).count(), 3)
    
    def test_update_destaque(self):
        """Atualizar destaque existente"""
        data = {
            'idacao': self.acao.idacao,
            'datdatadestaque': '2026-02-20T12:00:00Z'
        }
        response = self.client.put(
            f'/api/v1/acoes_pngi/acoes-destaque/{self.destaque1.idacaodestaque}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_destaque(self):
        """Deletar destaque"""
        destaque_id = self.destaque2.idacaodestaque
        response = self.client.delete(f'/api/v1/acoes_pngi/acoes-destaque/{destaque_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AcaoDestaque.objects.filter(idacaodestaque=destaque_id).exists())
    
    def test_filter_destaques_by_acao(self):
        """Filtrar destaques por ação"""
        response = self.client.get(
            f'/api/v1/acoes_pngi/acoes-destaque/?idacao={self.acao.idacao}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_ordering_destaques(self):
        """Destaques ordenados por data (mais recente primeiro)"""
        response = self.client.get('/api/v1/acoes_pngi/acoes-destaque/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Primeiro resultado deve ser o mais recente (fevereiro)
        first_date = datetime.fromisoformat(
            response.data['results'][0]['datdatadestaque'].replace('Z', '+00:00')
        )
        self.assertEqual(first_date.month, 2)
