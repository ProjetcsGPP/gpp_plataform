#!/usr/bin/env python3
"""
Script v3 - Correção massiva de testes PNGI

Correções aplicadas:
1. Remove indentação incorreta em VigenciaPNGI.objects.create()
2. Remove import de RequestFactory (não existe em base.py)
3. Converte test_api_views_alinhamento_responsaveis.py para usar BaseAPITestCase
"""

import os
import re

# Diretório dos testes
TESTS_DIR = os.path.join(os.path.dirname(__file__), 'acoes_pngi', 'tests')

print("=" * 70)
print("🔧 CORREÇÃO MASSIVA DE TESTES PNGI v3")
print("=" * 70)

# ============================================================================
# 1. CORRIGIR INDENTAÇÃO EM VigenciaPNGI.objects.create()
# ============================================================================

indentation_files = [
    'test_api_acoes_views.py',
    'test_api_alinhamento_views.py',
    'test_api_responsavel_views.py',
    'test_api_views.py',
    'test_api_views_acoes.py',
    'test_diagnostic_api.py',
    'test_diagnostic_simple.py',
    'test_views.py',
    'test_web_acoes_views.py',
    'test_web_views_complete.py',
]

total_indent_fixed = 0

print("\n📝 Corrigindo indentação em VigenciaPNGI.objects.create()...\n")

for filename in indentation_files:
    filepath = os.path.join(TESTS_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"⏭️  {filename} - Arquivo não encontrado")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Padrão: linha com datfinalvigencia com indentação incorreta
    # ANTES:
    #     strdescricaovigencia='PNGI 2026',
    #             datfinalvigencia=date(2026, 12, 31),
    # DEPOIS:
    #     strdescricaovigencia='PNGI 2026',
    #     datfinalvigencia=date(2026, 12, 31),
    
    # Regex para encontrar linhas com indentação excessiva em datfinalvigencia
    pattern = r'(\s+strdescricaovigencia=[^\n]+\n)\s{12,}(datfinalvigencia=date\([^\)]+\),?)'
    
    def fix_indentation(match):
        line1 = match.group(1)
        line2 = match.group(2)
        # Extrair a indentação correta da primeira linha
        indent = re.match(r'(\s+)', line1).group(1)
        return f"{line1}{indent}{line2}"
    
    content = re.sub(pattern, fix_indentation, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename} - Indentação corrigida")
        total_indent_fixed += 1
    else:
        print(f"⏭️  {filename} - Sem alterações")

print(f"\n✅ {total_indent_fixed}/{len(indentation_files)} arquivos com indentação corrigida")

# ============================================================================
# 2. REMOVER IMPORT RequestFactory
# ============================================================================

requestfactory_files = [
    'test_context_processors.py',
    'test_permissions.py',
]

total_rf_fixed = 0

print("\n📝 Removendo import de RequestFactory...\n")

for filename in requestfactory_files:
    filepath = os.path.join(TESTS_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"⏭️  {filename} - Arquivo não encontrado")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remover RequestFactory do import
    # ANTES: from .base import BaseTestCase, BaseAPITestCase, RequestFactory
    # DEPOIS: from .base import BaseTestCase, BaseAPITestCase
    content = re.sub(
        r'from \.base import (.*), RequestFactory',
        r'from .base import \1',
        content
    )
    
    # Adicionar import do RequestFactory do Django se necessário
    if 'RequestFactory' in content and 'from django.test import RequestFactory' not in content:
        # Adicionar após os imports de django.test
        content = re.sub(
            r'(from django\.test import [^\n]+)',
            r'\1, RequestFactory',
            content,
            count=1
        )
        # Se não encontrou, adicionar nova linha
        if 'from django.test import' not in content or 'RequestFactory' not in content.split('from django.test import')[1].split('\n')[0]:
            content = re.sub(
                r'(from django\.test import TestCase)',
                r'\1\nfrom django.test import RequestFactory',
                content,
                count=1
            )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename} - RequestFactory corrigido")
        total_rf_fixed += 1
    else:
        print(f"⏭️  {filename} - Sem alterações")

print(f"\n✅ {total_rf_fixed}/{len(requestfactory_files)} arquivos com RequestFactory corrigido")

# ============================================================================
# 3. CONVERTER test_api_views_alinhamento_responsaveis.py para BaseAPITestCase
# ============================================================================

print("\n📝 Convertendo test_api_views_alinhamento_responsaveis.py...\n")

alinhamento_file = os.path.join(TESTS_DIR, 'test_api_views_alinhamento_responsaveis.py')

