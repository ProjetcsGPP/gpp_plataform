# carga_org_lot/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import uuid

from carga_org_lot.models import (
    TblStatusProgresso,
    TblPatriarca,
    TblOrganogramaVersao,
    TblOrgaoUnidade,
    TblOrganogramaJson,
    TblLotacaoVersao,
    TblLotacao,
    TblLotacaoJsonOrgao,
    TblLotacaoInconsistencia,
    TblStatusTokenEnvioCarga,
    TblTokenEnvioCarga,
    TblStatusCarga,
    TblTipoCarga,
    TblCargaPatriarca,
    TblDetalheStatusCarga,
)
from accounts.models import Aplicacao, Role
from . import CargaOrgLotTestCase

User = get_user_model()


class BaseTestDataMixin:
    """
    Mixin que cria dados base necessários para todos os testes.
    Usa get_or_create para evitar conflitos com dados que podem existir.
    """
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        # Criar usuário de teste (User customizado usa 'name' e 'email')
        cls.user = User.objects.create_user(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
        
        # Criar aplicação (ou pegar se já existir)
        cls.aplicacao, _ = Aplicacao.objects.get_or_create(
            codigointerno='CARGA_ORG_LOT',
            defaults={
                'nomeaplicacao': 'Carga Org/Lot',  # Campo correto: nomeaplicacao
                'isshowinportal': True
            }
        )
        
        # Criar role (ou pegar se já existir)
        cls.role, _ = Role.objects.get_or_create(
            codigoperfil='GESTOR_CARGA',  # Campo correto: codigoperfil
            aplicacao=cls.aplicacao,
            defaults={'nomeperfil': 'Gestor de Carga'}
        )
        
        # Criar status de progresso (ou pegar se já existirem)
        cls.status_nova_carga, _ = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=1,
            defaults={'str_descricao': "Nova Carga"}
        )
        cls.status_processando, _ = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=2,
            defaults={'str_descricao': "Processando"}
        )
        cls.status_concluido, _ = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=3,
            defaults={'str_descricao': "Concluído"}
        )
        
        # Criar patriarca (DADO DE TESTE - sempre novo)
        cls.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='SEGER',
            str_nome='Secretaria de Gestão e Recursos',
            id_status_progresso=cls.status_nova_carga,
            dat_criacao=timezone.now(),
            id_usuario_criacao=cls.user
        )
        
        # Criar versão de organograma
        cls.org_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=cls.patriarca,
            str_origem='UPLOAD',
            str_tipo_arquivo_original='xlsx',
            str_nome_arquivo_original='organograma_test.xlsx',
            dat_processamento=timezone.now(),
            str_status_processamento='PROCESSADO',
            flg_ativo=True
        )
        
        # Criar órgão/unidade raiz
        cls.orgao_raiz = TblOrgaoUnidade.objects.create(
            id_organograma_versao=cls.org_versao,
            id_patriarca=cls.patriarca,
            str_nome='SEGER - Raiz',
            str_sigla='SEGER',
            id_orgao_unidade_pai=None,
            str_numero_hierarquia='1',
            int_nivel_hierarquia=1,
            flg_ativo=True,
            dat_criacao=timezone.now(),
            id_usuario_criacao=cls.user
        )
        
        # Criar órgão/unidade filho
        cls.orgao_filho = TblOrgaoUnidade.objects.create(
            id_organograma_versao=cls.org_versao,
            id_patriarca=cls.patriarca,
            str_nome='Subsecretaria de Gestão',
            str_sigla='SUBSEGER',
            id_orgao_unidade_pai=cls.orgao_raiz,
            str_numero_hierarquia='1.1',
            int_nivel_hierarquia=2,
            flg_ativo=True,
            dat_criacao=timezone.now(),
            id_usuario_criacao=cls.user
        )
        
        # Criar versão de lotação
        cls.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=cls.patriarca,
            id_organograma_versao=cls.org_versao,
            str_origem='UPLOAD',
            str_tipo_arquivo_original='xlsx',
            str_nome_arquivo_original='lotacao_test.xlsx',
            dat_processamento=timezone.now(),
            str_status_processamento='PROCESSADO',
            flg_ativo=True
        )
        
        # Criar status de token (ou pegar se já existirem)
        cls.status_token_ativo, _ = TblStatusTokenEnvioCarga.objects.get_or_create(
            id_status_token_envio_carga=1,
            defaults={'str_descricao': 'Ativo'}
        )
        cls.status_token_expirado, _ = TblStatusTokenEnvioCarga.objects.get_or_create(
            id_status_token_envio_carga=2,
            defaults={'str_descricao': 'Expirado'}
        )
        
        # Criar token de envio
        cls.token_envio = TblTokenEnvioCarga.objects.create(
            id_patriarca=cls.patriarca,
            id_status_token_envio_carga=cls.status_token_ativo,
            str_token_retorno='token_test_123456',
            dat_data_hora_inicio=timezone.now()
        )
        
        # Criar status de carga (ou pegar se já existirem)
        cls.status_carga_pendente, _ = TblStatusCarga.objects.get_or_create(
            id_status_carga=1,
            defaults={'str_descricao': 'Pendente', 'flg_sucesso': 0}
        )
        cls.status_carga_sucesso, _ = TblStatusCarga.objects.get_or_create(
            id_status_carga=2,
            defaults={'str_descricao': 'Sucesso', 'flg_sucesso': 1}
        )
        
        # Criar tipo de carga (ou pegar se já existirem)
        cls.tipo_carga_org, _ = TblTipoCarga.objects.get_or_create(
            id_tipo_carga=1,
            defaults={'str_descricao': 'Organograma'}
        )
        cls.tipo_carga_lot, _ = TblTipoCarga.objects.get_or_create(
            id_tipo_carga=2,
            defaults={'str_descricao': 'Lotação'}
        )


