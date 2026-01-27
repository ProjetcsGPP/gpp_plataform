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
    TblPatriarcaSerializer, TblStatusProgressoSerializer,
    TblLotacaoJsonOrgaoSerializer,
)

User = get_user_model()


class SerializersTest(TestCase):
    """Testes para serializers"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser_serial@example.com',
            password='testpass123'
        )
        
        self.status = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=1,
            defaults={'str_descricao': 'Teste'}
        )[0]
        
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='TST',
            str_nome='Teste',
            id_status_progresso=self.status,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
    
    def test_status_progresso_serializer(self):
        """Testa TblStatusProgressoSerializer"""
        serializer = TblStatusProgressoSerializer(self.status)
        self.assertEqual(serializer.data['str_descricao'], 'Teste')
    
    def test_patriarca_serializer(self):
        """Testa TblPatriarcaSerializer"""
        serializer = TblPatriarcaSerializer(self.patriarca)
        self.assertEqual(serializer.data['str_sigla_patriarca'], 'TST')
    
    def test_lotacao_json_serializer_total_servidores(self):
        """Testa campo calculado total_servidores"""
        organograma = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca,
            str_origem='TESTE',
            dat_processamento=timezone.now(),
            str_status_processamento='PROCESSADO',
            flg_ativo=True
        )
        
        lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=self.patriarca,
            id_organograma_versao=organograma,
            str_origem='TESTE',
            dat_processamento=timezone.now(),
            str_status_processamento='PROCESSADO',
            flg_ativo=True
        )
        
        orgao = TblOrgaoUnidade.objects.create(
            id_organograma_versao=organograma,
            id_patriarca=self.patriarca,
            str_nome='Órgão Teste',
            str_sigla='OT',
            int_nivel_hierarquia=1,
            flg_ativo=True,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        lotacao_json = TblLotacaoJsonOrgao.objects.create(
            id_lotacao_versao=lotacao_versao,
            id_organograma_versao=organograma,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=orgao,
            js_conteudo={'servidores': [{'cpf': '111'}, {'cpf': '222'}]},
            dat_criacao=timezone.now()
        )
        
        serializer = TblLotacaoJsonOrgaoSerializer(lotacao_json)
        self.assertEqual(serializer.data['total_servidores'], 2)
