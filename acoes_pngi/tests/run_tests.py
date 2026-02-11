#!/usr/bin/env python
"""
Script para executar testes de Ações PNGI de forma organizada.

Uso:
    python acoes_pngi/tests/run_tests.py [fase]

Fases:
    permissions  - Testes de permissões
    api          - Testes de API (todas as partes)
    web          - Testes web (views)
    all          - Todos os testes (padrão)

Exemplos:
    python acoes_pngi/tests/run_tests.py permissions
    python acoes_pngi/tests/run_tests.py api
    python manage.py test acoes_pngi.tests.test_permissions -v 2
"""

import sys
import os

# Adicionar o diretório do projeto ao PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from django.core.management import call_command
from django.conf import settings


def print_section(title):
    """Imprime seção formatada"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def run_test_module(module_path, description):
    """Executa um módulo de teste específico"""
    print_section(f"EXECUTANDO: {description}")
    print(f"Módulo: {module_path}\n")
    
    try:
        call_command('test', module_path, verbosity=2)
        print(f"\n✓ {description} - SUCESSO\n")
        return True
    except Exception as e:
        print(f"\n✗ {description} - FALHOU")
        print(f"Erro: {str(e)}\n")
        return False


def run_permissions_tests():
    """Executa testes de permissões"""
    return run_test_module(
        'acoes_pngi.tests.test_permissions',
        'Testes de Permissions (FASE 3)'
    )


def run_api_tests():
    """Executa todos os testes de API"""
    results = []
    
    results.append(run_test_module(
        'acoes_pngi.tests.test_api_views',
        'Testes de API - Parte 1: Eixo, Situação, Vigência (FASE 1.1)'
    ))
    
    results.append(run_test_module(
        'acoes_pngi.tests.test_api_views_acoes',
        'Testes de API - Parte 2: Ações, Prazos, Destaques (FASE 1.2)'
    ))
    
    results.append(run_test_module(
        'acoes_pngi.tests.test_api_views_alinhamento_responsaveis',
        'Testes de API - Parte 3: Alinhamento e Responsáveis (FASE 1.3)'
    ))
    
    return all(results)


def run_web_tests():
    """Executa testes web"""
    return run_test_module(
        'acoes_pngi.tests.test_views',
        'Testes Web (FASE 2)'
    )


def run_all_tests():
    """Executa todos os testes em ordem"""
    print_section("INICIANDO EXECUÇÃO DE TODOS OS TESTES")
    print("Ordem de execução:")
    print("  1. Permissions (base)")
    print("  2. API Tests (3 partes)")
    print("  3. Web Tests")
    print("\nTotal estimado: ~500 testes\n")
    
    results = {
        'permissions': run_permissions_tests(),
        'api': run_api_tests(),
        'web': run_web_tests()
    }
    
    # Resumo final
    print_section("RESUMO FINAL")
    
    for phase, success in results.items():
        status = "✓ SUCESSO" if success else "✗ FALHOU"
        print(f"{phase.upper():20} {status}")
    
    total_success = sum(results.values())
    total_phases = len(results)
    
    print(f"\nTotal: {total_success}/{total_phases} fases passaram")
    
    if all(results.values()):
        print("\n✓✓✓ TODOS OS TESTES PASSARAM! ✓✓✓\n")
        return 0
    else:
        print("\n✗✗✗ ALGUNS TESTES FALHARAM ✗✗✗\n")
        return 1


def main():
    """Função principal"""
    phase = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    if phase == 'permissions':
        success = run_permissions_tests()
    elif phase == 'api':
        success = run_api_tests()
    elif phase == 'web':
        success = run_web_tests()
    elif phase == 'all':
        return run_all_tests()
    else:
        print(f"Fase desconhecida: {phase}")
        print("Fases válidas: permissions, api, web, all")
        return 1
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
