#!/usr/bin/env python3
"""
Script v3 - Corrigir acesso a response.data (ReturnList vs dict)

Problema:
- response.data pode ser ReturnList (lista direta, sem paginação)
- response.data pode ser OrderedDict (paginado, com 'results')

Solução:
- Verificar tipo antes de acessar
- Se for lista, usar direto
- Se for dict, pegar 'results'
"""

import os
import re

TESTS_DIR = os.path.join(os.path.dirname(__file__), 'acoes_pngi', 'tests')
FILE = 'test_api_acoes_views.py'

print("=" * 70)
print("🎯 CORREÇÃO v3 - response.data (ReturnList vs dict)")
print("=" * 70)

filepath = os.path.join(TESTS_DIR, FILE)

if not os.path.exists(filepath):
    print(f"❌ {FILE} - Arquivo não encontrado")
    exit(1)

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

print(f"\n📝 Processando {FILE}...\n")

# ===========================================================================
# CORREÇÃO: response.data pode ser list OU dict
# ===========================================================================

# Padrão atual (ERRO):
# results = response.data.get('results', [])

# Novo padrão (CORRETO):
# results = response.data if isinstance(response.data, list) else response.data.get('results', [])

before_count = content.count("response.data.get('results', [])")

# Substituir TODAS as ocorrências
content = content.replace(
    "results = response.data.get('results', [])",
    "results = response.data if isinstance(response.data, list) else response.data.get('results', [])"
)

after_count = content.count("response.data.get('results', [])")

if before_count > after_count:
    fixed = before_count - after_count
    print(f"✅ response.data.get('results', []): {before_count} → {after_count} ({fixed} corrigidos)")
else:
    print("⏭️  Nenhuma alteração necessária")

# ===========================================================================
# SALVAR E VERIFICAR
# ===========================================================================

if content != original:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "=" * 70)
    print("🎉 ARQUIVO ATUALIZADO!")
    print("=" * 70)
else:
    print("\n" + "=" * 70)
    print("⏭️  NENHUMA ALTERAÇÃO NECESSÁRIA")
    print("=" * 70)

# Verificar resultado final
with open(filepath, 'r', encoding='utf-8') as f:
    final_content = f.read()

print("\n🔍 Verificação final:\n")

# Contar padrões corretos
correct_pattern = "response.data if isinstance(response.data, list) else response.data.get('results', [])"
correct_count = final_content.count(correct_pattern)

# Contar padrões incorretos remanescentes (isolados)
incorrect_pattern = "results = response.data.get('results', [])"
incorrect_count = final_content.count(incorrect_pattern)

print(f"✅ Padrão correto (isinstance): {correct_count} ocorrências")

if incorrect_count > 0:
    print(f"⚠️  Padrão incorreto remanescente: {incorrect_count} ocorrências")
else:
    print("✅ Nenhum padrão incorreto remanescente")

print("\n" + "=" * 70)
print("📌 Próximos passos:")
print("   1. Testar: python manage.py test acoes_pngi.tests.test_api_acoes_views -v 2")
print("   2. Se OK: git add . && git commit -m 'fix: response.data ReturnList vs dict'")
print("=" * 70)
