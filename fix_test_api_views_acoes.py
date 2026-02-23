# fix_test_api_views_acoes.py
# Corrige erros de sintaxe em test_api_views_acoes.py

import re

filepath = r"C:\Projects\gpp_plataform\acoes_pngi\tests\test_api_views_acoes.py"

print("Lendo arquivo...")
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("Aplicando correções...")
fixes_count = 0

# 1. Corrigir date(2026, 1, 1, -> date(2026, 1, 1)
# Linha 387: datiniciovigencia=date(2026, 1, 1,
pattern1 = r'date\((\d+),\s*(\d+),\s*(\d+),'
replacement1 = r'date(\1, \2, \3)'
new_content = re.sub(pattern1, replacement1, content)
count1 = len(re.findall(pattern1, content))
fixes_count += count1
if count1 > 0:
    print(f"  ✅ Corrigidas {count1} ocorrências de 'date(YYYY, MM, DD,'")

# 2. Corrigir datfinalvigencia=date(2026, 12, 31)), -> date(2026, 12, 31)
# Linha 388: datfinalvigencia=date(2026, 12, 31)),
pattern2 = r'date\((\d+),\s*(\d+),\s*(\d+)\)\)\,'
replacement2 = r'date(\1, \2, \3),'
new_content = re.sub(pattern2, replacement2, new_content)
count2 = len(re.findall(pattern2, content))
fixes_count += count2
if count2 > 0:
    print(f"  ✅ Corrigidas {count2} ocorrências de 'date(YYYY, MM, DD)),'")

# 3. Remover linhas em branco duplicadas após correções
new_content = re.sub(r'\n\s*\n\s*\n', '\n\n', new_content)

content = new_content

print(f"\nSalvando arquivo... (Total de {fixes_count} correções)")
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ ARQUIVO CORRIGIDO COM SUCESSO!")
print(f"   Total de correções aplicadas: {fixes_count}")
