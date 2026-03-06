#!/usr/bin/env python
"""
Script para aplicar automaticamente as correções de nomes de campos nos testes.

Este script lê os arquivos de teste e faz substituições de nomes de campos incorretos
por nomes corretos de acordo com os models reais.

Total de correções: 29
- test_api_views_acoes.py: 8 correções
- test_api_views_alinhamento_responsaveis.py: 21 correções

Uso:
    python acoes_pngi/tests/aplicar_correcoes.py
"""

import re
from pathlib import Path


class CorretorTestes:
    """Aplica correções nos arquivos de teste"""

    def __init__(self, caminho_base):
        self.caminho_base = Path(caminho_base)
        self.correcoes_aplicadas = 0

    def corrigir_acoes(self):
        """Corrige test_api_views_acoes.py - AcaoDestaque"""
        arquivo = self.caminho_base / "test_api_views_acoes.py"
        print(f"\n\U0001f4dd Corrigindo {arquivo.name}...")

        with open(arquivo, encoding="utf-8") as f:
            conteudo = f.read()

        # Backup
        backup = conteudo

        # 1. Adicionar import timezone
        if "from django.utils import timezone" not in conteudo:
            conteudo = conteudo.replace(
                "from datetime import date, timedelta",
                "from datetime import date, timedelta\nfrom django.utils import timezone",
            )
            print("  ✅ Adicionado import: from django.utils import timezone")
            self.correcoes_aplicadas += 1

        # 2-8. Substituir campos de AcaoDestaque

        # strdescricaodestaque -> datdatadestaque
        substituicoes = [
            # setup_test_data
            (
                r"self\.destaque = AcaoDestaque\.objects\.create\(\s*idacao=self\.acao,\s*strdescricaodestaque=[^,]+,\s*ordenacao=\d+\s*\)",
                "self.destaque = AcaoDestaque.objects.create(\n            idacao=self.acao,\n            datdatadestaque=timezone.now()\n        )",
            ),
            # data dicts com strdescricaodestaque
            (
                r"'strdescricaodestaque':\s*'[^']+'",
                "'datdatadestaque': timezone.now().isoformat()",
            ),
            # data dicts com ordenacao
            (r",\s*'ordenacao':\s*\d+", ""),
            # objects.create com strdescricaodestaque
            (
                r"AcaoDestaque\.objects\.create\(\s*idacao=[^,]+,\s*strdescricaodestaque=[^,]+,\s*ordenacao=\d+\s*\)",
                "AcaoDestaque.objects.create(\n            idacao=self.acao,\n            datdatadestaque=timezone.now()\n        )",
            ),
            # ordering=ordenacao -> ordering=-datdatadestaque
            (r"ordering=ordenacao", "ordering=-datdatadestaque"),
        ]

        for padrao, substituicao in substituicoes:
            novo_conteudo = re.sub(padrao, substituicao, conteudo)
            if novo_conteudo != conteudo:
                conteudo = novo_conteudo
                self.correcoes_aplicadas += 1
                print(f"  ✅ Substituído: {padrao[:50]}...")

        # Salvar se houve mudanças
        if conteudo != backup:
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"\n✅ Arquivo {arquivo.name} corrigido!\n")
        else:
            print(f"\n⚠️  Nenhuma correção aplicada em {arquivo.name}\n")

    def corrigir_alinhamento_responsaveis(self):
        """Corrige test_api_views_alinhamento_responsaveis.py"""
        arquivo = self.caminho_base / "test_api_views_alinhamento_responsaveis.py"
        print(f"\n\U0001f4dd Corrigindo {arquivo.name}...")

        with open(arquivo, encoding="utf-8") as f:
            conteudo = f.read()

        backup = conteudo

        # PARTE 1: TipoAnotacaoAlinhamento - nome do campo completo
        print("\n  Parte 1: TipoAnotacaoAlinhamento")
        substituicoes_tipo = [
            # strdescricaotipoanotacao -> strdescricaotipoanotacaoalinhamento
            (r"'strdescricaotipoanotacao':", "'strdescricaotipoanotacaoalinhamento':"),
            (r"strdescricaotipoanotacao=", "strdescricaotipoanotacaoalinhamento="),
            # Remover stralias
            (r",\s*'stralias':\s*'[^']+'", ""),
            (r",\s*stralias=[^)]+", ""),
            # ordering
            (
                r"ordering=strdescricaotipoanotacao",
                "ordering=strdescricaotipoanotacaoalinhamento",
            ),
        ]

        for padrao, substituicao in substituicoes_tipo:
            novo_conteudo = re.sub(padrao, substituicao, conteudo)
            if novo_conteudo != conteudo:
                conteudo = novo_conteudo
                self.correcoes_aplicadas += 1
                print(f"    ✅ {padrao[:40]}...")

        # PARTE 2: AcaoAnotacaoAlinhamento - campo data
        print("\n  Parte 2: AcaoAnotacaoAlinhamento")
        substituicoes_anotacao = [
            # dtanotacaoalinhamento -> datdataanotacaoalinhamento
            (r"'dtanotacaoalinhamento':", "'datdataanotacaoalinhamento':"),
            (r"dtanotacaoalinhamento=", "datdataanotacaoalinhamento="),
        ]

        for padrao, substituicao in substituicoes_anotacao:
            novo_conteudo = re.sub(padrao, substituicao, conteudo)
            if novo_conteudo != conteudo:
                conteudo = novo_conteudo
                self.correcoes_aplicadas += 1
                print(f"    ✅ {padrao[:40]}...")

        # PARTE 3: UsuarioResponsavel - PK correta
        print("\n  Parte 3: UsuarioResponsavel")
        substituicoes_usuario = [
            # idusuarioresponsavel -> pk
            (r"\.idusuarioresponsavel}/", ".pk}/"),
            (r"novo_resp\.idusuarioresponsavel", "novo_resp.pk"),
        ]

        for padrao, substituicao in substituicoes_usuario:
            novo_conteudo = re.sub(padrao, substituicao, conteudo)
            if novo_conteudo != conteudo:
                conteudo = novo_conteudo
                self.correcoes_aplicadas += 1
                print(f"    ✅ {padrao[:40]}...")

        # PARTE 4: RelacaoAcaoUsuarioResponsavel - PK correta
        print("\n  Parte 4: RelacaoAcaoUsuarioResponsavel")
        substituicoes_relacao = [
            # idrelacaoacaousuarioresponsavel -> idacaousuarioresponsavel
            (r"idrelacaoacaousuarioresponsavel", "idacaousuarioresponsavel"),
        ]

        for padrao, substituicao in substituicoes_relacao:
            novo_conteudo = re.sub(padrao, substituicao, conteudo)
            if novo_conteudo != conteudo:
                conteudo = novo_conteudo
                self.correcoes_aplicadas += 1
                print(f"    ✅ {padrao[:40]}...")

        # Salvar se houve mudanças
        if conteudo != backup:
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"\n✅ Arquivo {arquivo.name} corrigido!\n")
        else:
            print(f"\n⚠️  Nenhuma correção aplicada em {arquivo.name}\n")

    def executar(self):
        """Executa todas as correções"""
        print("\n" + "=" * 70)
        print("🔧 CORRETOR AUTOMÁTICO DE TESTES - Ações PNGI")
        print("=" * 70)

        self.corrigir_acoes()
        self.corrigir_alinhamento_responsaveis()

        print("\n" + "=" * 70)
        print(f"✅ CONCLUÍDO! Total de correções aplicadas: {self.correcoes_aplicadas}")
        print("=" * 70)
        print("\nPróximos passos:")
        print("1. Revisar as mudanças com 'git diff'")
        print("2. Executar os testes: python manage.py test acoes_pngi.tests")
        print("3. Fazer commit das correções")
        print()


if __name__ == "__main__":
    # Detectar caminho base do projeto
    import sys
    from pathlib import Path

    # Se executado do diretório tests
    if Path.cwd().name == "tests":
        caminho = Path.cwd()
    # Se executado da raiz do projeto
    elif (Path.cwd() / "acoes_pngi" / "tests").exists():
        caminho = Path.cwd() / "acoes_pngi" / "tests"
    # Se executado de acoes_pngi
    elif (Path.cwd() / "tests").exists():
        caminho = Path.cwd() / "tests"
    else:
        print("❌ Erro: Execute este script da raiz do projeto ou do diretório tests")
        sys.exit(1)

    corretor = CorretorTestes(caminho)
    corretor.executar()
