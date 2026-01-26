# carga_org_lot/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, datetime
import uuid
from .models import (
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

User = get_user_model()


class TblStatusProgressoTests(TestCase):
    """Testes para o modelo TblStatusProgresso"""

    def setUp(self):
        self.status = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )

    def test_criacao_status_progresso(self):
        """Testa a criação de um status de progresso"""
        self.assertEqual(self.status.str_descricao, 'Nova Carga')
        self.assertEqual(str(self.status), 'Nova Carga')

    def test_atualizacao_status_progresso(self):
        """Testa a atualização de um status de progresso"""
        self.status.str_descricao = 'Carga em Progresso'
        self.status.save()
        status_atualizado = TblStatusProgresso.objects.get(id_status_progresso=1)
        self.assertEqual(status_atualizado.str_descricao, 'Carga em Progresso')


class TblPatriarcaTests(TestCase):
    """Testes para o modelo TblPatriarca"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )

    def test_criacao_patriarca(self):
        """Testa a criação de um patriarca"""
        self.assertEqual(self.patriarca.str_sigla_patriarca, 'MGI')
        self.assertEqual(self.patriarca.str_nome, 'Ministério da Gestão e Inovação')
        self.assertIsNotNone(self.patriarca.dat_criacao)
        self.assertEqual(str(self.patriarca), 'MGI - Ministério da Gestão e Inovação')

    def test_relacionamento_status_progresso(self):
        """Testa o relacionamento com status de progresso"""
        self.assertEqual(self.patriarca.id_status_progresso, self.status_progresso)

    def test_relacionamento_usuario(self):
        """Testa o relacionamento com usuário"""
        self.assertEqual(self.patriarca.id_usuario_criacao, self.user)

    def test_atualizacao_patriarca(self):
        """Testa a atualização de um patriarca"""
        novo_status = TblStatusProgresso.objects.create(
            id_status_progresso=2,
            str_descricao='Organograma em Progresso'
        )
        self.patriarca.id_status_progresso = novo_status
        self.patriarca.id_usuario_alteracao = self.user
        self.patriarca.save()
        
        patriarca_atualizado = TblPatriarca.objects.get(id_patriarca=self.patriarca.id_patriarca)
        self.assertEqual(patriarca_atualizado.id_status_progresso, novo_status)
        self.assertEqual(patriarca_atualizado.id_usuario_alteracao, self.user)


class TblOrganogramaVersaoTests(TestCase):
    """Testes para o modelo TblOrganogramaVersao"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca,
            str_origem='API',
            str_tipo_arquivo_original='JSON',
            str_nome_arquivo_original='organograma.json'
        )

    def test_criacao_organograma_versao(self):
        """Testa a criação de uma versão de organograma"""
        self.assertEqual(self.organograma_versao.str_origem, 'API')
        self.assertEqual(self.organograma_versao.str_tipo_arquivo_original, 'JSON')
        self.assertFalse(self.organograma_versao.flg_ativo)
        self.assertIsNotNone(self.organograma_versao.dat_processamento)

    def test_ativacao_versao(self):
        """Testa a ativação de uma versão"""
        self.organograma_versao.flg_ativo = True
        self.organograma_versao.save()
        versao_ativa = TblOrganogramaVersao.objects.get(id_organograma_versao=self.organograma_versao.id_organograma_versao)
        self.assertTrue(versao_ativa.flg_ativo)


class TblOrgaoUnidadeTests(TestCase):
    """Testes para o modelo TblOrgaoUnidade"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca,
            str_origem='API'
        )
        self.orgao_pai = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca,
            str_nome='Ministério da Gestão e Inovação',
            str_sigla='MGI',
            str_numero_hierarquia='1',
            int_nivel_hierarquia=1
        )

    def test_criacao_orgao_unidade(self):
        """Testa a criação de um órgão/unidade"""
        self.assertEqual(self.orgao_pai.str_sigla, 'MGI')
        self.assertEqual(self.orgao_pai.str_nome, 'Ministério da Gestão e Inovação')
        self.assertTrue(self.orgao_pai.flg_ativo)
        self.assertEqual(str(self.orgao_pai), 'MGI - Ministério da Gestão e Inovação')

    def test_hierarquia_orgao(self):
        """Testa a hierarquia de órgãos"""
        unidade_filha = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca,
            str_nome='Secretaria de Gestão',
            str_sigla='SEGES',
            id_orgao_unidade_pai=self.orgao_pai,
            str_numero_hierarquia='1.1',
            int_nivel_hierarquia=2
        )
        self.assertEqual(unidade_filha.id_orgao_unidade_pai, self.orgao_pai)
        self.assertEqual(unidade_filha.int_nivel_hierarquia, 2)


class TblOrganogramaJsonTests(TestCase):
    """Testes para o modelo TblOrganogramaJson"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca,
            str_origem='API'
        )
        self.json_organograma = TblOrganogramaJson.objects.create(
            id_organograma_versao=self.organograma_versao,
            js_conteudo={'orgaos': []}
        )

    def test_criacao_json_organograma(self):
        """Testa a criação de um JSON de organograma"""
        self.assertEqual(self.json_organograma.js_conteudo, {'orgaos': []})
        self.assertIsNotNone(self.json_organograma.dat_criacao)

    def test_relacionamento_one_to_one(self):
        """Testa o relacionamento OneToOne com a versão"""
        self.assertEqual(self.json_organograma.id_organograma_versao, self.organograma_versao)


