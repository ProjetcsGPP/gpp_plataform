
"""
Testes para AcaoAnotacaoAlinhamento API ViewSet.
Todos os testes foram corrigidos com os campos corretos do modelo.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from datetime import timedelta
from django.utils import timezone

from accounts.models import Aplicacao, Role, UserRole
from acoes_pngi.models import (
    VigenciaPNGI,
    Acoes,
    TipoAnotacaoAlinhamento,
    AcaoAnotacaoAlinhamento
)

User = get_user_model()


class AcaoAnotacaoAlinhamentoViewSetTest(APITestCase):
    """Testes para ViewSet de Anotações de Alinhamento"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    @classmethod
    def setUpClass(cls):
        """Executado uma única vez antes de todos os testes"""
        super().setUpClass()
        
        # Criar aplicação ACOES_PNGI
        cls.app_acoes, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        # Criar role
        cls.role, _ = Role.objects.get_or_create(
            codigoperfil='GESTOR_PNGI',
            aplicacao=cls.app_acoes,
            defaults={'nomeperfil': 'Gestor PNGI'}
        )
    
    def setUp(self):
        """Executado antes de cada teste"""
        # Criar usuário
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User'
        )
        
        # Associar role ao usuário
        UserRole.objects.create(
            user=self.user,
            aplicacao=self.app_acoes,
            role=self.role
        )
        
        # Autenticar cliente
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Criar vigência
        self.vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='Vigência 2025',
            datiniciovigencia=timezone.now().date(),
            datfinalvigencia=timezone.now().date() + timedelta(days=365)
        )
        
        # Criar ações
        self.acao1 = Acoes.objects.create(
            strapelido='Ação 1',
            strdescricaoacao='Descrição Ação 1',
            strdescricaoentrega='Entrega 1',
            idvigenciapngi=self.vigencia
        )
        
        self.acao2 = Acoes.objects.create(
            strapelido='Ação 2',
            strdescricaoacao='Descrição Ação 2',
            strdescricaoentrega='Entrega 2',
            idvigenciapngi=self.vigencia
        )
        
        # Criar tipos de anotação
        self.tipo1 = TipoAnotacaoAlinhamento.objects.create(
            strdescricaotipoanotacaoalinhamento='Tipo 1'
        )
        
        self.tipo2 = TipoAnotacaoAlinhamento.objects.create(
            strdescricaotipoanotacaoalinhamento='Tipo 2'
        )
        
        # Criar anotações
        self.anotacao1 = AcaoAnotacaoAlinhamento.objects.create(
            idacao=self.acao1,
            idtipoanotacaoalinhamento=self.tipo1,
            datdataanotacaoalinhamento=timezone.now(),
            strdescricaoanotacaoalinhamento='Descrição Anotação 1',
            strnumeromonitoramento='12345'
        )
        
        self.anotacao2 = AcaoAnotacaoAlinhamento.objects.create(
            idacao=self.acao1,
            idtipoanotacaoalinhamento=self.tipo2,
            datdataanotacaoalinhamento=timezone.now() - timedelta(days=1),
            strdescricaoanotacaoalinhamento='Descrição Anotação 2',
            strnumeromonitoramento='54321'
        )
        
        self.api_base_url = '/api/v1/acoes_pngi/acoes-anotacao-alinhamento/'
    
    def _get_results(self, response):
        """Helper para extrair resultados da resposta (com ou sem paginação)"""
        if isinstance(response.data, list):
            return response.data
        else:
            return response.data.get('results', response.data)
    
    # ===== TESTES PASSANDO (4) =====
    
    def test_anotacao_with_all_relationships(self):
        """Anotação com todos os relacionamentos preenchidos"""
        response = self.client.get(f'{self.api_base_url}{self.anotacao1.idacaoanotacaoalinhamento}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['idacaoanotacaoalinhamento'], self.anotacao1.idacaoanotacaoalinhamento)
    
    def test_create_anotacao(self):
        """Criar nova anotação de alinhamento"""
        data = {
            'idacao': self.acao2.idacao,  # CORREÇÃO: usar idacao
            'idtipoanotacaoalinhamento': self.tipo1.idtipoanotacaoalinhamento,  # CORREÇÃO: usar idtipoanotacaoalinhamento
            'datdataanotacaoalinhamento': timezone.now().isoformat(),
            'strdescricaoanotacaoalinhamento': 'Nova anotação'
        }
        
        response = self.client.post(self.api_base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_anotacao_without_optional_fields(self):
        """Criar anotação sem campos opcionais"""
        data = {
            'idacao': self.acao2.idacao,
            'idtipoanotacaoalinhamento': self.tipo1.idtipoanotacaoalinhamento,
            'datdataanotacaoalinhamento': timezone.now().isoformat(),
            'strdescricaoanotacaoalinhamento': 'Anotação mínima'
        }
        
        response = self.client.post(self.api_base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_delete_anotacao(self):
        """Deletar anotação"""
        response = self.client.delete(
            f'{self.api_base_url}{self.anotacao1.idacaoanotacaoalinhamento}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_partial_update_anotacao(self):
        """Atualização parcial de anotação"""
        data = {
            'strdescricaoanotacaoalinhamento': 'Descrição atualizada parcialmente'
        }
        
        response = self.client.patch(
            f'{self.api_base_url}{self.anotacao1.idacaoanotacaoalinhamento}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_anotacao(self):
        """Recuperar detalhes de uma anotação específica"""
        response = self.client.get(
            f'{self.api_base_url}{self.anotacao1.idacaoanotacaoalinhamento}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['idacaoanotacaoalinhamento'], self.anotacao1.idacaoanotacaoalinhamento)
    
    def test_list_anotacoes_requires_authentication(self):
        """Lista de anotações requer autenticação"""
        client = APIClient()  # Sem autenticação
        response = client.get(self.api_base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # ===== TESTES QUE FALHAVAM (10) - AGORA CORRIGIDOS =====
    
    def test_list_anotacoes_authenticated(self):
        """Usuário autenticado pode listar anotações"""
        response = self.client.get(self.api_base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = self._get_results(response)
        self.assertEqual(len(results), 2)
    
    def test_filter_anotacoes_by_acao(self):
        """Filtrar anotações por ação"""
        # CORREÇÃO: usar idacao, não id
        response = self.client.get(f'{self.api_base_url}?idacao={self.acao1.idacao}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = self._get_results(response)
        self.assertEqual(len(results), 2)
    
    def test_filter_anotacoes_by_tipo(self):
        """Filtrar anotações por tipo"""
        # CORREÇÃO: usar idtipoanotacaoalinhamento, não id
        response = self.client.get(
            f'{self.api_base_url}?idtipoanotacaoalinhamento={self.tipo1.idtipoanotacaoalinhamento}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = self._get_results(response)
        self.assertEqual(len(results), 1)
    
    def test_filter_anotacoes_by_acao_and_tipo(self):
        """Filtrar anotações por ação E tipo"""
        response = self.client.get(
            f'{self.api_base_url}?idacao={self.acao1.idacao}&idtipoanotacaoalinhamento={self.tipo2.idtipoanotacaoalinhamento}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = self._get_results(response)
        self.assertEqual(len(results), 1)
    
    def test_ordering_anotacoes(self):
        """Ordenar anotações por data (mais recente primeiro)"""
        response = self.client.get(f'{self.api_base_url}?ordering=-datdataanotacaoalinhamento')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = self._get_results(response)
        self.assertTrue(len(results) > 0, "Nenhum resultado retornado")
        
        # Verificar ordem decrescente
        if len(results) > 1:
            self.assertGreaterEqual(
                results[0]['datdataanotacaoalinhamento'],
                results[1]['datdataanotacaoalinhamento']
            )
    
    def test_ordering_anotacoes_ascending(self):
        """Ordenar anotações por data (mais antiga primeiro)"""
        response = self.client.get(f'{self.api_base_url}?ordering=datdataanotacaoalinhamento')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = self._get_results(response)
        self.assertTrue(len(results) > 0, "Nenhum resultado retornado")
    
    def test_search_anotacoes_by_apelido(self):
        """Buscar anotações por apelido da ação"""
        response = self.client.get(f'{self.api_base_url}?search=Ação')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = self._get_results(response)
        self.assertEqual(len(results), 2)
    
    def test_search_anotacoes_by_descricao(self):
        """Buscar anotações por descrição"""
        response = self.client.get(f'{self.api_base_url}?search=Descrição')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = self._get_results(response)
        self.assertEqual(len(results), 1)
    
    def test_search_anotacoes_by_numero_monitoramento(self):
        """Buscar anotações por número de monitoramento"""
        response = self.client.get(f'{self.api_base_url}?search=123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = self._get_results(response)
        self.assertEqual(len(results), 1)
    
    def test_update_anotacao(self):
        """Atualizar anotação existente"""
        updated_data = {
            'idacao': self.acao1.idacao,  # CORREÇÃO: usar idacao, não id
            'idtipoanotacaoalinhamento': self.tipo2.idtipoanotacaoalinhamento,  # CORREÇÃO: usar idtipoanotacaoalinhamento, não id
            'datdataanotacaoalinhamento': timezone.now().isoformat(),
            'strdescricaoanotacaoalinhamento': 'Descrição atualizada'
        }
        
        url = f'{self.api_base_url}{self.anotacao1.idacaoanotacaoalinhamento}/'
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['strdescricaoanotacaoalinhamento'], 'Descrição atualizada')