# ============================================
# TESTES DE MODELOS
# ============================================

class TblStatusProgressoTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblStatusProgresso"""
    
    def test_create_status_progresso(self):
        """Deve criar um status de progresso"""
        status = TblStatusProgresso.objects.get(id_status_progresso=1)
        self.assertEqual(status.str_descricao, "Nova Carga")
        self.assertEqual(str(status), "Nova Carga")
    
    def test_status_progresso_count(self):
        """Deve ter pelo menos 3 status de progresso criados no setup"""
        count = TblStatusProgresso.objects.count()
        self.assertGreaterEqual(count, 3)


class TblPatriarcaTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblPatriarca"""
    
    def test_create_patriarca(self):
        """Deve criar um patriarca"""
        self.assertEqual(self.patriarca.str_sigla_patriarca, 'SEGER')
        self.assertEqual(self.patriarca.str_nome, 'Secretaria de Gestão e Recursos')
        self.assertEqual(self.patriarca.id_status_progresso, self.status_nova_carga)
    
    def test_patriarca_str_representation(self):
        """Deve retornar representação string correta"""
        expected = f"{self.patriarca.str_sigla_patriarca} - {self.patriarca.str_nome}"
        self.assertEqual(str(self.patriarca), expected)
    
    def test_patriarca_requires_user_creation(self):
        """Deve exigir usuário de criação"""
        self.assertEqual(self.patriarca.id_usuario_criacao, self.user)
        self.assertIsNotNone(self.patriarca.dat_criacao)
    
    def test_patriarca_update_fields(self):
        """Deve atualizar campos de alteração"""
        self.patriarca.str_nome = 'Nome Atualizado'
        self.patriarca.id_usuario_alteracao = self.user
        self.patriarca.dat_alteracao = timezone.now()
        self.patriarca.save()
        
        self.patriarca.refresh_from_db()
        self.assertEqual(self.patriarca.str_nome, 'Nome Atualizado')
        self.assertIsNotNone(self.patriarca.dat_alteracao)


class TblOrganogramaVersaoTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblOrganogramaVersao"""
    
    def test_create_organograma_versao(self):
        """Deve criar uma versão de organograma"""
        self.assertEqual(self.org_versao.id_patriarca, self.patriarca)
        self.assertEqual(self.org_versao.str_origem, 'UPLOAD')
        self.assertTrue(self.org_versao.flg_ativo)
    
    def test_organograma_versao_str_representation(self):
        """Deve retornar representação string correta"""
        expected = f"Organograma v{self.org_versao.id_organograma_versao} - {self.patriarca.str_sigla_patriarca}"
        self.assertEqual(str(self.org_versao), expected)
    
    def test_organograma_versao_status_processamento(self):
        """Deve armazenar status de processamento"""
        self.assertEqual(self.org_versao.str_status_processamento, 'PROCESSADO')
        self.assertIsNone(self.org_versao.str_mensagem_processamento)


class TblOrgaoUnidadeTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblOrgaoUnidade"""
    
    def test_create_orgao_raiz(self):
        """Deve criar um órgão raiz"""
        self.assertIsNone(self.orgao_raiz.id_orgao_unidade_pai)
        self.assertEqual(self.orgao_raiz.int_nivel_hierarquia, 1)
        self.assertEqual(self.orgao_raiz.str_numero_hierarquia, '1')
    
    def test_create_orgao_filho(self):
        """Deve criar um órgão filho com referência ao pai"""
        self.assertEqual(self.orgao_filho.id_orgao_unidade_pai, self.orgao_raiz)
        self.assertEqual(self.orgao_filho.int_nivel_hierarquia, 2)
        self.assertEqual(self.orgao_filho.str_numero_hierarquia, '1.1')
    
    def test_orgao_unidade_str_representation(self):
        """Deve retornar representação string correta"""
        expected = f"{self.orgao_raiz.str_sigla} - {self.orgao_raiz.str_nome}"
        self.assertEqual(str(self.orgao_raiz), expected)
    
    def test_orgao_unidade_cascade_delete(self):
        """Deve deletar filhos quando pai for deletado"""
        orgao_id = self.orgao_filho.id_orgao_unidade
        self.orgao_raiz.delete()
        
        with self.assertRaises(TblOrgaoUnidade.DoesNotExist):
            TblOrgaoUnidade.objects.get(id_orgao_unidade=orgao_id)


class TblOrganogramaJsonTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblOrganogramaJson"""
    
    def test_create_organograma_json(self):
        """Deve criar um JSON de organograma"""
        json_data = {
            "orgaos": [
                {"sigla": "SEGER", "nome": "Secretaria"}
            ]
        }
        
        org_json = TblOrganogramaJson.objects.create(
            id_organograma_versao=self.org_versao,
            js_conteudo=json_data,
            dat_criacao=timezone.now()
        )
        
        self.assertEqual(org_json.js_conteudo, json_data)
        self.assertIsNone(org_json.dat_envio_api)
    
    def test_organograma_json_str_representation(self):
        """Deve retornar representação string correta"""
        org_json = TblOrganogramaJson.objects.create(
            id_organograma_versao=self.org_versao,
            js_conteudo={},
            dat_criacao=timezone.now()
        )
        
        expected = f"JSON Organograma v{self.org_versao.id_organograma_versao}"
        self.assertEqual(str(org_json), expected)
    
    def test_organograma_json_envio_api(self):
        """Deve registrar envio à API"""
        org_json = TblOrganogramaJson.objects.create(
            id_organograma_versao=self.org_versao,
            js_conteudo={},
            dat_criacao=timezone.now(),
            dat_envio_api=timezone.now(),
            str_status_envio='SUCESSO',
            str_mensagem_retorno='Enviado com sucesso'
        )
        
        self.assertIsNotNone(org_json.dat_envio_api)
        self.assertEqual(org_json.str_status_envio, 'SUCESSO')


class TblLotacaoVersaoTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblLotacaoVersao"""
    
    def test_create_lotacao_versao(self):
        """Deve criar uma versão de lotação"""
        self.assertEqual(self.lotacao_versao.id_patriarca, self.patriarca)
        self.assertEqual(self.lotacao_versao.id_organograma_versao, self.org_versao)
        self.assertTrue(self.lotacao_versao.flg_ativo)
    
    def test_lotacao_versao_str_representation(self):
        """Deve retornar representação string correta"""
        expected = f"Lotação v{self.lotacao_versao.id_lotacao_versao} - {self.patriarca.str_sigla_patriarca}"
        self.assertEqual(str(self.lotacao_versao), expected)


class TblLotacaoTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblLotacao"""
    
    def test_create_lotacao_valida(self):
        """Deve criar uma lotação válida"""
        lotacao = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.org_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao_raiz,
            id_unidade_lotacao=self.orgao_filho,
            str_cpf='123.456.789-00',
            str_cargo_original='Analista',
            str_cargo_normalizado='ANALISTA',
            flg_valido=True,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        self.assertTrue(lotacao.flg_valido)
        self.assertEqual(lotacao.str_cpf, '123.456.789-00')
    
    def test_create_lotacao_invalida(self):
        """Deve criar uma lotação inválida com erros"""
        lotacao = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.org_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao_raiz,
            str_cpf='CPF_INVALIDO',
            flg_valido=False,
            str_erros_validacao='CPF inválido',
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        self.assertFalse(lotacao.flg_valido)
        self.assertIsNotNone(lotacao.str_erros_validacao)
    
    def test_lotacao_str_representation(self):
        """Deve retornar representação string correta"""
        lotacao = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.org_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao_raiz,
            str_cpf='123.456.789-00',
            flg_valido=True,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        expected = f"Lotação {lotacao.str_cpf} - {self.orgao_raiz.str_sigla}"
        self.assertEqual(str(lotacao), expected)


class TblLotacaoJsonOrgaoTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblLotacaoJsonOrgao"""
    
    def test_create_lotacao_json_orgao(self):
        """Deve criar um JSON de lotação por órgão"""
        json_data = {
            "lotacoes": [
                {"cpf": "123.456.789-00", "cargo": "Analista"}
            ]
        }
        
        lot_json = TblLotacaoJsonOrgao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.org_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao_raiz,
            js_conteudo=json_data,
            dat_criacao=timezone.now()
        )
        
        self.assertEqual(lot_json.js_conteudo, json_data)
        self.assertEqual(lot_json.id_orgao_lotacao, self.orgao_raiz)
    
    def test_lotacao_json_orgao_str_representation(self):
        """Deve retornar representação string correta"""
        lot_json = TblLotacaoJsonOrgao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.org_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao_raiz,
            js_conteudo={},
            dat_criacao=timezone.now()
        )
        
        expected = f"JSON Lotação {self.orgao_raiz.str_sigla}"
        self.assertEqual(str(lot_json), expected)


class TblLotacaoInconsistenciaTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblLotacaoInconsistencia"""
    
    def test_create_inconsistencia(self):
        """Deve criar uma inconsistência de lotação"""
        lotacao = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.org_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao_raiz,
            str_cpf='INVALIDO',
            flg_valido=False,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        inconsistencia = TblLotacaoInconsistencia.objects.create(
            id_lotacao=lotacao,
            str_tipo='CPF_INVALIDO',
            str_detalhe='CPF não possui formato válido',
            dat_registro=timezone.now()
        )
        
        self.assertEqual(inconsistencia.str_tipo, 'CPF_INVALIDO')
        self.assertEqual(inconsistencia.id_lotacao, lotacao)
    
    def test_inconsistencia_str_representation(self):
        """Deve retornar representação string correta"""
        lotacao = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.org_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao_raiz,
            str_cpf='INVALIDO',
            flg_valido=False,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        inconsistencia = TblLotacaoInconsistencia.objects.create(
            id_lotacao=lotacao,
            str_tipo='CPF_INVALIDO',
            str_detalhe='Erro',
            dat_registro=timezone.now()
        )
        
        expected = f"{inconsistencia.str_tipo} - Lotação {lotacao.id_lotacao}"
        self.assertEqual(str(inconsistencia), expected)


class TblTokenEnvioCargaTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblTokenEnvioCarga"""
    
    def test_create_token_envio(self):
        """Deve criar um token de envio"""
        self.assertEqual(self.token_envio.id_patriarca, self.patriarca)
        self.assertEqual(self.token_envio.str_token_retorno, 'token_test_123456')
        self.assertEqual(self.token_envio.id_status_token_envio_carga, self.status_token_ativo)
    
    def test_token_envio_str_representation(self):
        """Deve retornar representação string correta"""
        expected = f"Token {self.token_envio.id_token_envio_carga} - {self.patriarca.str_sigla_patriarca}"
        self.assertEqual(str(self.token_envio), expected)
    
    def test_token_envio_finalizado(self):
        """Deve registrar data/hora de fim"""
        self.token_envio.dat_data_hora_fim = timezone.now()
        self.token_envio.save()
        
        self.token_envio.refresh_from_db()
        self.assertIsNotNone(self.token_envio.dat_data_hora_fim)


class TblStatusProgressoDuplicateTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para verificar unicidade de TblStatusProgresso"""
    
    def test_status_progresso_unique(self):
        """IDs de status devem ser únicos"""
        with self.assertRaises(Exception):
            # Tentar criar com ID que já existe
            TblStatusProgresso.objects.create(
                id_status_progresso=1,  # Já existe
                str_descricao="Duplicado"
            )


class TblCargaPatriarcaTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblCargaPatriarca"""
    
    def test_create_carga_patriarca(self):
        """Deve criar uma carga de patriarca"""
        carga = TblCargaPatriarca.objects.create(
            id_patriarca=self.patriarca,
            id_token_envio_carga=self.token_envio,
            id_status_carga=self.status_carga_pendente,
            id_tipo_carga=self.tipo_carga_org,
            dat_data_hora_inicio=timezone.now()
        )
        
        self.assertEqual(carga.id_patriarca, self.patriarca)
        self.assertEqual(carga.id_tipo_carga, self.tipo_carga_org)
        self.assertIsNone(carga.dat_data_hora_fim)
    
    def test_carga_patriarca_str_representation(self):
        """Deve retornar representação string correta"""
        carga = TblCargaPatriarca.objects.create(
            id_patriarca=self.patriarca,
            id_token_envio_carga=self.token_envio,
            id_status_carga=self.status_carga_pendente,
            id_tipo_carga=self.tipo_carga_org,
            dat_data_hora_inicio=timezone.now()
        )
        
        expected = f"Carga {carga.id_carga_patriarca} - {self.tipo_carga_org.str_descricao}"
        self.assertEqual(str(carga), expected)


class TblDetalheStatusCargaTests(BaseTestDataMixin, CargaOrgLotTestCase):
    """Testes para o modelo TblDetalheStatusCarga"""
    
    def test_create_detalhe_status(self):
        """Deve criar detalhes de status da carga"""
        carga = TblCargaPatriarca.objects.create(
            id_patriarca=self.patriarca,
            id_token_envio_carga=self.token_envio,
            id_status_carga=self.status_carga_pendente,
            id_tipo_carga=self.tipo_carga_org,
            dat_data_hora_inicio=timezone.now()
        )
        
        detalhe = TblDetalheStatusCarga.objects.create(
            id_carga_patriarca=carga,
            id_status_carga=self.status_carga_sucesso,
            dat_registro=timezone.now(),
            str_mensagem='Processamento iniciado'
        )
        
        self.assertEqual(detalhe.id_carga_patriarca, carga)
        self.assertEqual(detalhe.str_mensagem, 'Processamento iniciado')
    
    def test_detalhe_status_ordering(self):
        """Deve ordenar por data de registro"""
        carga = TblCargaPatriarca.objects.create(
            id_patriarca=self.patriarca,
            id_token_envio_carga=self.token_envio,
            id_status_carga=self.status_carga_pendente,
            id_tipo_carga=self.tipo_carga_org,
            dat_data_hora_inicio=timezone.now()
        )
        
        # Criar múltiplos detalhes
        detalhe1 = TblDetalheStatusCarga.objects.create(
            id_carga_patriarca=carga,
            id_status_carga=self.status_carga_pendente,
            dat_registro=timezone.now(),
            str_mensagem='Primeiro'
        )
        
        detalhe2 = TblDetalheStatusCarga.objects.create(
            id_carga_patriarca=carga,
            id_status_carga=self.status_carga_sucesso,
            dat_registro=timezone.now(),
            str_mensagem='Segundo'
        )
        
        detalhes = TblDetalheStatusCarga.objects.filter(id_carga_patriarca=carga)
        self.assertEqual(detalhes.first(), detalhe1)
