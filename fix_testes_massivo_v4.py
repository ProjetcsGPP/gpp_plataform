#!/usr/bin/env python3
"""
Script v4 - Correção massiva de testes PNGI

ESTRATÉGIA:
1. Remove COMPLETAMENTE blocos de criação manual de vigencia/eixo/situacao
2. Garante que classes herdam de BaseTestCase/BaseAPITestCase
3. Substitui referências por self.eixo_base/situacao_base/vigencia_base
"""

import os
import re

# Diretório dos testes
TESTS_DIR = os.path.join(os.path.dirname(__file__), 'acoes_pngi', 'tests')

print("=" * 70)
print("🔧 CORREÇÃO MASSIVA DE TESTES PNGI v4")
print("=" * 70)

# Arquivos a serem corrigidos
files_to_fix = [
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

total_fixed = 0

print("\n📝 Removendo blocos de criação manual de fixtures...\n")

for filename in files_to_fix:
    filepath = os.path.join(TESTS_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"⏭️  {filename} - Arquivo não encontrado")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # ==========================================================================
    # 1. REMOVER BLOCOS DE CRIAÇÃO DE VIGÊNCIA
    # ==========================================================================
    
    # Padrão 1: Bloco completo com comentário
    # # Criar vigência
    # # Removido: usar self.eixo_base...
    #     datfinalvigencia=date(2026, 12, 31),
    #     isvigenciaativa=True
    # )
    
    vigencia_patterns = [
        # Padrão com comentário "Removido"
        r'\s*# Criar vigência\s*\n\s*# Removido:[^\n]+\n\s+datfinalvigencia=[^\n]+\n\s+[^\n]*\n\s*\)',
        
        # Padrão sem comentário (linha solta)
        r'\s+datfinalvigencia=date\(\d{4}, \d{1,2}, \d{1,2}\),?\s*\n',
        
        # Padrão de linhas soltas vazias após remoção
        r'\s+isvigenciaativa=True\s*\n\s*\)',
    ]
    
    for pattern in vigencia_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, '', content)
            changes.append("Removido bloco de vigencia")
    
    # ==========================================================================
    # 2. REMOVER COMENTÁRIOS "# Removido: usar self.eixo_base..."
    # ==========================================================================
    
    content = re.sub(r'\s*# Removido: usar self\.eixo_base[^\n]*\n', '', content)
    
    # ==========================================================================
    # 3. REMOVER BLOCOS DE CRIAÇÃO DE EIXO
    # ==========================================================================
    
    eixo_patterns = [
        r'\s*# ✅ Criar Eixo\s*\n\s*# Removido:[^\n]+\n',
        r'\s*self\.eixo = Eixo\.objects\.create\([^)]+\)\s*\n',
    ]
    
    for pattern in eixo_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, '', content)
            changes.append("Removido bloco de eixo")
    
    # ==========================================================================
    # 4. REMOVER BLOCOS DE CRIAÇÃO DE SITUAÇÃO
    # ==========================================================================
    
    situacao_patterns = [
        r'\s*# ✅ Criar Situação\s*\n\s*# Removido:[^\n]+\n',
        r'\s*self\.situacao = SituacaoAcao\.objects\.create\([^)]+\)\s*\n',
    ]
    
    for pattern in situacao_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, '', content)
            changes.append("Removido bloco de situacao")
    
    # ==========================================================================
    # 5. SUBSTITUIR REFERÊNCIAS POR FIXTURES BASE
    # ==========================================================================
    
    # Substituir self.vigencia por self.vigencia_base
    if 'idvigenciapngi=self.vigencia,' in content or 'idvigenciapngi=self.vigencia)' in content:
        content = content.replace('idvigenciapngi=self.vigencia,', 'idvigenciapngi=self.vigencia_base,')
        content = content.replace('idvigenciapngi=self.vigencia)', 'idvigenciapngi=self.vigencia_base)')
        changes.append("Substituiu self.vigencia -> self.vigencia_base")
    
    # Substituir self.eixo por self.eixo_base
    if 'ideixo=self.eixo,' in content or 'ideixo=self.eixo)' in content:
        content = content.replace('ideixo=self.eixo,', 'ideixo=self.eixo_base,')
        content = content.replace('ideixo=self.eixo)', 'ideixo=self.eixo_base)')
        changes.append("Substituiu self.eixo -> self.eixo_base")
    
    # Substituir self.situacao por self.situacao_base
    if 'idsituacaoacao=self.situacao,' in content or 'idsituacaoacao=self.situacao)' in content:
        content = content.replace('idsituacaoacao=self.situacao,', 'idsituacaoacao=self.situacao_base,')
        content = content.replace('idsituacaoacao=self.situacao)', 'idsituacaoacao=self.situacao_base)')
        changes.append("Substituiu self.situacao -> self.situacao_base")
    
    # ==========================================================================
    # 6. LIMPAR LINHAS VAZIAS EXCESSIVAS
    # ==========================================================================
    
    # Reduzir múltiplas linhas vazias para no máximo 2
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # ==========================================================================
    # SALVAR SE HOUVE MUDANÇAS
    # ==========================================================================
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename}")
        if changes:
            print(f"   Mudanças: {', '.join(set(changes))}")
        total_fixed += 1
    else:
        print(f"⏭️  {filename} - Sem alterações")

print(f"\n✅ {total_fixed}/{len(files_to_fix)} arquivos corrigidos")

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("\n" + "=" * 70)
print("🎉 CONCLUÍDO!")
print("=" * 70)
print(f"✅ {total_fixed} arquivos corrigidos")
print("=" * 70)

print("\n📌 Próximos passos:")
print("   1. Testar: python manage.py test acoes_pngi.tests.test_models -v 2")
print("   2. Se OK: python manage.py test acoes_pngi.tests -v 2")
print("   3. Commit: git add . && git commit -m 'fix: v4 - remover fixtures manuais'")
