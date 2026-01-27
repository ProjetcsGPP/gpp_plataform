"""
Testes para Serializers
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

from ..models import (
    TblPatriarca, TblStatusProgresso, TblLotacaoJsonOrgao,
    TblOrganogramaVersao, TblLotacaoVersao, TblOrgaoUnidade,
)
from ..serializers import (
    TblPatriarcaSerializer,
    TblLotacaoJsonOrgaoSerializer,
    TblStatusProgressoSerializer,
)

User = get_user_model()


class SerializersTest(TestCase):
    """Testes para Serializers"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser_serial',
            password='testpass123'
        )
        
        self.status_progresso = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=1,
            defaults={'str_descricao': 'Em Progresso'}
        )[0]
    
    def test_status_progresso_serializer(self):
        """Testa StatusProgressoSerializer"""
        serializer = TblStatusProgressoSerializer(self.status_progresso)
        data = serializer.data
        
        self.assertEqual(data['id_status_progresso'], 1)
        self.assertEqual(data['str_descricao'], 'Em Progresso')
    
    def test_patriarca_serializer(self):
        """Testa PatriarcaSerializer"""
        patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='TEST',
            str_nome='Teste',
            id_status_progresso=self.status_progresso,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        serializer = TblPatriarcaSerializer(patriarca)
        data = serializer.data
        
        self.assertEqual(data['str_sigla_patriarca'], 'TEST')
        self.assertIn('status_progresso', data)
    
    def test_lotacao_json_serializer_total_servidores(self):
        """Testa campo calculado total_servidores"""
        patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='TEST',
            str_nome='Teste',
            id_status_progresso=self.status_progresso,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        organograma = TblOrganogramaVersao.objects.create(
            id_patriarca=patriarca,
            str_origem='TESTE',
            dat_processamento=timezone.now(),
            str_status_processamento='PROCESSADO',
            flg_ativo=True
        )
        
        lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=patriarca,
            id_organograma_versao=organograma,
            str_origem='TESTE',
            dat_processamento=timezone.now(),
            str_status_processamento='PROCESSADO',
            flg_ativo=True
        )
        
        orgao = TblOrgaoUnidade.objects.create(
            id_organograma_versao=organograma,
            id_patriarca=patriarca,
            str_nome='Teste',
            str_sigla='TST',
            int_nivel_hierarquia=1,
            flg_ativo=True,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        lotacao_json = TblLotacaoJsonOrgao.objects.create(
            id_lotacao_versao=lotacao_versao,
            id_organograma_versao=organograma,
            id_patriarca=patriarca,
            id_orgao_lotacao=orgao,
            js_conteudo={'servidores': [{'cpf': '111'}, {'cpf': '222'}]},
            dat_criacao=timezone.now()
        )
        
        serializer = TblLotacaoJsonOrgaoSerializer(lotacao_json)
        data = serializer.data
        
        self.assertEqual(data['total_servidores'], 2)
