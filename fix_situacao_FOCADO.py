#!/usr/bin/env python3
"""
Script FOCADO - Corrigir APENAS AttributeError: 'situacao' (58 erros)

Arquivos alvo:
- test_api_acoes_views.py (27 erros)
- test_api_alinhamento_views.py (17 erros)  
- test_api_responsavel_views.py (14 erros)

Estratégia:
1. Substituir self.situacao → self.situacao_base
2. Substituir self.vigencia → self.vigencia_base
3. Substituir self.eixo → self.eixo_base
"""

import os
import re

TESTS_DIR = os.path.join(os.path.dirname(__file__), 'acoes_pngi', 'tests')

print("=" * 70)
print("🎯 CORREÇÃO FOCADA - AttributeError: 'situacao' (58 erros)")
print("=" * 70)

def fix_attribute_errors(filepath, filename):
    """
    Substitui referências incorretas de fixtures em um arquivo
    """
    if not os.path.exists(filepath):
        print(f"❌ {filename} - Arquivo não encontrado")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # Contar ocorrências ANTES
    before_situacao = len(re.findall(r'idsituacaoacao=self\.situacao[,\)]', content))
    before_vigencia = len(re.findall(r'idvigenciapngi=self\.vigencia[,\)]', content))
    before_eixo = len(re.findall(r'ideixo=self\.eixo[,\)]', content))
    
    # Substituir self.situacao → self.situacao_base
    content = re.sub(
        r'idsituacaoacao=self\.situacao([,\)])',
        r'idsituacaoacao=self.situacao_base\1',
        content
    )
    
    # Substituir self.vigencia → self.vigencia_base
    content = re.sub(
        r'idvigenciapngi=self\.vigencia([,\)])',
        r'idvigenciapngi=self.vigencia_base\1',
        content
    )
    
    # Substituir self.eixo → self.eixo_base
    content = re.sub(
        r'ideixo=self\.eixo([,\)])',
        r'ideixo=self.eixo_base\1',
        content
    )
    
    # Contar ocorrências DEPOIS
    after_situacao = len(re.findall(r'idsituacaoacao=self\.situacao[,\)]', content))
    after_vigencia = len(re.findall(r'idvigenciapngi=self\.vigencia[,\)]', content))
    after_eixo = len(re.findall(r'ideixo=self\.eixo[,\)]', content))
    
    # Verificar se houve mudanças
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filename}")
        
        if before_situacao > after_situacao:
            fixed = before_situacao - after_situacao
            print(f"   ✓ self.situacao: {before_situacao} → {after_situacao} ({fixed} corrigidos)")
            changes.append(f"situacao: {fixed}")
        
        if before_vigencia > after_vigencia:
            fixed = before_vigencia - after_vigencia
            print(f"   ✓ self.vigencia: {before_vigencia} → {after_vigencia} ({fixed} corrigidos)")
            changes.append(f"vigencia: {fixed}")
        
        if before_eixo > after_eixo:
            fixed = before_eixo - after_eixo
            print(f"   ✓ self.eixo: {before_eixo} → {after_eixo} ({fixed} corrigidos)")
            changes.append(f"eixo: {fixed}")
        
        return True
    else:
        print(f"⏭️  {filename} - Nenhuma alteração necessária")
        return False

# ===========================================================================
# PROCESSAR OS 3 ARQUIVOS
# ===========================================================================

print("\n📝 Processando arquivos...\n")

files_to_fix = [
    'test_api_acoes_views.py',
    'test_api_alinhamento_views.py',
    'test_api_responsavel_views.py',
]

fixed_count = 0
for filename in files_to_fix:
    filepath = os.path.join(TESTS_DIR, filename)
    if fix_attribute_errors(filepath, filename):
        fixed_count += 1

# ===========================================================================
# VERIFICAÇÃO FINAL
# ===========================================================================

print("\n🔍 Verificação final...\n")

total_remaining = 0
for filename in files_to_fix:
    filepath = os.path.join(TESTS_DIR, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    remaining_situacao = len(re.findall(r'idsituacaoacao=self\.situacao[,\)]', content))
    remaining_vigencia = len(re.findall(r'idvigenciapngi=self\.vigencia[,\)]', content))
    remaining_eixo = len(re.findall(r'ideixo=self\.eixo[,\)]', content))
    
    if remaining_situacao > 0 or remaining_vigencia > 0 or remaining_eixo > 0:
        print(f"⚠️  {filename}:")
        if remaining_situacao > 0:
            print(f"   - self.situacao: {remaining_situacao} restantes")
            total_remaining += remaining_situacao
        if remaining_vigencia > 0:
            print(f"   - self.vigencia: {remaining_vigencia} restantes")
            total_remaining += remaining_vigencia
        if remaining_eixo > 0:
            print(f"   - self.eixo: {remaining_eixo} restantes")
            total_remaining += remaining_eixo
    else:
        print(f"✅ {filename} - LIMPO!")

# ===========================================================================
# RESUMO FINAL
# ===========================================================================

print("\n" + "=" * 70)
print("🎉 CONCLUÍDO!")
print("=" * 70)
print(f"✅ {fixed_count}/{len(files_to_fix)} arquivos corrigidos")
if total_remaining == 0:
    print("✅ NENHUM problema remanescente!")
else:
    print(f"⚠️  {total_remaining} problemas remanescentes")
print("=" * 70)

print("\n📌 Próximos passos:")
print("   1. Testar: python manage.py test acoes_pngi.tests.test_api_acoes_views -v 2")
print("   2. Testar: python manage.py test acoes_pngi.tests.test_api_alinhamento_views -v 2")
print("   3. Testar: python manage.py test acoes_pngi.tests.test_api_responsavel_views -v 2")
print("   4. Se OK: git add . && git commit -m 'fix: corrigir AttributeError situacao (58 erros)'")
