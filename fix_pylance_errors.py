#!/usr/bin/env python3
"""
Script - Corrigir erros identificados pelo Pylance

1. test_api_views_alinhamento_responsaveis.py:
   - Linhas 329-330: eixo → self.eixo_base, situacao → self.situacao_base
   - Linhas 700-701: Mesmo problema

2. test_views.py:
   - Linha 37: Adicionar import BaseTestCase
"""

import os
import re

TESTS_DIR = os.path.join(os.path.dirname(__file__), 'acoes_pngi', 'tests')

print("=" * 70)
print("🐞 CORREÇÃO - Erros Pylance")
print("=" * 70)

# ===========================================================================
# ARQUIVO 1: test_api_views_alinhamento_responsaveis.py
# ===========================================================================

file1 = 'test_api_views_alinhamento_responsaveis.py'
filepath1 = os.path.join(TESTS_DIR, file1)

if os.path.exists(filepath1):
    print(f"\n📝 Processando {file1}...\n")
    
    with open(filepath1, 'r', encoding='utf-8') as f:
        content1 = f.read()
    
    original1 = content1
    
    # Substituir variáveis não definidas por self.xxx_base
    # Usar word boundaries para evitar substituir dentro de outras palavras
    
    # Contar antes
    before_eixo = len(re.findall(r'\beixo\b(?!_base)', content1))
    before_situacao = len(re.findall(r'\bsituacao\b(?!_base|acao)', content1))
    before_vigencia = len(re.findall(r'\bvigencia\b(?!_base)', content1))
    
    # Substituir ideixo=eixo → ideixo=self.eixo_base
    content1 = re.sub(r'ideixo=eixo\b', 'ideixo=self.eixo_base', content1)
    
    # Substituir idsituacaoacao=situacao → idsituacaoacao=self.situacao_base
    content1 = re.sub(r'idsituacaoacao=situacao\b', 'idsituacaoacao=self.situacao_base', content1)
    
    # Substituir idvigenciapngi=vigencia → idvigenciapngi=self.vigencia_base
    content1 = re.sub(r'idvigenciapngi=vigencia\b', 'idvigenciapngi=self.vigencia_base', content1)
    
    # Contar depois
    after_eixo = len(re.findall(r'\beixo\b(?!_base)', content1))
    after_situacao = len(re.findall(r'\bsituacao\b(?!_base|acao)', content1))
    after_vigencia = len(re.findall(r'\bvigencia\b(?!_base)', content1))
    
    if content1 != original1:
        with open(filepath1, 'w', encoding='utf-8') as f:
            f.write(content1)
        
        print(f"✅ {file1} corrigido:")
        if before_eixo > after_eixo:
            print(f"   ✓ eixo: {before_eixo} → {after_eixo} ({before_eixo - after_eixo} corrigidos)")
        if before_situacao > after_situacao:
            print(f"   ✓ situacao: {before_situacao} → {after_situacao} ({before_situacao - after_situacao} corrigidos)")
        if before_vigencia > after_vigencia:
            print(f"   ✓ vigencia: {before_vigencia} → {after_vigencia} ({before_vigencia - after_vigencia} corrigidos)")
    else:
        print(f"⏭️  {file1} - Já está correto")
else:
    print(f"❌ {file1} - Não encontrado")

# ===========================================================================
# ARQUIVO 2: test_views.py
# ===========================================================================

file2 = 'test_views.py'
filepath2 = os.path.join(TESTS_DIR, file2)

if os.path.exists(filepath2):
    print(f"\n📝 Processando {file2}...\n")
    
    with open(filepath2, 'r', encoding='utf-8') as f:
        content2 = f.read()
    
    original2 = content2
    
    # Verificar se BaseTestCase já está importado
    has_import = 'from .base import BaseTestCase' in content2
    
    if not has_import:
        # Procurar linha de imports (geralmente após docstring)
        # Adicionar import após "from django.test import TestCase"
        
        # Procurar padrão: from django.test import ...
        import_pattern = r'(from django\.test import [^\n]+\n)'
        
        if re.search(import_pattern, content2):
            # Adicionar import após imports do Django
            content2 = re.sub(
                import_pattern,
                r'\1from .base import BaseTestCase\n',
                content2,
                count=1
            )
            print(f"✅ {file2} corrigido:")
            print(f"   ✓ Import BaseTestCase adicionado")
        else:
            print(f"⚠️  {file2} - Padrão de import não encontrado")
    else:
        print(f"⏭️  {file2} - Import já existe")
    
    if content2 != original2:
        with open(filepath2, 'w', encoding='utf-8') as f:
            f.write(content2)
else:
    print(f"❌ {file2} - Não encontrado")

# ===========================================================================
# VERIFICAÇÃO FINAL
# ===========================================================================

print("\n" + "=" * 70)
print("🔍 Verificação final")
print("=" * 70)

# Verificar arquivo 1
if os.path.exists(filepath1):
    with open(filepath1, 'r', encoding='utf-8') as f:
        final1 = f.read()
    
    remaining_eixo = len(re.findall(r'ideixo=eixo\b', final1))
    remaining_situacao = len(re.findall(r'idsituacaoacao=situacao\b', final1))
    remaining_vigencia = len(re.findall(r'idvigenciapngi=vigencia\b', final1))
    
    print(f"\n{file1}:")
    if remaining_eixo == 0 and remaining_situacao == 0 and remaining_vigencia == 0:
        print("✅ Todos os problemas corrigidos!")
    else:
        if remaining_eixo > 0:
            print(f"⚠️  ideixo=eixo: {remaining_eixo} restantes")
        if remaining_situacao > 0:
            print(f"⚠️  idsituacaoacao=situacao: {remaining_situacao} restantes")
        if remaining_vigencia > 0:
            print(f"⚠️  idvigenciapngi=vigencia: {remaining_vigencia} restantes")

# Verificar arquivo 2
if os.path.exists(filepath2):
    with open(filepath2, 'r', encoding='utf-8') as f:
        final2 = f.read()
    
    has_import = 'from .base import BaseTestCase' in final2
    
    print(f"\n{file2}:")
    if has_import:
        print("✅ Import BaseTestCase presente!")
    else:
        print("⚠️  Import BaseTestCase ainda faltando")

print("\n" + "=" * 70)
print("📌 Próximos passos:")
print("   1. Verificar VSCode - Erros Pylance devem sumir")
print("   2. Testar: python manage.py test acoes_pngi.tests.test_api_views_alinhamento_responsaveis -v 2")
print("   3. Testar: python manage.py test acoes_pngi.tests.test_views -v 2")
print("=" * 70)
