"""
Teste de diagnóstico para entender por que a busca não retorna resultados.
Execute este teste e compartilhe o output.
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import Aplicacao, Role, UserRole
from acoes_pngi.models import (
    AcaoAnotacaoAlinhamento,
    Acoes,
    TipoAnotacaoAlinhamento,
    VigenciaPNGI,
)

User = get_user_model()


class DiagnosticSearchTest(APITestCase):
    """Teste para diagnosticar problemas com busca"""

    databases = {"default", "gpp_plataform_db"}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.app_acoes, _ = Aplicacao.objects.get_or_create(
            codigointerno="ACOES_PNGI", defaults={"nomeaplicacao": "Ações PNGI"}
        )
        cls.role, _ = Role.objects.get_or_create(
            codigoperfil="GESTOR_PNGI",
            aplicacao=cls.app_acoes,
            defaults={"nomeperfil": "Gestor PNGI"},
        )

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass123", name="Test User"
        )

        UserRole.objects.create(
            user=self.user, aplicacao=self.app_acoes, role=self.role
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi="Vigência 2025",
            datiniciovigencia=timezone.now().date(),
            datfinalvigencia=timezone.now().date() + timedelta(days=365),
        )

        self.acao1 = Acoes.objects.create(
            strapelido="Ação 1",
            strdescricaoacao="Descrição Ação 1",
            strdescricaoentrega="Entrega 1",
            idvigenciapngi=self.vigencia,
        )

        self.tipo1 = TipoAnotacaoAlinhamento.objects.create(
            strdescricaotipoanotacaoalinhamento="Tipo 1"
        )

        # CRIAR ANOTAÇÃO COM VALORES EXATOS
        self.anotacao1 = AcaoAnotacaoAlinhamento.objects.create(
            idacao=self.acao1,
            idtipoanotacaoalinhamento=self.tipo1,
            datdataanotacaoalinhamento=timezone.now(),
            strdescricaoanotacaoalinhamento="Descrição Anotação 1",
            strnumeromonitoramento="12345",
        )

        self.api_base_url = "/api/v1/acoes_pngi/acoes-anotacao-alinhamento/"

    def _get_results(self, response):
        if isinstance(response.data, list):
            return response.data
        else:
            return response.data.get("results", response.data)

    def test_01_check_database_objects(self):
        """
        ✅ TESTE 1: Verifica se os objetos existem no banco
        """
        print("\n" + "=" * 80)
        print("TESTE 1: VERIFICANDO OBJETOS NO BANCO DE DADOS")
        print("=" * 80)

        all_anotacoes = AcaoAnotacaoAlinhamento.objects.all()
        count = all_anotacoes.count()

        print(f"\n📊 Total de anotações no banco: {count}")

        for anotacao in all_anotacoes:
            print(f"\n  ID: {anotacao.idacaoanotacaoalinhamento}")
            print(f"  Descrição: '{anotacao.strdescricaoanotacaoalinhamento}'")
            print(f"  Número Monitoramento: '{anotacao.strnumeromonitoramento}'")
            print(f"  Ação: '{anotacao.idacao.strapelido}'")

        self.assertGreater(count, 0, "❌ ERRO: Nenhuma anotação no banco!")
        print("\n✅ OK: Anotações encontradas no banco")

    def test_02_list_all_without_search(self):
        """
        ✅ TESTE 2: Lista TUDO sem filtro de busca
        """
        print("\n" + "=" * 80)
        print("TESTE 2: LISTANDO TODAS AS ANOTAÇÕES (SEM BUSCA)")
        print("=" * 80)

        response = self.client.get(self.api_base_url)

        print(f"\n📡 Status code: {response.status_code}")
        print(f"📡 Tipo de resposta: {type(response.data)}")

        results = self._get_results(response)
        print(f"\n📊 Total de resultados: {len(results)}")

        if len(results) > 0:
            print("\n📝 Primeiros resultados:")
            for i, result in enumerate(results[:2]):
                print(f"\n  [{i}] ID: {result.get('idacaoanotacaoalinhamento')}")
                print(
                    f"      Descrição: '{result.get('strdescricaoanotacaoalinhamento')}'"
                )
                print(f"      Número: '{result.get('strnumeromonitoramento')}'")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(results), 0, "❌ ERRO: Lista vazia mesmo sem filtro!")
        print("\n✅ OK: Anotações retornadas na lista")

    def test_03_search_exact_description(self):
        """
        ✅ TESTE 3: Busca com descrição EXATA
        """
        print("\n" + "=" * 80)
        print("TESTE 3: BUSCA POR DESCRIÇÃO EXATA")
        print("=" * 80)

        search_term = "Descrição Anotação 1"
        url = f"{self.api_base_url}?search={search_term}"

        print(f"\n🔍 Buscando por: '{search_term}'")
        print(f"📡 URL: {url}")

        response = self.client.get(url)

        print(f"\n📡 Status code: {response.status_code}")
        results = self._get_results(response)
        print(f"📊 Resultados encontrados: {len(results)}")

        if len(results) > 0:
            print("\n✅ SUCESSO: Encontrados resultados!")
            for result in results:
                print(f"   - {result.get('strdescricaoanotacaoalinhamento')}")
        else:
            print("❌ FALHA: Nenhum resultado com descrição exata")

        # NÃO FAÇA ASSERTION - apenas registre
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_04_search_partial_description(self):
        """
        ✅ TESTE 4: Busca com descrição PARCIAL
        """
        print("\n" + "=" * 80)
        print("TESTE 4: BUSCA POR DESCRIÇÃO PARCIAL")
        print("=" * 80)

        test_cases = ["Descrição", "Anotação", "Anotação 1", "Des", "1"]

        for search_term in test_cases:
            url = f"{self.api_base_url}?search={search_term}"

            print(f"\n🔍 Buscando por: '{search_term}'")
            response = self.client.get(url)
            results = self._get_results(response)

            print(f"   Resultados: {len(results)}")
            if len(results) > 0:
                print("   ✅ Encontrados")
            else:
                print("   ❌ Nenhum resultado")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_05_search_exact_number(self):
        """
        ✅ TESTE 5: Busca por número EXATO
        """
        print("\n" + "=" * 80)
        print("TESTE 5: BUSCA POR NÚMERO EXATO")
        print("=" * 80)

        search_term = "12345"
        url = f"{self.api_base_url}?search={search_term}"

        print(f"\n🔍 Buscando por: '{search_term}'")
        print(f"📡 URL: {url}")

        response = self.client.get(url)

        print(f"\n📡 Status code: {response.status_code}")
        results = self._get_results(response)
        print(f"📊 Resultados encontrados: {len(results)}")

        if len(results) > 0:
            print("\n✅ SUCESSO: Encontrados resultados!")
            for result in results:
                print(f"   - Número: {result.get('strnumeromonitoramento')}")
        else:
            print("❌ FALHA: Nenhum resultado com número exato")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_06_search_partial_number(self):
        """
        ✅ TESTE 6: Busca por número PARCIAL
        """
        print("\n" + "=" * 80)
        print("TESTE 6: BUSCA POR NÚMERO PARCIAL")
        print("=" * 80)

        test_cases = ["12345", "123", "12", "1", "45"]

        for search_term in test_cases:
            url = f"{self.api_base_url}?search={search_term}"

            print(f"\n🔍 Buscando por: '{search_term}'")
            response = self.client.get(url)
            results = self._get_results(response)

            print(f"   Resultados: {len(results)}")
            if len(results) > 0:
                print("   ✅ Encontrados")
            else:
                print("   ❌ Nenhum resultado")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_07_search_by_acao_name(self):
        """
        ✅ TESTE 7: Busca pelo nome da ação (deve funcionar)
        """
        print("\n" + "=" * 80)
        print("TESTE 7: BUSCA PELO NOME DA AÇÃO")
        print("=" * 80)

        search_term = "Ação"
        url = f"{self.api_base_url}?search={search_term}"

        print(f"\n🔍 Buscando por: '{search_term}'")
        print(f"📡 URL: {url}")

        response = self.client.get(url)

        print(f"\n📡 Status code: {response.status_code}")
        results = self._get_results(response)
        print(f"📊 Resultados encontrados: {len(results)}")

        if len(results) > 0:
            print("\n✅ SUCESSO: Busca por ação funciona!")
            for result in results:
                print(f"   - Ação: {result.get('idacao_display')}")
        else:
            print("❌ FALHA: Busca por ação não retorna nada")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_08_check_search_fields_in_viewset(self):
        """
        ✅ TESTE 8: Verifica quais campos estão configurados para busca
        """
        print("\n" + "=" * 80)
        print("TESTE 8: CAMPOS CONFIGURADOS PARA BUSCA NO VIEWSET")
        print("=" * 80)

        from acoes_pngi.views.api_views import AcaoAnotacaoAlinhamentoViewSet

        viewset = AcaoAnotacaoAlinhamentoViewSet()

        print("\n📋 Campos de busca configurados:")
        for field in viewset.search_fields:
            print(f"   - {field}")

        print("\n📋 Filter backends:")
        for backend in viewset.filter_backends:
            print(f"   - {backend.__name__}")

        self.assertIn(
            "strdescricaoanotacaoalinhamento",
            viewset.search_fields,
            "❌ strdescricaoanotacaoalinhamento não está em search_fields!",
        )
        self.assertIn(
            "strnumeromonitoramento",
            viewset.search_fields,
            "❌ strnumeromonitoramento não está em search_fields!",
        )

        print("\n✅ OK: Campos de busca estão configurados corretamente")
