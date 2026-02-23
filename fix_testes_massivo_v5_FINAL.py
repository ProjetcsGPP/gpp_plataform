#!/usr/bin/env python3
"""
Script v5 FINAL - Correção DEFINITIVA de todos os testes PNGI

CORREÇÕES:
1. Remove blocos de criação manual (vigencia/eixo/situacao)
2. Substitui referências por fixtures base
3. Corrige erros de sintaxe (parênteses, strings, indentação)
4. Corrige imports incorretos
5. Limpa código duplicado
"""

import os
import re

TESTS_DIR = os.path.join(os.path.dirname(__file__), 'acoes_pngi', 'tests')

print("=" * 70)
print("🔧 CORREÇÃO FINAL MASSIVA DE TESTES PNGI v5")
print("=" * 70)

# ===========================================================================
# DICIONÁRIO DE CORREÇÕES ESPECÍFICAS POR ARQUIVO
# ===========================================================================

SPECIFIC_FIXES = {
    'test_api_views.py': [
        # Remover bloco de vigência quebrado
        (r'        # Criar vigência\s*\n\s*self\.vigencia = VigenciaPNGI\.objects\.create\([^)]*$', ''),
        # Adicionar self.vigencia_base se não existir
    ],
    
    'test_api_views_acoes.py': [
        # Remover linha solta de dataentrega
        (r'\s*datdataentrega=timezone\.now\(\) \+ timedelta\(days=30\)\s*\n', ''),
        # Corrigir indentação linha 301
        (r'(\s+)# Criar ação para teste\s*\n\s+# Removido:', r'\1# Criar ação para teste'),
    ],
    
    'test_diagnostic_api.py': [
        # Remover import desnecessário
        (r'from django\.test import RequestFactory\s*\n', ''),
    ],
}

# ===========================================================================
# PADRÕES GLOBAIS DE CORREÇÃO
# ===========================================================================

GLOBAL_PATTERNS = [
    # 1. Remover comentários "Removido:"
    (r'\s*# Removido:[^\n]*\n', ''),
    
    # 2. Remover blocos de vigência quebrados
    (r'\s*# Criar vigência\s*\n\s*self\.vigencia = VigenciaPNGI\.objects\.create\(\s*\n[^)]*\)', ''),
    
    # 3. Remover linhas soltas de datfinalvigencia
    (r'\s*datfinalvigencia=date\(\d{4}, \d{1,2}, \d{1,2}\),?\s*\n', ''),
    (r'\s*isvigenciaativa=True\s*\n\s*\)', ''),
    
    # 4. Remover blocos de eixo
    (r'\s*# ✅ Criar Eixo\s*\n', ''),
    (r'\s*self\.eixo = Eixo\.objects\.create\([^)]+\)\s*\n', ''),
    
    # 5. Remover blocos de situação
    (r'\s*# ✅ Criar Situação\s*\n', ''),
    (r'\s*self\.situacao = SituacaoAcao\.objects\.create\([^)]+\)\s*\n', ''),
    
    # 6. Substituir referências
    (r'idvigenciapngi=self\.vigencia([,\)])', r'idvigenciapngi=self.vigencia_base\1'),
    (r'ideixo=self\.eixo([,\)])', r'ideixo=self.eixo_base\1'),
    (r'idsituacaoacao=self\.situacao([,\)])', r'idsituacaoacao=self.situacao_base\1'),
    
    # 7. Limpar linhas vazias excessivas
    (r'\n{4,}', '\n\n\n'),
]

# ===========================================================================
# FUNÇÃO PRINCIPAL DE CORREÇÃO
# ===========================================================================

def fix_file(filepath, filename):
    """Corrige um arquivo de teste"""
    
    if not os.path.exists(filepath):
        print(f"⏭️  {filename} - Não encontrado")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # Aplicar correções específicas primeiro
    if filename in SPECIFIC_FIXES:
        for pattern, replacement in SPECIFIC_FIXES[filename]:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes.append(f"Fix específico aplicado")
    
    # Aplicar padrões globais
    for pattern, replacement in GLOBAL_PATTERNS:
        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, replacement, content)
            changes.append(f"Padrão global ({matches}x)")
    
    # Salvar se houve mudanças
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename}")
        if changes:
            print(f"   Mudanças: {len(changes)} padrões aplicados")
        return True
    else:
        print(f"⏭️  {filename} - Sem alterações")
        return False

