"""
Testes para LotacaoJsonOrgaoViewSet
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
import uuid

from ..models import (
    TblPatriarca, TblOrganogramaVersao, TblLotacaoVersao,
    TblOrgaoUnidade, TblLotacaoJsonOrgao, TblLotacao, TblStatusProgresso,
)

User = get_user_model()


class LotacaoJsonOrgaoViewSetTest(TestCase):
    """Testes para ViewSet de JSON de Lotação por Órgão"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Configuração inicial"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Dados de teste
        self.status_progresso = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=1,
            defaults={'str_descricao': 'Em Progresso'}
        )[0]
        
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='SEGER',
            str_nome='Secretaria de Estado de Gestão',
            id_status_progresso=self.status_progresso,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        self.organograma = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca,
            str_origem='TESTE',
            dat_processamento=timezone.now(),
            str_status_processamento='PROCESSADO',
            flg_ativo=True
        )
        
        self.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=self.patriarca,
            id_organograma_versao=self.organograma,
            str_origem='TESTE',
            dat_processamento=timezone.now(),
            str_status_processamento='PROCESSADO',
            flg_ativo=True
        )
        
        self.orgao = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma,
            id_patriarca=self.patriarca,
            str_nome='Subsecretaria de Gestão',
            str_sigla='SUBGES',
            int_nivel_hierarquia=1,
            flg_ativo=True,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        self.lotacao = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.organograma,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao,
            str_cpf='123.456.789-00',
            str_cargo_original='Analista',
            flg_valido=True,
            dat_criacao=timezone.now()
        )
        
        self.lotacao_json = TblLotacaoJsonOrgao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.organograma,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao,
            js_conteudo={'orgao': {'sigla': 'SUBGES'}, 'servidores': [{'cpf': '123.456.789-00'}]},
            dat_criacao=timezone.now()
        )
    
    def test_list(self):
        """Testa listagem"""
        response = self.client.get('/api/v1/carga/lotacao-json/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve(self):
        """Testa recuperação"""
        url = f'/api/v1/carga/lotacao-json/{self.lotacao_json.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_conteudo_action(self):
        """Testa action conteudo"""
        url = f'/api/v1/carga/lotacao-json/{self.lotacao_json.pk}/conteudo/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('conteudo', response.data)
    
    def test_regenerar_action(self):
        """Testa action regenerar"""
        url = f'/api/v1/carga/lotacao-json/{self.lotacao_json.pk}/regenerar/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_estatisticas_action(self):
        """Testa action estatisticas"""
        response = self.client.get('/api/v1/carga/lotacao-json/estatisticas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
