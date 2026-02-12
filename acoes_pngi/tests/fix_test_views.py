#!/usr/bin/env python3
import os
import re

TESTS_DIR = r'C:\Projects\gpp_plataform\acoes_pngi\tests'
FILE = 'test_views.py'

filepath = os.path.join(TESTS_DIR, FILE)

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Antes: {content.count('self.situacao')} ocorrências de self.situacao")

# Substituir self.situacao → self.situacao_base (apenas palavra inteira)
content = re.sub(r'self\.situacao\b', 'self.situacao_base', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Depois: {content.count('self.situacao')} ocorrências restantes")
print("✅ test_views.py corrigido!")

# Testar
print("\nTestando...")
os.system("python manage.py test acoes_pngi.tests.test_views -v 2")
