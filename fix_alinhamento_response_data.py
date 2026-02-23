#!/usr/bin/env python3
"""
Script - Corrigir response.data['results'] em test_api_views_alinhamento_responsaveis.py

Problema:
- response.data pode ser ReturnList (lista) ou dict
- Código assume que sempre é dict com chave 'results'

Solução:
- Substituir: response.data['results']
- Por: response.data if isinstance(response.data, list) else response.data.get('results', [])
"""

import os
import re

TESTS_DIR = os.path.join(os.path.dirname(__file__), 'acoes_pngi', 'tests')
FILE = 'test_api_views_alinhamento_responsaveis.py'

print("=" * 70)
print("🎯 CORREÇÃO - response.data em alinhamento_responsaveis")
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
# CORREÇÃO: response.data['results'] → verificação de tipo
# ===========================================================================

# Contar ocorrências ANTES
before_count = content.count("response.data['results']")

if before_count > 0:
    # Substituir todas as ocorrências de response.data['results']
    # Para: (response.data if isinstance(response.data, list) else response.data.get('results', []))
    
    content = content.replace(
        "response.data['results']",
        "(response.data if isinstance(response.data, list) else response.data.get('results', []))"
    )
    
    after_count = content.count("response.data['results']")
    fixed = before_count - after_count
    
    print(f"✅ response.data['results']: {before_count} → {after_count} ({fixed} corrigidos)")
else:
    print("⏭️  Nenhuma ocorrência de response.data['results'] encontrada")

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

remaining = final_content.count("response.data['results']")
correct_pattern = "response.data if isinstance(response.data, list) else response.data.get('results', [])"
correct_count = final_content.count(correct_pattern)

if remaining == 0:
    print("✅ Nenhum response.data['results'] remanescente")
    print(f"✅ Padrão correto presente: {correct_count} ocorrências")
else:
    print(f"⚠️  {remaining} response.data['results'] ainda presentes")

print("\n" + "=" * 70)
print("📌 Próximos passos:")
print("   1. Testar: python manage.py test acoes_pngi.tests.test_api_views_alinhamento_responsaveis -v 2")
print("   2. Se OK: git add . && git commit -m 'fix: response.data alinhamento'")
print("=" * 70)
