#!/usr/bin/env python
"""Script de correção massiva v2 para testes PNGI

Corrige:
1. IndentationError em VigenciaPNGI.objects.create()
2. Import incorreto de rest_framework
3. Adiciona campos obrigatórios em Acoes.objects.create()

Uso:
    python fix_testes_massivo_v2.py
"""

import os
import re
from pathlib import Path


def fix_base_py():
    """Corrige o arquivo base.py - remove import do rest_framework"""
    base_file = Path('acoes_pngi/tests/base.py')
    
    if not base_file.exists():
        print("❌ Arquivo base.py não encontrado!")
        return False
    
    print("\n📄 Corrigindo base.py...")
    content = base_file.read_text(encoding='utf-8')
    
    # Remover import do rest_framework (causa erro)
    if 'from rest_framework.test import APITestCase' in content:
        content = content.replace('from rest_framework.test import APITestCase\n', '')
        print("   ✅ Removido import rest_framework")
    
    # Trocar herança de BaseAPITestCase para TestCase
    if 'class BaseAPITestCase(APITestCase):' in content:
        content = content.replace('class BaseAPITestCase(APITestCase):', 'class BaseAPITestCase(TestCase):')
        print("   ✅ BaseAPITestCase agora herda de TestCase")
    
    base_file.write_text(content, encoding='utf-8')
    print("✅ base.py corrigido!")
    return True


def fix_indentation_errors(file_path):
    """Corrige erros de indentação em VigenciaPNGI.objects.create()"""
    content = file_path.read_text(encoding='utf-8')
    original = content
    
    # Padrão: encontrar VigenciaPNGI.objects.create( com indentação incorreta
    # Problema: linhas após get_or_create/create têm indentação extra
    
    # Padrão 1: VigenciaPNGI.objects.get_or_create com defaults mal indentado
    pattern1 = r'(VigenciaPNGI\.objects\.get_or_create\([^)]+?defaults=\{[^}]+?)(\s+)(datiniciovigencia=[^,]+,\s+datfinalvigencia=[^,]+,\s+isvigenciaativa=[^}]+\})'
    
    def fix_vigencia_indent(match):
        prefix = match.group(1)
        bad_indent = match.group(2)
        fields = match.group(3)
        
        # Remover indentação extra e formatar corretamente
        fixed_fields = fields.replace('\n            ', '\n            ')
        return f"{prefix}\n            {fixed_fields}"
    
    content = re.sub(pattern1, fix_vigencia_indent, content, flags=re.MULTILINE | re.DOTALL)
    
    # Padrão 2: Corrigir qualquer linha com 'datfinalvigencia' mal indentada
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Se linha tem datfinalvigencia ou datiniciovigencia com muita indentação
        if ('datfinalvigencia=' in line or 'datiniciovigencia=' in line) and line.startswith('                '):
            # Remover 4 espaços extras
            fixed_line = line[4:]
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    if content != original:
        return content, True
    return content, False


def fix_acoes_create_calls(file_path):
    """Adiciona ideixo e idsituacaoacao em Acoes.objects.create()"""
    content = file_path.read_text(encoding='utf-8')
    original = content
    changes = []
    
    # Encontrar todos os Acoes.objects.create(
    pattern = r'(Acoes\.objects\.create\s*\([^)]+)(\))'
    
    def add_missing_fields(match):
        args_block = match.group(1)
        closing = match.group(2)
        
        # Verificar se já tem os campos
        has_eixo = 'ideixo=' in args_block
        has_situacao = 'idsituacaoacao=' in args_block
        
        if has_eixo and has_situacao:
            return match.group(0)  # Já está OK
        
        # Remover vírgula final se houver
        args_block = args_block.rstrip().rstrip(',')
        
        # Adicionar campos faltantes
        additions = []
        if not has_eixo:
            additions.append('ideixo=self.eixo_base')
        if not has_situacao:
            additions.append('idsituacaoacao=self.situacao_base')
        
        if additions:
            # Detectar indentação da última linha
            lines = args_block.split('\n')
            if len(lines) > 1:
                last_line = lines[-1]
                indent = len(last_line) - len(last_line.lstrip())
                indent_str = ' ' * indent
            else:
                indent_str = ''
            
            new_fields = ',\n' + indent_str + (',\n' + indent_str).join(additions)
            return args_block + new_fields + closing
        
        return match.group(0)
    
    content = re.sub(pattern, add_missing_fields, content, flags=re.DOTALL)
    
    if content != original:
        return content, True
    return content, False


def fix_file(file_path):
    """Aplica todas as correções em um arquivo"""
    print(f"\n📄 Processando: {file_path.name}")
    
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        changes = []
        
        # 1. Corrigir indentação
        content, changed = fix_indentation_errors(file_path)
        if changed:
            changes.append("Indentação corrigida")
            # Salvar temporariamente para próximas correções
            file_path.write_text(content, encoding='utf-8')
        
        # 2. Corrigir Acoes.objects.create
        content, changed = fix_acoes_create_calls(file_path)
        if changed:
            changes.append("Campos adicionados em Acoes.objects.create()")
        
        # Salvar se houver mudanças
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            print(f"✅ {file_path.name} - {len(changes)} correções aplicadas")
            for change in changes:
                print(f"   - {change}")
            return True
        else:
            print(f"⏭️  {file_path.name} - Sem mudanças necessárias")
            return False
            
    except Exception as e:
        print(f"❌ Erro em {file_path.name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""
    print("="*70)
    print("🔧 CORREÇÃO MASSIVA DE TESTES PNGI v2")
    print("="*70)
    
    # 1. Corrigir base.py primeiro
    if not fix_base_py():
        print("\n❌ Erro ao corrigir base.py. Abortando.")
        return
    
    # 2. Encontrar todos os arquivos test_*.py
    test_dir = Path('acoes_pngi/tests')
    if not test_dir.exists():
        print(f"\n❌ Diretório não encontrado: {test_dir}")
        return
    
    test_files = sorted(test_dir.glob('test_*.py'))
    
    if not test_files:
        print("\n❌ Nenhum arquivo de teste encontrado!")
        return
    
    print(f"\n📋 Encontrados {len(test_files)} arquivos de teste")
    
    # 3. Processar cada arquivo
    fixed_count = 0
    for file_path in test_files:
        if fix_file(file_path):
            fixed_count += 1
    
    # 4. Resultado final
    print("\n" + "="*70)
    print(f"🎉 CONCLUÍDO!")
    print(f"✅ {fixed_count}/{len(test_files)} arquivos corrigidos")
    print(f"⏭️  {len(test_files) - fixed_count}/{len(test_files)} arquivos sem alterações")
    print("="*70)
    print("\n📌 Próximos passos:")
    print("   1. Testar: pytest acoes_pngi/tests/test_models.py -v")
    print("   2. Se OK, testar todos: pytest acoes_pngi/tests/ -v")
    print("   3. Commit: git add . && git commit -m 'fix: Correções massivas testes'")
    print()


if __name__ == '__main__':
    main()