# ===========================================================================
# PROCESSAR TODOS OS ARQUIVOS
# ===========================================================================

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

print("\n📝 Processando arquivos...\n")

total_fixed = 0
for filename in files_to_fix:
    filepath = os.path.join(TESTS_DIR, filename)
    if fix_file(filepath, filename):
        total_fixed += 1

# ===========================================================================
# CORREÇÕES MANUAIS ADICIONAIS
# ===========================================================================

print("\n📝 Aplicando correções manuais adicionais...\n")

# Corrigir test_api_views.py - Adicionar self.vigencia_base
test_api_views_path = os.path.join(TESTS_DIR, 'test_api_views.py')
if os.path.exists(test_api_views_path):
    with open(test_api_views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se setUp existe sem self.vigencia_base
    if 'def setUp(self):' in content and 'self.vigencia_base' not in content:
        # Adicionar após self.client.force_authenticate
        content = content.replace(
            'self.client.force_authenticate(user=self.user)',
            'self.client.force_authenticate(user=self.user)\n        \n        # Usar fixtures base do BaseTestCase\n        # self.vigencia_base, self.eixo_base, self.situacao_base já existem'
        )
        
        with open(test_api_views_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ test_api_views.py - Comentário de fixtures adicionado")

# Corrigir test_api_views_acoes.py - Remover datdataentrega solta
test_api_views_acoes_path = os.path.join(TESTS_DIR, 'test_api_views_acoes.py')
if os.path.exists(test_api_views_acoes_path):
    with open(test_api_views_acoes_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remover linha solta de datdataentrega
    content = re.sub(r'\s*datdataentrega=timezone\.now\(\) \+ timedelta\(days=30\)\s*\n\s*\)', ')', content)
    
    with open(test_api_views_acoes_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ test_api_views_acoes.py - Linha solta removida")

# ===========================================================================
# VERIFICAÇÃO FINAL - BUSCAR PROBLEMAS REMANESCENTES
# ===========================================================================

print("\n🔍 Verificando problemas remanescentes...\n")

issues_found = {}
for filename in files_to_fix:
    filepath = os.path.join(TESTS_DIR, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    problems = []
    
    # Verificar self.vigencia (sem _base)
    if re.search(r'idvigenciapngi=self\.vigencia[,\)]', content):
        problems.append("self.vigencia encontrado (deve ser vigencia_base)")
    
    # Verificar self.eixo (sem _base)
    if re.search(r'ideixo=self\.eixo[,\)]', content):
        problems.append("self.eixo encontrado (deve ser eixo_base)")
    
    # Verificar self.situacao (sem _base)
    if re.search(r'idsituacaoacao=self\.situacao[,\)]', content):
        problems.append("self.situacao encontrado (deve ser situacao_base)")
    
    # Verificar comentários "Removido:"
    if '# Removido:' in content:
        problems.append("Comentários 'Removido:' ainda presentes")
    
    # Verificar linhas soltas
    if re.search(r'^\s*datfinalvigencia=', content, re.MULTILINE):
        problems.append("Linha solta de datfinalvigencia")
    
    if problems:
        issues_found[filename] = problems

if issues_found:
    print("⚠️  Problemas encontrados:\n")
    for filename, problems in issues_found.items():
        print(f"   {filename}:")
        for problem in problems:
            print(f"      - {problem}")
else:
    print("✅ Nenhum problema encontrado!")

# ===========================================================================
# RESUMO FINAL
# ===========================================================================

print("\n" + "=" * 70)
print("🎉 CONCLUÍDO!")
print("=" * 70)
print(f"✅ {total_fixed}/{len(files_to_fix)} arquivos corrigidos")
print("=" * 70)

print("\n📌 Próximos passos:")
print("   1. Testar models: python manage.py test acoes_pngi.tests.test_models -v 2")
print("   2. Testar tudo: python manage.py test acoes_pngi.tests -v 2")
print("   3. Commit: git add . && git commit -m 'fix: v5 FINAL - correção completa'")
print("   4. Push: git push origin fix/correcao-massiva-testes-pngi")
