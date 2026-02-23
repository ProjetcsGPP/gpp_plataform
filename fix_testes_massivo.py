#!/usr/bin/env python
"""Script de correção massiva para testes PNGI

Este script corrige AUTOMATICAMENTE todos os arquivos de teste que possuem
erros de NULL constraint violation em Acoes.objects.create().

Problema:
    Acoes.objects.create() sem ideixo e idsituacaoacao

Solução:
    1. Adiciona imports necessários
    2. Troca TestCase por BaseTestCase
    3. Adiciona ideixo=self.eixo_base e idsituacaoacao=self.situacao_base

Uso:
    python fix_testes_massivo.py
"""

import os
import re
from pathlib import Path


def fix_imports(content):
    """Adiciona imports necessários se não existirem"""
    changes = []
    
    # Adicionar import da BaseTestCase
    if 'from .base import' not in content and 'BaseTestCase' not in content:
        # Encontrar linha de imports do Django
        if 'from django.test import TestCase' in content:
            content = content.replace(
                'from django.test import TestCase',
                'from django.test import TestCase\nfrom .base import BaseTestCase, BaseAPITestCase'
            )
            changes.append('Adicionado import BaseTestCase')
        elif 'from rest_framework.test import APITestCase' in content:
            content = content.replace(
                'from rest_framework.test import APITestCase',
                'from rest_framework.test import APITestCase\nfrom .base import BaseTestCase, BaseAPITestCase'
            )
            changes.append('Adicionado import BaseAPITestCase')
    
    return content, changes


def fix_test_class_inheritance(content):
    """Troca TestCase por BaseTestCase e APITestCase por BaseAPITestCase"""
    changes = []
    
    # Trocar TestCase por BaseTestCase
    pattern_testcase = r'class (\w+)\(TestCase\):'
    matches = re.findall(pattern_testcase, content)
    if matches:
        content = re.sub(pattern_testcase, r'class \1(BaseTestCase):', content)
        changes.append(f'Trocado {len(matches)} classe(s) TestCase → BaseTestCase')
    
    # Trocar APITestCase por BaseAPITestCase
    pattern_api = r'class (\w+)\(APITestCase\):'
    matches = re.findall(pattern_api, content)
    if matches:
        content = re.sub(pattern_api, r'class \1(BaseAPITestCase):', content)
        changes.append(f'Trocado {len(matches)} classe(s) APITestCase → BaseAPITestCase')
    
    return content, changes


def fix_acoes_create(content):
    """Adiciona ideixo e idsituacaoacao em todas as chamadas Acoes.objects.create()"""
    changes = []
    
    # Padrão: Acoes.objects.create(...) SEM ideixo e idsituacaoacao
    pattern = r'Acoes\.objects\.create\(([^)]+)\)'
    
    def replacer(match):
        args = match.group(1)
        
        # Verificar se já tem ideixo e idsituacaoacao
        has_eixo = 'ideixo=' in args
        has_situacao = 'idsituacaoacao=' in args
        
        if has_eixo and has_situacao:
            return match.group(0)  # Já está correto
        
        # Adicionar campos faltantes
        to_add = []
        if not has_eixo:
            to_add.append('ideixo=self.eixo_base')
        if not has_situacao:
            to_add.append('idsituacaoacao=self.situacao_base')
        
        if to_add:
            # Adicionar ao final dos argumentos
            new_args = args.rstrip().rstrip(',') + ',\n            ' + ',\n            '.join(to_add)
            changes.append('Adicionado ideixo e/ou idsituacaoacao')
            return f'Acoes.objects.create({new_args})'
        
        return match.group(0)
    
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    return new_content, changes


def remove_setup_duplicates(content):
    """Remove criações duplicadas de eixo, situacao e vigencia em setUp/setUpClass"""
    changes = []
    
    # Remover criações de Eixo, SituacaoAcao, VigenciaPNGI em setUp
    patterns_to_remove = [
        r'self\.eixo\s*=\s*Eixo\.objects\.create\([^)]+\)',
        r'self\.situacao\s*=\s*SituacaoAcao\.objects\.create\([^)]+\)',
        r'self\.vigencia\s*=\s*VigenciaPNGI\.objects\.create\([^)]+\)',
    ]
    
    for pattern in patterns_to_remove:
        if re.search(pattern, content):
            content = re.sub(pattern, '# Removido: usar self.eixo_base/situacao_base/vigencia_base', content)
            changes.append('Removido criação duplicada de dados base')
    
    return content, changes


def fix_file(file_path):
    """Corrige um arquivo de teste"""
    print(f"\n📄 Processando: {file_path.name}")
    
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        all_changes = []
        
        # Aplicar correções
        content, changes = fix_imports(content)
        all_changes.extend(changes)
        
        content, changes = fix_test_class_inheritance(content)
        all_changes.extend(changes)
        
        content, changes = fix_acoes_create(content)
        all_changes.extend(changes)
        
        content, changes = remove_setup_duplicates(content)
        all_changes.extend(changes)
        
        # Salvar se houver mudanças
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            print(f"✅ {file_path.name} - {len(all_changes)} alterações")
            for change in all_changes:
                print(f"   - {change}")
            return True
        else:
            print(f"⏭️  {file_path.name} - Nenhuma alteração necessária")
            return False
    
    except Exception as e:
        print(f"❌ Erro em {file_path.name}: {e}")
        return False


def main():
    """Função principal"""
    print("="*70)
    print("🔧 CORREÇÃO MASSIVA DE TESTES PNGI")
    print("="*70)
    
    # Encontrar todos os arquivos test_*.py
    test_dir = Path('acoes_pngi/tests')
    test_files = sorted(test_dir.glob('test_*.py'))
    
    if not test_files:
        print("❌ Nenhum arquivo de teste encontrado!")
        return
    
    print(f"\n📋 Encontrados {len(test_files)} arquivos de teste\n")
    
    # Processar cada arquivo
    fixed_count = 0
    for file_path in test_files:
        if fix_file(file_path):
            fixed_count += 1
    
    # Resultado final
    print("\n" + "="*70)
    print(f"🎉 CONCLUÍDO!")
    print(f"✅ {fixed_count}/{len(test_files)} arquivos corrigidos")
    print(f"⏭️  {len(test_files) - fixed_count}/{len(test_files)} arquivos sem alterações")
    print("="*70)
    print("\n📌 Próximos passos:")
    print("   1. Revisar as mudanças: git diff")
    print("   2. Executar testes: pytest acoes_pngi/tests/ -v")
    print("   3. Commit: git add . && git commit -m 'fix: Correção massiva testes PNGI'")
    print()


if __name__ == '__main__':
    main()