class TblLotacaoVersaoTests(TestCase):
    """Testes para o modelo TblLotacaoVersao"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca,
            str_origem='API'
        )
        self.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=self.patriarca,
            id_organograma_versao=self.organograma_versao,
            str_origem='ARQUIVO',
            str_tipo_arquivo_original='CSV',
            str_nome_arquivo_original='lotacao.csv'
        )

    def test_criacao_lotacao_versao(self):
        """Testa a criação de uma versão de lotação"""
        self.assertEqual(self.lotacao_versao.str_origem, 'ARQUIVO')
        self.assertEqual(self.lotacao_versao.str_tipo_arquivo_original, 'CSV')
        self.assertFalse(self.lotacao_versao.flg_ativo)


class TblLotacaoTests(TestCase):
    """Testes para o modelo TblLotacao"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca,
            str_origem='API'
        )
        self.orgao = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca,
            str_nome='Secretaria de Gestão',
            str_sigla='SEGES'
        )
        self.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=self.patriarca,
            id_organograma_versao=self.organograma_versao,
            str_origem='ARQUIVO'
        )
        self.lotacao = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao,
            str_cpf='12345678901',
            str_cargo_original='Analista',
            str_cargo_normalizado='ANALISTA',
            dat_referencia=date.today()
        )

    def test_criacao_lotacao(self):
        """Testa a criação de uma lotação"""
        self.assertEqual(self.lotacao.str_cpf, '12345678901')
        self.assertEqual(self.lotacao.str_cargo_normalizado, 'ANALISTA')
        self.assertTrue(self.lotacao.flg_valido)

    def test_lotacao_com_erro_validacao(self):
        """Testa lotação com erro de validação"""
        lotacao_invalida = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao,
            str_cpf='00000000000',
            flg_valido=False,
            str_erros_validacao='CPF inválido'
        )
        self.assertFalse(lotacao_invalida.flg_valido)
        self.assertEqual(lotacao_invalida.str_erros_validacao, 'CPF inválido')


class TblLotacaoJsonOrgaoTests(TestCase):
    """Testes para o modelo TblLotacaoJsonOrgao"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca,
            str_origem='API'
        )
        self.orgao = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca,
            str_nome='Secretaria de Gestão',
            str_sigla='SEGES'
        )
        self.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=self.patriarca,
            id_organograma_versao=self.organograma_versao,
            str_origem='ARQUIVO'
        )
        self.json_lotacao = TblLotacaoJsonOrgao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao,
            js_conteudo={'lotacoes': []}
        )

    def test_criacao_json_lotacao(self):
        """Testa a criação de um JSON de lotação"""
        self.assertEqual(self.json_lotacao.js_conteudo, {'lotacoes': []})
        self.assertIsNotNone(self.json_lotacao.dat_criacao)


class TblLotacaoInconsistenciaTests(TestCase):
    """Testes para o modelo TblLotacaoInconsistencia"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca,
            str_origem='API'
        )
        self.orgao = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca,
            str_nome='Secretaria de Gestão',
            str_sigla='SEGES'
        )
        self.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=self.patriarca,
            id_organograma_versao=self.organograma_versao,
            str_origem='ARQUIVO'
        )
        self.lotacao = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca,
            id_orgao_lotacao=self.orgao,
            str_cpf='12345678901'
        )
        self.inconsistencia = TblLotacaoInconsistencia.objects.create(
            id_lotacao=self.lotacao,
            str_tipo='CPF Duplicado',
            str_detalhe='CPF já existe em outra lotação'
        )

    def test_criacao_inconsistencia(self):
        """Testa a criação de uma inconsistência"""
        self.assertEqual(self.inconsistencia.str_tipo, 'CPF Duplicado')
        self.assertIsNotNone(self.inconsistencia.dat_registro)


