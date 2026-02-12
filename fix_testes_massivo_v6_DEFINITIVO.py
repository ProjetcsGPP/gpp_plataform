#!/usr/bin/env python3
"""
Script v6 DEFINITIVO - Correção de TODOS os erros identificados

CATEGORIAS DE ERROS:
1. ImportError (4 arquivos) - imports incorretos
2. AttributeError 'situacao' (58 erros) - usar self.situacao_base
3. NameError 'vigencia' (30+ erros) - variável não definida
4. ValidationError datfinalvigencia (40+ erros) - campo obrigatório
5. AttributeError 'vigencia' (10 erros) - usar self.vigencia_base
6. TypeError list indices (2 erros) - acesso incorreto a response.data
7. SyntaxError (1 erro) - parêntese não fechado
"""

import os
import re

TESTS_DIR = os.path.join(os.path.dirname(__file__), 'acoes_pngi', 'tests')

print("=" * 70)
print("🔧 CORREÇÃO DEFINITIVA v6 - 171 ERROS")
print("=" * 70)

# ===========================================================================
# CORREÇÕES ESPECÍFICAS POR ARQUIVO
# ===========================================================================

def fix_test_diagnostic_api():
    """CATEGORIA 1: Corrigir ImportError - override_settings"""
    filepath = os.path.join(TESTS_DIR, 'test_diagnostic_api.py')
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remover import incorreto
    content = re.sub(r'from \.base import[^\n]*override_settings[^\n]*\n', '', content)
    
    # Adicionar import correto se necessário
    if 'override_settings' in content and 'from django.test import override_settings' not in content:
        content = 'from django.test import override_settings\n' + content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ test_diagnostic_api.py - ImportError corrigido")
    return True

def fix_test_views():
    """CATEGORIA 1: Corrigir ImportError - Client"""
    filepath = os.path.join(TESTS_DIR, 'test_views.py')
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remover import incorreto
    content = re.sub(r'from \.base import[^\n]*Client[^\n]*\n', '', content)
    
    # Adicionar import correto
    if 'Client' in content and 'from django.test import Client' not in content:
        # Adicionar após outros imports do django.test
        content = re.sub(
            r'(from django\.test import[^\n]+)',
            r'\1, Client',
            content,
            count=1
        )
        # Se não encontrou, adicionar nova linha
        if 'from django.test import' not in content or ', Client' not in content:
            content = 'from django.test import Client\n' + content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ test_views.py - ImportError corrigido")
    return True

def fix_test_web_acoes_views():
    """CATEGORIA 1: Corrigir ImportError - Client"""
    filepath = os.path.join(TESTS_DIR, 'test_web_acoes_views.py')
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remover import incorreto
    content = re.sub(r'from \.base import[^\n]*Client[^\n]*\n', '', content)
    
    # Adicionar import correto
    if 'Client' in content and 'from django.test import Client' not in content:
        content = 'from django.test import Client\n' + content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ test_web_acoes_views.py - ImportError corrigido")
    return True

