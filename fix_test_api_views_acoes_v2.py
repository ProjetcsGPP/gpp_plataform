# fix_test_api_views_acoes_v2.py
import re

filepath = r"C:\Projects\gpp_plataform\acoes_pngi\tests\test_api_views_acoes.py"

print("Lendo arquivo...")
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("Aplicando correções...")

# Corrigir: datiniciovigencia=date(2026, 1, 1)\n            datfinalvigencia=
# Para:     datiniciovigencia=date(2026, 1, 1),\n            datfinalvigencia=
content = content.replace(
    'datiniciovigencia=date(2026, 1, 1)\n            datfinalvigencia=',
    'datiniciovigencia=date(2026, 1, 1),\n            datfinalvigencia='
)

print("Salvando arquivo...")
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ ARQUIVO CORRIGIDO!")