class TblTokenEnvioCargaTests(TestCase):
    """Testes para o modelo TblTokenEnvioCarga"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )
        self.status_token = TblStatusTokenEnvioCarga.objects.create(
            id_status_token_envio_carga=1,
            str_descricao='Solicitando Token'
        )
        self.token = TblTokenEnvioCarga.objects.create(
            id_patriarca=self.patriarca,
            id_status_token_envio_carga=self.status_token,
            str_token_retorno='abc123xyz'
        )

    def test_criacao_token(self):
        """Testa a criação de um token"""
        self.assertEqual(self.token.str_token_retorno, 'abc123xyz')
        self.assertIsNotNone(self.token.dat_data_hora_inicio)


class TblCargaPatriarcaTests(TestCase):
    """Testes para o modelo TblCargaPatriarca"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )
        self.status_token = TblStatusTokenEnvioCarga.objects.create(
            id_status_token_envio_carga=1,
            str_descricao='Token Adquirido'
        )
        self.token = TblTokenEnvioCarga.objects.create(
            id_patriarca=self.patriarca,
            id_status_token_envio_carga=self.status_token,
            str_token_retorno='abc123xyz'
        )
        self.status_carga = TblStatusCarga.objects.create(
            id_status_carga=1,
            str_descricao='Enviando Carga de Organograma',
            flg_sucesso=0
        )
        self.tipo_carga = TblTipoCarga.objects.create(
            id_tipo_carga=1,
            str_descricao='Organograma'
        )
        self.carga = TblCargaPatriarca.objects.create(
            id_patriarca=self.patriarca,
            id_token_envio_carga=self.token,
            id_status_carga=self.status_carga,
            id_tipo_carga=self.tipo_carga
        )

    def test_criacao_carga(self):
        """Testa a criação de uma carga"""
        self.assertEqual(self.carga.id_tipo_carga.str_descricao, 'Organograma')
        self.assertIsNotNone(self.carga.dat_data_hora_inicio)


class TblDetalheStatusCargaTests(TestCase):
    """Testes para o modelo TblDetalheStatusCarga"""

    def setUp(self):
        self.user = User.objects.create_user(
            str_email='test@test.com',
            str_nome='Test User',
            str_senha='password123',
            id_status_usuario=1,
            id_tipo_usuario=1,
            id_classificacao_usuario=1
        )
        self.status_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao='Nova Carga'
        )
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='MGI',
            str_nome='Ministério da Gestão e Inovação',
            id_status_progresso=self.status_progresso,
            id_usuario_criacao=self.user
        )
        self.status_token = TblStatusTokenEnvioCarga.objects.create(
            id_status_token_envio_carga=1,
            str_descricao='Token Adquirido'
        )
        self.token = TblTokenEnvioCarga.objects.create(
            id_patriarca=self.patriarca,
            id_status_token_envio_carga=self.status_token,
            str_token_retorno='abc123xyz'
        )
        self.status_carga = TblStatusCarga.objects.create(
            id_status_carga=1,
            str_descricao='Enviando Carga de Organograma',
            flg_sucesso=0
        )
        self.tipo_carga = TblTipoCarga.objects.create(
            id_tipo_carga=1,
            str_descricao='Organograma'
        )
        self.carga = TblCargaPatriarca.objects.create(
            id_patriarca=self.patriarca,
            id_token_envio_carga=self.token,
            id_status_carga=self.status_carga,
            id_tipo_carga=self.tipo_carga
        )
        self.detalhe = TblDetalheStatusCarga.objects.create(
            id_carga_patriarca=self.carga,
            id_status_carga=self.status_carga,
            str_mensagem='Iniciando envio'
        )

    def test_criacao_detalhe_status(self):
        """Testa a criação de um detalhe de status"""
        self.assertEqual(self.detalhe.str_mensagem, 'Iniciando envio')
        self.assertIsNotNone(self.detalhe.dat_registro)

    def test_timeline_multiplos_detalhes(self):
        """Testa a criação de múltiplos detalhes (timeline)"""
        status_sucesso = TblStatusCarga.objects.create(
            id_status_carga=2,
            str_descricao='Organograma Enviado com sucesso',
            flg_sucesso=1
        )
        detalhe2 = TblDetalheStatusCarga.objects.create(
            id_carga_patriarca=self.carga,
            id_status_carga=status_sucesso,
            str_mensagem='Envio concluído'
        )
        
        detalhes = TblDetalheStatusCarga.objects.filter(id_carga_patriarca=self.carga).order_by('dat_registro')
        self.assertEqual(detalhes.count(), 2)
        self.assertEqual(detalhes[0].str_mensagem, 'Iniciando envio')
        self.assertEqual(detalhes[1].str_mensagem, 'Envio concluído')