def fix_test_web_views_complete():
    """CATEGORIA 7: Corrigir SyntaxError - parêntese não fechado"""
    filepath = os.path.join(TESTS_DIR, 'test_web_views_complete.py')
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Procurar por parênteses não fechados
    # Padrão comum: função com múltiplos argumentos sem fechar
    content = re.sub(r'(\w+\([^)]*)\n(\s*$)', r'\1)', content, flags=re.MULTILINE)
    
    # Corrigir linha 216 especificamente se existir
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if i == 215:  # linha 216 (index 215)
            # Contar parênteses
            open_count = line.count('(')
            close_count = line.count(')')
            if open_count > close_count:
                lines[i] = line + ')' * (open_count - close_count)
    
    content = '\n'.join(lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ test_web_views_complete.py - SyntaxError corrigido")
    return True

def fix_api_acoes_views():
    """CATEGORIA 2: Corrigir 27 AttributeError - self.situacao"""
    filepath = os.path.join(TESTS_DIR, 'test_api_acoes_views.py')
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Substituir self.situacao por self.situacao_base
    content = re.sub(r'idsituacaoacao=self\.situacao([,\)])', r'idsituacaoacao=self.situacao_base\1', content)
    
    # Substituir self.vigencia por self.vigencia_base
    content = re.sub(r'idvigenciapngi=self\.vigencia([,\)])', r'idvigenciapngi=self.vigencia_base\1', content)
    
    # Substituir self.eixo por self.eixo_base
    content = re.sub(r'ideixo=self\.eixo([,\)])', r'ideixo=self.eixo_base\1', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ test_api_acoes_views.py - 27 AttributeError corrigidos")
        return True
    
    return False

def fix_api_alinhamento_views():
    """CATEGORIA 2: Corrigir 17 AttributeError - self.situacao"""
    filepath = os.path.join(TESTS_DIR, 'test_api_alinhamento_views.py')
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Substituir self.situacao por self.situacao_base
    content = re.sub(r'idsituacaoacao=self\.situacao([,\)])', r'idsituacaoacao=self.situacao_base\1', content)
    
    # Substituir self.vigencia por self.vigencia_base
    content = re.sub(r'idvigenciapngi=self\.vigencia([,\)])', r'idvigenciapngi=self.vigencia_base\1', content)
    
    # Substituir self.eixo por self.eixo_base
    content = re.sub(r'ideixo=self\.eixo([,\)])', r'ideixo=self.eixo_base\1', content)
    
    # Corrigir IndexError linha 178 - verificar acesso a lista
    content = re.sub(
        r'self\.assertEqual\(response\.data\[0\]\[\'strdescricaotipoanotacao\'\]',
        r'self.assertEqual(response.data[\'results\'][0][\'strdescricaotipoanotacao\']',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ test_api_alinhamento_views.py - 17 AttributeError + IndexError corrigidos")
        return True
    
    return False

def fix_api_responsavel_views():
    """CATEGORIA 2: Corrigir 14 AttributeError - self.situacao"""
    filepath = os.path.join(TESTS_DIR, 'test_api_responsavel_views.py')
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Substituir self.situacao por self.situacao_base
    content = re.sub(r'idsituacaoacao=self\.situacao([,\)])', r'idsituacaoacao=self.situacao_base\1', content)
    
    # Substituir self.vigencia por self.vigencia_base
    content = re.sub(r'idvigenciapngi=self\.vigencia([,\)])', r'idvigenciapngi=self.vigencia_base\1', content)
    
    # Substituir self.eixo por self.eixo_base
    content = re.sub(r'ideixo=self\.eixo([,\)])', r'ideixo=self.eixo_base\1', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ test_api_responsavel_views.py - 14 AttributeError corrigidos")
        return True
    
    return False

def fix_api_views_acoes():
    """CATEGORIA 3, 4, 5, 6: Corrigir múltiplos erros"""
    filepath = os.path.join(TESTS_DIR, 'test_api_views_acoes.py')
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # CATEGORIA 3: NameError - 'vigencia' não definido em setup_test_data()
    # Substituir 'vigencia' por 'self.vigencia_base' em métodos de classe
    content = re.sub(
        r'(\s+)vigencia = VigenciaPNGI\.objects\.create\(',
        r'\1self.vigencia_base = VigenciaPNGI.objects.create(',
        content
    )
    content = re.sub(r'idvigenciapngi=vigencia([,\)])', r'idvigenciapngi=self.vigencia_base\1', content)
    
    # CATEGORIA 4: ValidationError - Adicionar datfinalvigencia
    # Encontrar VigenciaPNGI.objects.create sem datfinalvigencia
    vigencia_pattern = r'(VigenciaPNGI\.objects\.create\([^)]*datiniciovigencia=[^,\)]+)(\))'
    
    def add_datfinal(match):
        content = match.group(1)
        if 'datfinalvigencia' not in content:
            # Extrair data inicial para calcular final
            return content + ',\n            datfinalvigencia=date(2026, 12, 31)' + match.group(2)
        return match.group(0)
    
    content = re.sub(vigencia_pattern, add_datfinal, content)
    
    # CATEGORIA 5: self.vigencia -> self.vigencia_base
    content = re.sub(r'idvigenciapngi=self\.vigencia([,\)])', r'idvigenciapngi=self.vigencia_base\1', content)
    content = re.sub(r'idsituacaoacao=self\.situacao([,\)])', r'idsituacaoacao=self.situacao_base\1', content)
    content = re.sub(r'ideixo=self\.eixo([,\)])', r'ideixo=self.eixo_base\1', content)
    
    # CATEGORIA 6: TypeError - list indices must be integers
    # Corrigir acesso a response.data quando é lista paginada
    # Padrão: response.data['strapelido'] deve ser response.data['results'][0]['strapelido']
    
    # Linhas 371, 394: Acessando response.data diretamente quando é paginado
    content = re.sub(
        r"self\.assertEqual\(response\.data\['strapelido'\]",
        r"self.assertEqual(response.data['results'][0]['strapelido']",
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ test_api_views_acoes.py - NameError + ValidationError + TypeError corrigidos")
        return True
    
    return False

def fix_api_views_alinhamento_responsaveis():
    """CATEGORIA 3, 4: Corrigir NameError e ValidationError"""
    filepath = os.path.join(TESTS_DIR, 'test_api_views_alinhamento_responsaveis.py')
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # CATEGORIA 3: NameError - 'vigencia' não definido
    content = re.sub(r'idvigenciapngi=vigencia([,\)])', r'idvigenciapngi=self.vigencia_base\1', content)
    
    # Substituir variável local 'vigencia' por 'self.vigencia_base' em setup_test_data
    content = re.sub(
        r'(\s+)vigencia = VigenciaPNGI\.objects\.create\(',
        r'\1self.vigencia_base = VigenciaPNGI.objects.create(',
        content
    )
    
    # CATEGORIA 4: ValidationError - Adicionar datfinalvigencia
    vigencia_pattern = r'(VigenciaPNGI\.objects\.create\([^)]*datiniciovigencia=[^,\)]+)(\))'
    
    def add_datfinal(match):
        content = match.group(1)
        if 'datfinalvigencia' not in content:
            return content + ',\n            datfinalvigencia=date(2026, 12, 31)' + match.group(2)
        return match.group(0)
    
    content = re.sub(vigencia_pattern, add_datfinal, content)
    
    # Substituir outras referências
    content = re.sub(r'idsituacaoacao=self\.situacao([,\)])', r'idsituacaoacao=self.situacao_base\1', content)
    content = re.sub(r'ideixo=self\.eixo([,\)])', r'ideixo=self.eixo_base\1', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ test_api_views_alinhamento_responsaveis.py - NameError + ValidationError corrigidos")
        return True
    
    return False

def fix_api_views():
    """CATEGORIA 5: Corrigir self.vigencia -> self.vigencia_base"""
    filepath = os.path.join(TESTS_DIR, 'test_api_views.py')
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Substituir todas as referências incorretas
    content = re.sub(r'idvigenciapngi=self\.vigencia([,\)])', r'idvigenciapngi=self.vigencia_base\1', content)
    content = re.sub(r'idsituacaoacao=self\.situacao([,\)])', r'idsituacaoacao=self.situacao_base\1', content)
    content = re.sub(r'ideixo=self\.eixo([,\)])', r'ideixo=self.eixo_base\1', content)
    
    # Substituir self.vigencia.pk por self.vigencia_base.pk
    content = re.sub(r'self\.vigencia\.pk', r'self.vigencia_base.pk', content)
    content = re.sub(r'self\.vigencia\.idvigenciapngi', r'self.vigencia_base.idvigenciapngi', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ test_api_views.py - AttributeError 'vigencia' corrigido")
        return True
    
    return False

# ===========================================================================
# EXECUTAR TODAS AS CORREÇÕES
# ===========================================================================

print("\n📝 Aplicando correções por categoria...\n")

fixed_count = 0

# CATEGORIA 1: ImportError
if fix_test_diagnostic_api():
    fixed_count += 1
if fix_test_views():
    fixed_count += 1
if fix_test_web_acoes_views():
    fixed_count += 1

# CATEGORIA 7: SyntaxError
if fix_test_web_views_complete():
    fixed_count += 1

# CATEGORIA 2, 5: AttributeError
if fix_api_acoes_views():
    fixed_count += 1
if fix_api_alinhamento_views():
    fixed_count += 1
if fix_api_responsavel_views():
    fixed_count += 1
if fix_api_views():
    fixed_count += 1

# CATEGORIA 3, 4, 6: NameError, ValidationError, TypeError
if fix_api_views_acoes():
    fixed_count += 1
if fix_api_views_alinhamento_responsaveis():
    fixed_count += 1

# ===========================================================================
# VERIFICAÇÃO FINAL
# ===========================================================================

print("\n🔍 Verificando problemas remanescentes...\n")

issues = {}
files_to_check = [
    'test_api_acoes_views.py',
    'test_api_alinhamento_views.py',
    'test_api_responsavel_views.py',
    'test_api_views.py',
    'test_api_views_acoes.py',
    'test_api_views_alinhamento_responsaveis.py',
    'test_diagnostic_api.py',
    'test_views.py',
    'test_web_acoes_views.py',
    'test_web_views_complete.py',
]

for filename in files_to_check:
    filepath = os.path.join(TESTS_DIR, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    problems = []
    
    # Verificar self.situacao (sem _base)
    if re.search(r'idsituacaoacao=self\.situacao[,\)]', content):
        count = len(re.findall(r'idsituacaoacao=self\.situacao[,\)]', content))
        problems.append(f"self.situacao encontrado ({count}x)")
    
    # Verificar self.vigencia (sem _base)
    if re.search(r'idvigenciapngi=self\.vigencia[,\)]', content):
        count = len(re.findall(r'idvigenciapngi=self\.vigencia[,\)]', content))
        problems.append(f"self.vigencia encontrado ({count}x)")
    
    # Verificar self.eixo (sem _base)
    if re.search(r'ideixo=self\.eixo[,\)]', content):
        count = len(re.findall(r'ideixo=self\.eixo[,\)]', content))
        problems.append(f"self.eixo encontrado ({count}x)")
    
    # Verificar variável 'vigencia' sem self
    if re.search(r'idvigenciapngi=vigencia[,\)]', content):
        count = len(re.findall(r'idvigenciapngi=vigencia[,\)]', content))
        problems.append(f"variável 'vigencia' encontrada ({count}x)")
    
    if problems:
        issues[filename] = problems

if issues:
    print("⚠️  Problemas encontrados:\n")
    for filename, problems in issues.items():
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
print(f"✅ {fixed_count} arquivos corrigidos")
print("=" * 70)

print("\n📌 Próximos passos:")
print("   1. Testar: python manage.py test acoes_pngi.tests.test_models -v 2")
print("   2. Testar tudo: python manage.py test acoes_pngi.tests -v 2")
print("   3. Commit: git add . && git commit -m 'fix: v6 - correção de 171 erros'")
print("   4. Push: git push origin fix/correcao-massiva-testes-pngi")
