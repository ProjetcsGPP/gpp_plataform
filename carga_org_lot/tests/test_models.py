from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
import uuid

from ..models import (
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


class BaseCargaOrgLotTestCase(TestCase):
    """
    Classe base para todos os testes do app carga_org_lot.

    Métodos / dados criados:
    - Usuário padrão: self.user
    - Status de progresso:
        self.status_nova_carga
        self.status_org_em_progresso
        self.status_lot_em_progresso
        self.status_pronto_carga
        self.status_carga_proc
        self.status_carga_finalizada
    - Tipos de carga:
        self.tipo_carga_organograma
        self.tipo_carga_lotacao
        self.tipo_carga_lotacao_unica
    - Status de token:
        self.status_token_solicitando
        self.status_token_adquirido
        self.status_token_negado
        self.status_token_expirado
        self.status_token_invalido
        self.status_token_timeout
    - Patriarca base:
        self.patriarca_pmexe
    """

    @classmethod
    def setUpTestData(cls):
        # 1) Usuário padrão
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="password123",
            name="Test User",
            idstatususuario=1,
            idtipousuario=1,
            idclassificacaousuario=1,
        )

        # 2) Status de progresso (tblstatusprogresso)
        cls.status_nova_carga = TblStatusProgresso.objects.create(
            id_status_progresso=1,
            str_descricao="Nova Carga",
        )
        cls.status_org_em_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=2,
            str_descricao="Organograma em Progresso",
        )
        cls.status_lot_em_progresso = TblStatusProgresso.objects.create(
            id_status_progresso=3,
            str_descricao="Lotação em Progresso",
        )
        cls.status_pronto_carga = TblStatusProgresso.objects.create(
            id_status_progresso=4,
            str_descricao="Pronto para Carga",
        )
        cls.status_carga_proc = TblStatusProgresso.objects.create(
            id_status_progresso=5,
            str_descricao="Carga em Processamento",
        )
        cls.status_carga_finalizada = TblStatusProgresso.objects.create(
            id_status_progresso=6,
            str_descricao="Carga Finalizada",
        )

        # 3) Tipos de carga (TblTipoCarga)
        cls.tipo_carga_organograma = TblTipoCarga.objects.create(
            id_tipo_carga=1,
            str_descricao="Organograma",
        )
        cls.tipo_carga_lotacao = TblTipoCarga.objects.create(
            id_tipo_carga=2,
            str_descricao="Lotação",
        )
        cls.tipo_carga_lotacao_unica = TblTipoCarga.objects.create(
            id_tipo_carga=3,
            str_descricao="Lotação Arq. Único",
        )

        # 4) Status de token (TblStatusTokenEnvioCarga)
        cls.status_token_solicitando = TblStatusTokenEnvioCarga.objects.create(
            id_status_token_envio_carga=1,
            str_descricao="Solicitando Token",
        )
        cls.status_token_adquirido = TblStatusTokenEnvioCarga.objects.create(
            id_status_token_envio_carga=2,
            str_descricao="Token Adquirido",
        )
        cls.status_token_negado = TblStatusTokenEnvioCarga.objects.create(
            id_status_token_envio_carga=3,
            str_descricao="Token Negado",
        )
        cls.status_token_expirado = TblStatusTokenEnvioCarga.objects.create(
            id_status_token_envio_carga=4,
            str_descricao="Token Expirado",
        )
        cls.status_token_invalido = TblStatusTokenEnvioCarga.objects.create(
            id_status_token_envio_carga=5,
            str_descricao="Token Inválido",
        )
        cls.status_token_timeout = TblStatusTokenEnvioCarga.objects.create(
            id_status_token_envio_carga=6,
            str_descricao="Tempo Ultrapassado (Solicitação)",
        )

        # 5) Patriarca base (TblPatriarca)
        cls.patriarca_pmexe = TblPatriarca.objects.create(
            id_patriarca=1,
            id_externo_patriarca="PMEXE",
            str_sigla_patriarca="PMEXE",
            str_nome="PREFEITURA TESTE",
            id_status_progresso=cls.status_nova_carga,
            id_usuario_criacao=cls.user,
        )


class TblStatusProgressoTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de status de progresso
    - atualização de status de progresso
    """

    def test_criacao_status_progresso(self):
        self.assertEqual(self.status_nova_carga.str_descricao, "Nova Carga")

    def test_atualizacao_status_progresso(self):
        self.status_nova_carga.str_descricao = "Carga em Progresso"
        self.status_nova_carga.save()
        s = TblStatusProgresso.objects.get(id_status_progresso=1)
        self.assertEqual(s.str_descricao, "Carga em Progresso")


class TblPatriarcaTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de patriarca
    - relacionamento com status de progresso
    - relacionamento com usuário
    - atualização de patriarca
    """

    def test_criacao_patriarca(self):
        self.assertEqual(self.patriarca_pmexe.str_sigla_patriarca, "PMEXE")
        self.assertEqual(self.patriarca_pmexe.str_nome, "PREFEITURA TESTE")
        self.assertIsNotNone(self.patriarca_pmexe.dat_criacao)

    def test_relacionamento_status_progresso(self):
        self.assertEqual(
            self.patriarca_pmexe.id_status_progresso, self.status_nova_carga
        )

    def test_relacionamento_usuario(self):
        self.assertEqual(self.patriarca_pmexe.id_usuario_criacao, self.user)

    def test_atualizacao_patriarca(self):
        self.patriarca_pmexe.id_status_progresso = self.status_carga_finalizada
        self.patriarca_pmexe.id_usuario_alteracao = self.user
        self.patriarca_pmexe.save()
        p = TblPatriarca.objects.get(id_patriarca=self.patriarca_pmexe.id_patriarca)
        self.assertEqual(p.id_status_progresso, self.status_carga_finalizada)
        self.assertEqual(p.id_usuario_alteracao, self.user)


class TblOrganogramaVersaoTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de versão de organograma
    - ativação de versão (flg_ativo)
    """

    def setUp(self):
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            str_origem="API",
            str_tipo_arquivo_original="JSON",
            str_nome_arquivo_original="organograma.json",
        )

    def test_criacao_organograma_versao(self):
        self.assertEqual(self.organograma_versao.str_origem, "API")
        self.assertEqual(self.organograma_versao.str_tipo_arquivo_original, "JSON")
        self.assertFalse(self.organograma_versao.flg_ativo)
        self.assertIsNotNone(self.organograma_versao.dat_processamento)

    def test_ativacao_versao(self):
        self.organograma_versao.flg_ativo = True
        self.organograma_versao.save()
        v = TblOrganogramaVersao.objects.get(
            id_organograma_versao=self.organograma_versao.id_organograma_versao
        )
        self.assertTrue(v.flg_ativo)


class TblOrgaoUnidadeTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de órgão/unidade
    - hierarquia de órgãos (pai/filho)
    """

    def setUp(self):
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            str_origem="API",
        )
        self.orgao_pai = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca_pmexe,
            str_nome="PREFEITURA TESTE",
            str_sigla="PMEXE",
            str_numero_hierarquia="1",
            int_nivel_hierarquia=1,
        )

    def test_criacao_orgao_unidade(self):
        self.assertEqual(self.orgao_pai.str_sigla, "PMEXE")
        self.assertEqual(self.orgao_pai.str_nome, "PREFEITURA TESTE")
        self.assertTrue(self.orgao_pai.flg_ativo)

    def test_hierarquia_orgao(self):
        unidade_filha = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca_pmexe,
            str_nome="Secretaria de Gestão",
            str_sigla="SEGES",
            id_orgao_unidade_pai=self.orgao_pai,
            str_numero_hierarquia="1.1",
            int_nivel_hierarquia=2,
        )
        self.assertEqual(unidade_filha.id_orgao_unidade_pai, self.orgao_pai)
        self.assertEqual(unidade_filha.int_nivel_hierarquia, 2)


class TblOrganogramaJsonTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de JSON de organograma
    - relacionamento OneToOne com versão
    """

    def setUp(self):
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            str_origem="API",
        )
        self.json_organograma = TblOrganogramaJson.objects.create(
            id_organograma_versao=self.organograma_versao,
            js_conteudo={"orgaos": []},
        )

    def test_criacao_json_organograma(self):
        self.assertEqual(self.json_organograma.js_conteudo, {"orgaos": []})
        self.assertIsNotNone(self.json_organograma.dat_criacao)

    def test_relacionamento_one_to_one(self):
        self.assertEqual(
            self.json_organograma.id_organograma_versao, self.organograma_versao
        )


class TblLotacaoVersaoTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de versão de lotação
    """

    def setUp(self):
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            str_origem="API",
        )
        self.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            id_organograma_versao=self.organograma_versao,
            str_origem="ARQUIVO",
            str_tipo_arquivo_original="CSV",
            str_nome_arquivo_original="lotacao.csv",
        )

    def test_criacao_lotacao_versao(self):
        self.assertEqual(self.lotacao_versao.str_origem, "ARQUIVO")
        self.assertEqual(self.lotacao_versao.str_tipo_arquivo_original, "CSV")
        self.assertFalse(self.lotacao_versao.flg_ativo)


class TblLotacaoTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de lotação válida
    - lotação com erro de validação
    """

    def setUp(self):
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            str_origem="API",
        )
        self.orgao = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca_pmexe,
            str_nome="Secretaria de Gestão",
            str_sigla="SEGES",
        )
        self.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            id_organograma_versao=self.organograma_versao,
            str_origem="ARQUIVO",
        )
        self.lotacao = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca_pmexe,
            id_orgao_lotacao=self.orgao,
            str_cpf="12345678901",
            str_cargo_original="Analista",
            str_cargo_normalizado="ANALISTA",
            dat_referencia=date.today(),
        )

    def test_criacao_lotacao(self):
        self.assertEqual(self.lotacao.str_cpf, "12345678901")
        self.assertEqual(self.lotacao.str_cargo_normalizado, "ANALISTA")
        self.assertTrue(self.lotacao.flg_valido)

    def test_lotacao_com_erro_validacao(self):
        lotacao_invalida = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca_pmexe,
            id_orgao_lotacao=self.orgao,
            str_cpf="00000000000",
            flg_valido=False,
            str_erros_validacao="CPF inválido",
        )
        self.assertFalse(lotacao_invalida.flg_valido)
        self.assertEqual(lotacao_invalida.str_erros_validacao, "CPF inválido")


class TblLotacaoJsonOrgaoTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de JSON de lotação por órgão
    """

    def setUp(self):
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            str_origem="API",
        )
        self.orgao = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca_pmexe,
            str_nome="Secretaria de Gestão",
            str_sigla="SEGES",
        )
        self.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            id_organograma_versao=self.organograma_versao,
            str_origem="ARQUIVO",
        )
        self.json_lotacao = TblLotacaoJsonOrgao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca_pmexe,
            id_orgao_lotacao=self.orgao,
            js_conteudo={"lotacoes": []},
        )

    def test_criacao_json_lotacao(self):
        self.assertEqual(self.json_lotacao.js_conteudo, {"lotacoes": []})
        self.assertIsNotNone(self.json_lotacao.dat_criacao)


class TblLotacaoInconsistenciaTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de inconsistência de lotação
    """

    def setUp(self):
        self.organograma_versao = TblOrganogramaVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            str_origem="API",
        )
        self.orgao = TblOrgaoUnidade.objects.create(
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca_pmexe,
            str_nome="Secretaria de Gestão",
            str_sigla="SEGES",
        )
        self.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=self.patriarca_pmexe,
            id_organograma_versao=self.organograma_versao,
            str_origem="ARQUIVO",
        )
        self.lotacao = TblLotacao.objects.create(
            id_lotacao_versao=self.lotacao_versao,
            id_organograma_versao=self.organograma_versao,
            id_patriarca=self.patriarca_pmexe,
            id_orgao_lotacao=self.orgao,
            str_cpf="12345678901",
        )
        self.inconsistencia = TblLotacaoInconsistencia.objects.create(
            id_lotacao=self.lotacao,
            str_tipo="CPF Duplicado",
            str_detalhe="CPF já existe em outra lotação",
        )

    def test_criacao_inconsistencia(self):
        self.assertEqual(self.inconsistencia.str_tipo, "CPF Duplicado")
        self.assertIsNotNone(self.inconsistencia.dat_registro)


class TblTokenEnvioCargaTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de token de envio de carga
    """

    def test_criacao_token(self):
        token = TblTokenEnvioCarga.objects.create(
            id_patriarca=self.patriarca_pmexe,
            id_status_token_envio_carga=self.status_token_solicitando,
            str_token_retorno="abc123xyz",
        )
        self.assertEqual(token.str_token_retorno, "abc123xyz")
        self.assertIsNotNone(token.dat_data_hora_inicio)


class TblCargaPatriarcaTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de carga do patriarca
    """

    def test_criacao_carga(self):
        token = TblTokenEnvioCarga.objects.create(
            id_patriarca=self.patriarca_pmexe,
            id_status_token_envio_carga=self.status_token_adquirido,
            str_token_retorno="abc123xyz",
        )
        status_carga = TblStatusCarga.objects.create(
            id_status_carga=1,
            str_descricao="Enviando Carga de Organograma",
            flg_sucesso=0,
        )
        carga = TblCargaPatriarca.objects.create(
            id_patriarca=self.patriarca_pmexe,
            id_token_envio_carga=token,
            id_status_carga=status_carga,
            id_tipo_carga=self.tipo_carga_organograma,
        )
        self.assertEqual(carga.id_tipo_carga.str_descricao, "Organograma")
        self.assertIsNotNone(carga.dat_data_hora_inicio)


class TblDetalheStatusCargaTests(BaseCargaOrgLotTestCase):
    """
    Métodos testados:
    - criação de detalhe de status
    - criação de múltiplos detalhes (timeline)
    """

    def setUp(self):
        self.token = TblTokenEnvioCarga.objects.create(
            id_patriarca=self.patriarca_pmexe,
            id_status_token_envio_carga=self.status_token_adquirido,
            str_token_retorno="abc123xyz",
        )
        self.status_carga_inicial = TblStatusCarga.objects.create(
            id_status_carga=1,
            str_descricao="Enviando Carga de Organograma",
            flg_sucesso=0,
        )
        self.status_carga_final = TblStatusCarga.objects.create(
            id_status_carga=2,
            str_descricao="Organograma Enviado com sucesso",
            flg_sucesso=1,
        )
        self.carga = TblCargaPatriarca.objects.create(
            id_patriarca=self.patriarca_pmexe,
            id_token_envio_carga=self.token,
            id_status_carga=self.status_carga_inicial,
            id_tipo_carga=self.tipo_carga_organograma,
        )
        self.detalhe_inicial = TblDetalheStatusCarga.objects.create(
            id_carga_patriarca=self.carga,
            id_status_carga=self.status_carga_inicial,
            str_mensagem="Iniciando envio",
        )

    def test_criacao_detalhe_status(self):
        self.assertEqual(self.detalhe_inicial.str_mensagem, "Iniciando envio")
        self.assertIsNotNone(self.detalhe_inicial.dat_registro)

    def test_timeline_multiplos_detalhes(self):
        detalhe2 = TblDetalheStatusCarga.objects.create(
            id_carga_patriarca=self.carga,
            id_status_carga=self.status_carga_final,
            str_mensagem="Envio concluído",
        )
        detalhes = TblDetalheStatusCarga.objects.filter(
            id_carga_patriarca=self.carga
        ).order_by("dat_registro")
        self.assertEqual(detalhes.count(), 2)
        self.assertEqual(detalhes[0].str_mensagem, "Iniciando envio")
        self.assertEqual(detalhes[1].str_mensagem, "Envio concluído")
