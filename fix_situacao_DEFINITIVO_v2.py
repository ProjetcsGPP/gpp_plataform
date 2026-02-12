#!/usr/bin/env python3
"""
Script DEFINITIVO v2 - Corrigir TODOS os AttributeError

Problema identificado:
- Linhas 83, 286, 420: idsituacaoacao=self.situacao
- O script anterior só procurava dentro de parâmetros
- Agora busca QUALQUER referência isolada

Estratégia NOVA:
1. Substituir self.situacao → self.situacao_base (QUALQUER contexto)
2. Substituir self.vigencia → self.vigencia_base (QUALQUER contexto)
3. Substituir self.eixo → self.eixo_base (QUALQUER contexto)
4. MAS preservar self.situacao_base, self.vigencia_base, self.eixo_base
"""

import os
import re

TESTS_DIR = os.path.join(os.path.dirname(__file__), 'acoes_pngi', 'tests')

print("=" * 70)
print("🎯 CORREÇÃO DEFINITIVA v2 - Substituir TODAS as referências")
print("=" * 70)

def fix_all_references(filepath, filename):
    """
    Substitui TODAS as referências de self.situacao/vigencia/eixo
    """
    if not os.path.exists(filepath):
        print(f"❌ {filename} - Arquivo não encontrado")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # Contar ocorrências ANTES (excluindo já corretos _base)
    before_situacao = len(re.findall(r'self\.situacao(?!_base|acao)', content))
    before_vigencia = len(re.findall(r'self\.vigencia(?!_base)', content))
    before_eixo = len(re.findall(r'self\.eixo(?!_base)', content))
    
    # Substituir self.situacao → self.situacao_base
    # (?!_base) = negative lookahead para não substituir self.situacao_base
    # (?!acao) = negative lookahead para não substituir self.situacaoacao  
    content = re.sub(
        r'\bself\.situacao\b(?!_base|acao)',
        'self.situacao_base',
        content
    )
    
    # Substituir self.vigencia → self.vigencia_base
    content = re.sub(
        r'\bself\.vigencia\b(?!_base)',
        'self.vigencia_base',
        content
    )
    
    # Substituir self.eixo → self.eixo_base
    content = re.sub(
        r'\bself\.eixo\b(?!_base)',
        'self.eixo_base',
        content
    )
    
    # Contar ocorrências DEPOIS
    after_situacao = len(re.findall(r'self\.situacao(?!_base|acao)', content))
    after_vigencia = len(re.findall(r'self\.vigencia(?!_base)', content))
    after_eixo = len(re.findall(r'self\.eixo(?!_base)', content))
    
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
    if fix_all_references(filepath, filename):
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
    
    remaining_situacao = len(re.findall(r'self\.situacao(?!_base|acao)', content))
    remaining_vigencia = len(re.findall(r'self\.vigencia(?!_base)', content))
    remaining_eixo = len(re.findall(r'self\.eixo(?!_base)', content))
    
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
print("   2. Se OK, commit: git add . && git commit -m 'fix: corrigir AttributeError (58 erros)'")
