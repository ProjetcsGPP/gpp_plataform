#!/usr/bin/env python3
"""fix_all_test_errors.py

Script para corrigir TODOS os erros restantes nos testes (76 erros).

Execução:
    python acoes_pngi/tests/fix_all_test_errors.py

Problemas corrigidos:
1. ✅ ValidationError datfinalvigencia - Adiciona campo obrigatório
2. ✅ IndexError list index out of range - Garante fixtures antes de testes
3. ✅ AssertionError 0 != 1/2 - Adiciona ideixo e idsituacaoacao nas Acoes
4. ✅ AttributeError self.eixo/vigencia - Adiciona atributos no setUp()
"""

import re
from pathlib import Path


class TestErrorFixer:
    """Corrige erros nos arquivos de teste"""

    def __init__(self, tests_dir):
        self.tests_dir = Path(tests_dir)
        self.changes_made = []

    def fix_all(self):
        """Executa todas as correções"""
        print("🔧 Iniciando correção de TODOS os erros de teste...")
        print("=" * 70)

        # 1. Adicionar datfinalvigencia em VigenciaPNGI
        self.fix_vigencia_validation_errors()

        # 2. Corrigir AttributeError self.eixo e self.vigencia
        self.fix_attribute_errors()

        # 3. Garantir fixtures completas antes de testes de filtros
        self.fix_index_errors_and_assertions()

        print("\n" + "=" * 70)
        print(f"✅ Correções concluídas! Total de mudanças: {len(self.changes_made)}")
        self._print_summary()

    # ========================================================================
    # 1. CORRIGIR VALIDATION ERRORS - Adicionar datfinalvigencia
    # ========================================================================

    def fix_vigencia_validation_errors(self):
        """Adiciona datfinalvigencia em todas criações de VigenciaPNGI"""
        print("\n1️⃣  Corrigindo ValidationError (datfinalvigencia)...")

        test_files = list(self.tests_dir.glob("test_*.py"))

        for filepath in test_files:
            content = filepath.read_text(encoding="utf-8")
            original_content = content

            # Padrão 1: VigenciaPNGI.objects.create(...datiniciovigencia=date(...)) SEM datfinalvigencia
            # Adicionar datfinalvigencia logo após datiniciovigencia

            def add_datfinalvigencia(match):
                full_text = match.group(0)
                year = match.group(2)

                # Se termina com vírgula, adicionar após
                if ",\n" in full_text or ", " in full_text:
                    return (
                        full_text
                        + f",\n            datfinalvigencia=date({year}, 12, 31)"
                    )
                # Se termina com ), adicionar antes do )
                elif full_text.endswith(")"):
                    return (
                        full_text[:-1]
                        + f",\n            datfinalvigencia=date({year}, 12, 31))"
                    )
                else:
                    return (
                        full_text
                        + f",\n            datfinalvigencia=date({year}, 12, 31)"
                    )

            # Aplicar correção
            new_content = content

            # Encontrar todos os VigenciaPNGI.objects.create
            vigencia_pattern = r"VigenciaPNGI\.objects\.create\([^)]+\)"
            matches = list(re.finditer(vigencia_pattern, content, re.DOTALL))

            for match in reversed(matches):  # Reverso para não afetar índices
                vigencia_create = match.group(0)

                # Se NÃO tem datfinalvigencia, adicionar
                if "datfinalvigencia" not in vigencia_create:
                    # Extrair ano de datiniciovigencia
                    year_match = re.search(
                        r"datiniciovigencia=date\((\d{4})", vigencia_create
                    )
                    if year_match:
                        year = year_match.group(1)

                        # Adicionar antes do último )
                        fixed_vigencia = (
                            vigencia_create[:-1]
                            + f",\n            datfinalvigencia=date({year}, 12, 31))"
                        )

                        # Substituir no conteúdo
                        new_content = (
                            new_content[: match.start()]
                            + fixed_vigencia
                            + new_content[match.end() :]
                        )

            if new_content != original_content:
                filepath.write_text(new_content, encoding="utf-8")
                self.changes_made.append(
                    f"✅ {filepath.name}: Adicionado datfinalvigencia"
                )
                print(f"   ✅ {filepath.name}")

    # ========================================================================
    # 2. CORRIGIR ATTRIBUTE ERRORS - Adicionar self.eixo e self.vigencia
    # ========================================================================

    def fix_attribute_errors(self):
        """Adiciona self.eixo e self.vigencia no setup_test_data() onde estão faltando"""
        print("\n2️⃣  Corrigindo AttributeError (self.eixo, self.vigencia)...")

        filepath = self.tests_dir / "test_api_views.py"
        if not filepath.exists():
            print("   ⚠️  Arquivo não encontrado: test_api_views.py")
            return

        content = filepath.read_text(encoding="utf-8")
        original_content = content

        # Substituir variáveis locais por self.
        replacements = [
            (r"(\s+)vigencia = VigenciaPNGI", r"\1self.vigencia = VigenciaPNGI"),
            (
                r"(\s+)eixo = Eixo\.objects\.create",
                r"\1self.eixo = Eixo.objects.create",
            ),
            (
                r"(\s+)situacao = SituacaoAcao\.objects\.create",
                r"\1self.situacao = SituacaoAcao.objects.create",
            ),
        ]

        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)

        # Substituir referências às variáveis locais por self.
        content = re.sub(
            r"idvigenciapngi=vigencia", r"idvigenciapngi=self.vigencia", content
        )
        content = re.sub(r"ideixo=eixo", r"ideixo=self.eixo", content)
        content = re.sub(
            r"idsituacaoacao=situacao", r"idsituacaoacao=self.situacao", content
        )

        if content != original_content:
            filepath.write_text(content, encoding="utf-8")
            self.changes_made.append(
                "✅ test_api_views.py: Adicionado self.eixo, self.vigencia e self.situacao"
            )
            print("   ✅ test_api_views.py")

    # ========================================================================
    # 3. CORRIGIR INDEX ERRORS E ASSERTION ERRORS
    # ========================================================================

    def fix_index_errors_and_assertions(self):
        """Corrige IndexErrors e AssertionErrors (0 != 1/2) garantindo fixtures"""
        print("\n3️⃣  Corrigindo IndexError e AssertionError (fixtures incompletas)...")

        test_files = [
            "test_api_views.py",
            "test_api_acoes_views.py",
            "test_api_alinhamento_views.py",
            "test_api_responsavel_views.py",
            "test_api_views_acoes.py",
            "test_api_views_alinhamento_responsaveis.py",
        ]

        for filename in test_files:
            filepath = self.tests_dir / filename
            if not filepath.exists():
                continue

            content = filepath.read_text(encoding="utf-8")
            original_content = content

            # Adicionar ideixo quando falta
            content = self._add_missing_fk_to_acoes(content, "ideixo")

            # Adicionar idsituacaoacao quando falta
            content = self._add_missing_fk_to_acoes(content, "idsituacaoacao")

            # Garantir que setup_test_data cria Eixo e SituacaoAcao
            content = self._ensure_setup_creates_dependencies(content)

            if content != original_content:
                filepath.write_text(content, encoding="utf-8")
                self.changes_made.append(f"✅ {filename}: Fixtures completas")
                print(f"   ✅ {filename}")

    def _add_missing_fk_to_acoes(self, content, fk_name):
        """Adiciona FK faltando em Acoes.objects.create()"""

        # Padrão: Acoes.objects.create(...idvigenciapngi=...) SEM o FK
        acoes_pattern = r"Acoes\.objects\.create\([^)]+\)"
        matches = list(re.finditer(acoes_pattern, content, re.DOTALL))

        for match in reversed(matches):
            acoes_create = match.group(0)

            # Se NÃO tem o FK, adicionar
            if fk_name not in acoes_create and "idvigenciapngi" in acoes_create:
                # Determinar valor do FK
                if fk_name == "ideixo":
                    fk_value = "self.eixo"
                elif fk_name == "idsituacaoacao":
                    fk_value = "self.situacao"
                else:
                    continue

                # Adicionar antes do último )
                fixed_acoes = (
                    acoes_create[:-1] + f",\n            {fk_name}={fk_value})"
                )

                # Substituir no conteúdo
                content = (
                    content[: match.start()] + fixed_acoes + content[match.end() :]
                )

        return content

    def _ensure_setup_creates_dependencies(self, content):
        """Garante que setup_test_data cria Eixo e SituacaoAcao"""

        # Se setup_test_data não cria Eixo, adicionar
        if "def setup_test_data(self):" in content:
            # Procurar métodos setup_test_data
            setup_pattern = (
                r"(def setup_test_data\(self\):)(.*?)(?=\n    def |\nclass |\Z)"
            )

            def add_dependencies(match):
                method_def = match.group(1)
                method_body = match.group(2)

                additions = ""

                # Se não cria Eixo, adicionar
                if (
                    "self.eixo" not in method_body
                    and "Eixo.objects.create" not in method_body
                ):
                    additions += """
        # Criar Eixo (se não existe)
        if not hasattr(self, 'eixo') or self.eixo is None:
            self.eixo = Eixo.objects.create(
                stralias='E1',
                strdescricaoeixo='Eixo 1 - Gestão'
            )
"""

                # Se não cria SituacaoAcao, adicionar
                if (
                    "self.situacao" not in method_body
                    and "SituacaoAcao.objects.create" not in method_body
                ):
                    additions += """
        # Criar SituacaoAcao (se não existe)
        if not hasattr(self, 'situacao') or self.situacao is None:
            self.situacao = SituacaoAcao.objects.create(
                strdescricaosituacao='Em Andamento'
            )
"""

                return method_def + additions + method_body

            content = re.sub(setup_pattern, add_dependencies, content, flags=re.DOTALL)

        return content

    # ========================================================================
    # RELATÓRIO FINAL
    # ========================================================================

    def _print_summary(self):
        """Imprime sumário das correções"""
        print("\n📊 SUMÁRIO DAS CORREÇÕES:")
        print("-" * 70)

        categories = {"ValidationError": [], "AttributeError": [], "Fixtures": []}

        for change in self.changes_made:
            if "datfinalvigencia" in change:
                categories["ValidationError"].append(change)
            elif "self.eixo" in change or "self.vigencia" in change:
                categories["AttributeError"].append(change)
            else:
                categories["Fixtures"].append(change)

        for category, changes in categories.items():
            if changes:
                print(f"\n{category} ({len(changes)} arquivos):")
                for change in changes:
                    print(f"  • {change}")

        print("\n" + "=" * 70)
        print("🎉 Script concluído com sucesso!")
        print("\n💡 Próximos passos:")
        print("   1. Rodar os testes novamente: python manage.py test acoes_pngi.tests")
        print("   2. Verificar se os 76 erros foram reduzidos")
        print("   3. Analisar logs para erros restantes")


def main():
    """Função principal"""
    # Obter diretório de testes
    script_dir = Path(__file__).parent
    tests_dir = script_dir

    print("🚀 Fix All Test Errors")
    print("=" * 70)
    print(f"📁 Diretório de testes: {tests_dir}")

    # Executar correções
    fixer = TestErrorFixer(tests_dir)
    fixer.fix_all()


if __name__ == "__main__":
    main()
