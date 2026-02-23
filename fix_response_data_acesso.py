#!/usr/bin/env python3
"""
Script FOCADO - Corrigir 2 problemas em test_api_acoes_views.py:

1. Linha 162: Adicionar datfinalvigencia ao criar vigencia2
2. Todas as linhas: Corrigir acesso a response.data['results']

Problema identificado:
- getattr(response.data, 'results', []) NÃO funciona para dict
- Deve usar: response.data.get('results', []) ou verificar tipo
"""

import os
import re

TESTS_DIR = os.path.join(os.path.dirname(__file__), 'acoes_pngi', 'tests')
FILE = 'test_api_acoes_views.py'

print("=" * 70)
print("🎯 CORREÇÃO - response.data e datfinalvigencia")
print("=" * 70)

filepath = os.path.join(TESTS_DIR, FILE)

if not os.path.exists(filepath):
    print(f"❌ {FILE} - Arquivo não encontrado")
    exit(1)

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content
changes = []

print(f"\n📝 Processando {FILE}...\n")

# ===========================================================================
# CORREÇÃO 1: Adicionar datfinalvigencia na linha 162
# ===========================================================================

# Procurar o padrão específico da criação de vigencia2
pattern_vigencia = r"(vigencia2 = VigenciaPNGI\.objects\.create\(\s+strdescricaovigenciapngi='PNGI 2027',\s+datiniciovigencia=date\(2027, 1, 1\),)\s+\)"

replacement_vigencia = r"\1\n            datfinalvigencia=date(2027, 12, 31)\n        )"

if re.search(pattern_vigencia, content):
    content = re.sub(pattern_vigencia, replacement_vigencia, content)
    print("✅ Linha 162: Adicionado datfinalvigencia=date(2027, 12, 31)")
    changes.append("datfinalvigencia")
else:
    print("⏭️  Linha 162: Já corrigida ou padrão não encontrado")

# ===========================================================================
# CORREÇÃO 2: Corrigir acesso a response.data['results']
# ===========================================================================

# Contar ocorrências ANTES
before_getattr = content.count("getattr(response.data, 'results', [])")

# Substituir getattr por get (para dicts)
# getattr(response.data, 'results', []) → response.data.get('results', [])
content = content.replace(
    "getattr(response.data, 'results', [])",
    "response.data.get('results', [])"
)

# Contar ocorrências DEPOIS
after_getattr = content.count("getattr(response.data, 'results', [])")

if before_getattr > after_getattr:
    fixed = before_getattr - after_getattr
    print(f"✅ getattr(response.data, 'results', []): {before_getattr} → {after_getattr} ({fixed} corrigidos)")
    changes.append(f"getattr: {fixed}")
else:
    print("⏭️  getattr: Nenhuma alteração necessária")

# ===========================================================================
# SALVAR E VERIFICAR
# ===========================================================================

if content != original:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "=" * 70)
    print("🎉 ARQUIVO ATUALIZADO!")
    print("=" * 70)
    print(f"✅ Alterações aplicadas: {', '.join(changes)}")
    print("=" * 70)
else:
    print("\n" + "=" * 70)
    print("⏭️  NENHUMA ALTERAÇÃO NECESSÁRIA")
    print("=" * 70)

# Verificar resultado final
with open(filepath, 'r', encoding='utf-8') as f:
    final_content = f.read()

print("\n🔍 Verificação final:\n")

remaining_getattr = final_content.count("getattr(response.data, 'results', [])")
has_datfinalvigencia = 'datfinalvigencia=date(2027, 12, 31)' in final_content

if remaining_getattr == 0:
    print("✅ Nenhum getattr(response.data, 'results') remanescente")
else:
    print(f"⚠️  {remaining_getattr} getattr(response.data, 'results') ainda presentes")

if has_datfinalvigencia:
    print("✅ datfinalvigencia presente em vigencia2")
else:
    print("⚠️  datfinalvigencia NÃO encontrado em vigencia2")

print("\n" + "=" * 70)
print("📌 Próximos passos:")
print("   1. Testar: python manage.py test acoes_pngi.tests.test_api_acoes_views -v 2")
print("   2. Se OK: git add . && git commit -m 'fix: corrigir response.data e vigencia'")
print("=" * 70)