if os.path.exists(alinhamento_file):
    with open(alinhamento_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # 1. Mudar herança para BaseAPITestCase
    if 'class TipoAnotacaoAlinhamentoAPITests(APITestCase):' in content:
        content = content.replace(
            'class TipoAnotacaoAlinhamentoAPITests(APITestCase):',
            'class TipoAnotacaoAlinhamentoAPITests(BaseAPITestCase):'
        )
        changes.append("Herda de BaseAPITestCase")
    
    if 'class UsuarioResponsavelAPITests(APITestCase):' in content:
        content = content.replace(
            'class UsuarioResponsavelAPITests(APITestCase):',
            'class UsuarioResponsavelAPITests(BaseAPITestCase):'
        )
        changes.append("Herda de BaseAPITestCase")
    
    if 'class AcaoAnotacaoAlinhamentoAPITests(APITestCase):' in content:
        content = content.replace(
            'class AcaoAnotacaoAlinhamentoAPITests(APITestCase):',
            'class AcaoAnotacaoAlinhamentoAPITests(BaseAPITestCase):'
        )
        changes.append("Herda de BaseAPITestCase")
    
    if 'class RelacaoAcaoUsuarioResponsavelAPITests(APITestCase):' in content:
        content = content.replace(
            'class RelacaoAcaoUsuarioResponsavelAPITests(APITestCase):',
            'class RelacaoAcaoUsuarioResponsavelAPITests(BaseAPITestCase):'
        )
        changes.append("Herda de BaseAPITestCase")
    
    # 2. Remover setup_test_data() e usar fixtures base
    # Substituir chamadas de criação manual por uso de self.eixo_base, etc
    
    # Padrão para encontrar setup_test_data
    if 'def setup_test_data(cls):' in content:
        # Remover todo o método setup_test_data
        content = re.sub(
            r'    @classmethod\s+def setup_test_data\(cls\):.*?(?=\n    @classmethod|\n    def [^s]|\nclass |\Z)',
            '',
            content,
            flags=re.DOTALL
        )
        changes.append("Removido setup_test_data()")
    
    # 3. Substituir self.eixo por self.eixo_base
    content = content.replace('self.eixo', 'self.eixo_base')
    content = content.replace('cls.eixo', 'cls.eixo_base')
    
    # 4. Substituir self.situacao por self.situacao_base
    content = content.replace('self.situacao', 'self.situacao_base')
    content = content.replace('cls.situacao', 'cls.situacao_base')
    
    # 5. Substituir self.vigencia por self.vigencia_base
    content = content.replace('self.vigencia', 'self.vigencia_base')
    content = content.replace('cls.vigencia', 'cls.vigencia_base')
    
    # 6. Remover criação manual de Eixo, SituacaoAcao, VigenciaPNGI
    patterns_to_remove = [
        r'eixo = Eixo\.objects\.create\([^)]+\)\s*',
        r'situacao = SituacaoAcao\.objects\.create\([^)]+\)\s*',
        r'vigencia = VigenciaPNGI\.objects\.create\([^)]+\)\s*',
        r'cls\.eixo = Eixo\.objects\.create\([^)]+\)\s*',
        r'cls\.situacao = SituacaoAcao\.objects\.create\([^)]+\)\s*',
        r'cls\.vigencia = VigenciaPNGI\.objects\.create\([^)]+\)\s*',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content)
    
    # 7. Remover import de APITestCase
    content = re.sub(r'from rest_framework\.test import APITestCase\n', '', content)
    
    # 8. Garantir import de BaseAPITestCase
    if 'from .base import BaseAPITestCase' not in content:
        # Adicionar após outros imports de .base ou no início dos imports locais
        if 'from .base import' in content:
            content = re.sub(
                r'from \.base import ([^\n]+)',
                r'from .base import \1, BaseAPITestCase',
                content,
                count=1
            )
        else:
            # Adicionar nova linha após imports do Django
            content = re.sub(
                r'(from django[^\n]+\n)',
                r'\1from .base import BaseAPITestCase\n',
                content,
                count=1
            )
    
    if content != original_content:
        with open(alinhamento_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ test_api_views_alinhamento_responsaveis.py convertido!")
        print(f"   Mudanças: {', '.join(changes)}")
    else:
        print(f"⏭️  test_api_views_alinhamento_responsaveis.py - Sem alterações")

else:
    print(f"⚠️  test_api_views_alinhamento_responsaveis.py não encontrado")

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("\n" + "=" * 70)
print("🎉 CONCLUÍDO!")
print("=" * 70)
print(f"✅ Indentação: {total_indent_fixed} arquivos corrigidos")
print(f"✅ RequestFactory: {total_rf_fixed} arquivos corrigidos")
print(f"✅ test_api_views_alinhamento_responsaveis.py: convertido para BaseAPITestCase")
print("=" * 70)

print("\n📌 Próximos passos:")
print("   1. Testar: python manage.py test acoes_pngi.tests -v 2")
print("   2. Commit: git add . && git commit -m 'fix: v3 - indentação + RequestFactory + fixtures'")
print("   3. Push: git push origin fix/correcao-massiva-testes-pngi")
