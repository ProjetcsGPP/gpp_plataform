#!/usr/bin/env python
"""fix_all_tests_massive.py

Script para correção MASSIVA de TODOS os testes do módulo acoes_pngi.

Problemas corrigidos:
1. Referências incorretas a self.vigencia → self.vigencia_base
2. Referências incorretas a self.eixo → self.eixo_base
3. Referências incorretas a self.situacao → self.situacao_base
4. Métodos setup_test_data() vazios ou com variáveis locais
5. Falta do campo datfinalvigencia em VigenciaPNGI.objects.create()

Execução:
    python acoes_pngi/tests/fix_all_tests_massive.py
"""

import os
import re
from pathlib import Path


# Diretório base dos testes
TESTS_DIR = Path(__file__).parent

# Arquivos que SERÃO corrigidos
FILES_TO_FIX = [
    'test_api_views.py',
    'test_views.py',
    'test_context_processors.py',
    'test_web_views_complete.py',
    'test_context_api_views_complete.py',
]


def fix_setup_test_data_empty(content):
    """
    Corrige métodos setup_test_data() que estão vazios ou apenas com pass.
    Remove completamente para usar a implementação da classe base.
    """
    # Padrão: def setup_test_data(self): seguido de apenas pass ou docstring + pass
    pattern = r'(\s+)def setup_test_data\(self\):[\s\S]*?(?=\n\s{4}def |\n\s{0,3}class |\Z)'
    
    def replacer(match):
        method_content = match.group(0)
        # Se o método só tem pass ou docstring vazia, remove
        if 'pass' in method_content and method_content.count('\n') <= 5:
            return ''  # Remove completamente
        # Se tem comentários mas nada de código útil, remove
        if not any(x in method_content for x in ['objects.create', 'objects.get_or_create', 'self.']):
            return ''
        return match.group(0)
    
    return re.sub(pattern, replacer, content)


def fix_local_variables_to_self(content):
    """
    Corrige variáveis locais dentro de setup_test_data() para self.atributo.
    
    Exemplos:
        eixo = Eixo.objects.create(...) → self.eixo = Eixo.objects.create(...)
        situacao = SituacaoAcao.objects.create(...) → self.situacao = ...
        vigencia = VigenciaPNGI.objects.create(...) → self.vigencia = ...
    """
    patterns = [
        # eixo = Eixo.objects → self.eixo = Eixo.objects
        (r'(\s+)eixo = Eixo\.objects', r'\1self.eixo = Eixo.objects'),
        # situacao = SituacaoAcao.objects → self.situacao = ...
        (r'(\s+)situacao = SituacaoAcao\.objects', r'\1self.situacao = SituacaoAcao.objects'),
        # vigencia = VigenciaPNGI.objects → self.vigencia = ...
        (r'(\s+)vigencia = VigenciaPNGI\.objects', r'\1self.vigencia = VigenciaPNGI.objects'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content


def fix_vigencia_references(content):
    """
    Substitui TODAS as referências a self.vigencia por self.vigencia_base.
    Exceto em definições (self.vigencia =).
    """
    # Não substituir quando é atribuição: self.vigencia =
    # Substituir: self.vigencia.campo, self.vigencia)
    patterns = [
        # self.vigencia. → self.vigencia_base.
        (r'self\.vigencia\.', 'self.vigencia_base.'),
        # self.vigencia) → self.vigencia_base)
        (r'self\.vigencia\)', 'self.vigencia_base)'),
        # self.vigencia, → self.vigencia_base,
        (r'self\.vigencia,', 'self.vigencia_base,'),
        # idvigenciapngi=self.vigencia → idvigenciapngi=self.vigencia_base
        (r'idvigenciapngi=self\.vigencia([\s\),])', r'idvigenciapngi=self.vigencia_base\1'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content


def fix_eixo_references(content):
    """
    Substitui TODAS as referências a self.eixo por self.eixo_base.
    Exceto em definições (self.eixo =).
    """
    patterns = [
        # self.eixo. → self.eixo_base.
        (r'self\.eixo\.', 'self.eixo_base.'),
        # self.eixo) → self.eixo_base)
        (r'self\.eixo\)', 'self.eixo_base)'),
        # self.eixo, → self.eixo_base,
        (r'self\.eixo,', 'self.eixo_base,'),
        # ideixo=self.eixo → ideixo=self.eixo_base
        (r'ideixo=self\.eixo([\s\),])', r'ideixo=self.eixo_base\1'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content


def fix_situacao_references(content):
    """
    Substitui TODAS as referências a self.situacao por self.situacao_base.
    Exceto em definições (self.situacao =).
    """
    patterns = [
        # self.situacao. → self.situacao_base.
        (r'self\.situacao\.', 'self.situacao_base.'),
        # self.situacao) → self.situacao_base)
        (r'self\.situacao\)', 'self.situacao_base)'),
        # self.situacao, → self.situacao_base,
        (r'self\.situacao,', 'self.situacao_base,'),
        # idsituacaoacao=self.situacao → idsituacaoacao=self.situacao_base
        (r'idsituacaoacao=self\.situacao([\s\),])', r'idsituacaoacao=self.situacao_base\1'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content


def add_datfinalvigencia(content):
    """
    Adiciona datfinalvigencia em todas as criações de VigenciaPNGI que não têm.
    
    Procura por:
        VigenciaPNGI.objects.create(
            ...
            datiniciovigencia=date(YYYY, M, D)
            # FALTA datfinalvigencia
        )
    
    Adiciona:
        datfinalvigencia=date(YYYY, 12, 31)
    """
    # Padrão complexo para capturar blocos de criação sem datfinalvigencia
    pattern = r'(VigenciaPNGI\.objects\.(?:create|get_or_create)\([^)]*datiniciovigencia=date\((\d{4})[^)]*\)(?![^)]*datfinalvigencia)[^)]*)(\))'
    
    def replacer(match):
        block = match.group(1)
        year = match.group(2)
        closing = match.group(3)
        
        # Se já tem datfinalvigencia, não mexe
        if 'datfinalvigencia' in block:
            return match.group(0)
        
        # Adicionar antes do )
        return f"{block},\n            datfinalvigencia=date({year}, 12, 31){closing}"
    
    return re.sub(pattern, replacer, content, flags=re.DOTALL)


def remove_duplicate_base_creations(content):
    """
    Remove criações duplicadas de Eixo, SituacaoAcao dentro de setup_test_data()
    quando a classe já herda de BaseTestCase (que cria eixo_base, situacao_base, vigencia_base).
    """
    # Padrão: bloco if dentro de setup_test_data criando eixo/situacao
    patterns_to_remove = [
        # if not hasattr(self, 'eixo') ... self.eixo = Eixo.objects.create(...)
        r"\s+# Criar Eixo \(se não existe\)[^\n]*\n\s+if not hasattr\(self, 'eixo'\)[\s\S]*?(?=\n\s{8}# Criar|\n\s{4}def |\Z)",
        # if not hasattr(self, 'situacao') ... self.situacao = SituacaoAcao.objects.create(...)
        r"\s+# Criar SituacaoAcao \(se não existe\)[^\n]*\n\s+if not hasattr\(self, 'situacao'\)[\s\S]*?(?=\n\s{8}# Criar|\n\s{4}def |\Z)",
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content)
    
    return content


def process_file(filepath):
    """
    Processa um arquivo de teste aplicando todas as correções.
    """
    print(f"\n{'='*80}")
    print(f"Processando: {filepath.name}")
    print('='*80)
    
    # Ler conteúdo
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    content = original_content
    
    # Aplicar todas as correções
    print("  [1/8] Corrigindo setup_test_data() vazios...")
    content = fix_setup_test_data_empty(content)
    
    print("  [2/8] Corrigindo variáveis locais para self...")
    content = fix_local_variables_to_self(content)
    
    print("  [3/8] Corrigindo referências self.vigencia → self.vigencia_base...")
    content = fix_vigencia_references(content)
    
    print("  [4/8] Corrigindo referências self.eixo → self.eixo_base...")
    content = fix_eixo_references(content)
    
    print("  [5/8] Corrigindo referências self.situacao → self.situacao_base...")
    content = fix_situacao_references(content)
    
    print("  [6/8] Adicionando datfinalvigencia em VigenciaPNGI...")
    content = add_datfinalvigencia(content)
    
    print("  [7/8] Removendo criações duplicadas de base...")
    content = remove_duplicate_base_creations(content)
    
    # Verificar se houve mudanças
    if content == original_content:
        print("  ✅ Nenhuma mudança necessária")
        return False
    
    # Escrever arquivo atualizado
    print("  [8/8] Salvando arquivo...")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Arquivo corrigido com sucesso!")
    return True


def main():
    """
    Função principal que executa todas as correções.
    """
    print("✅" * 40)
    print("CORREÇÃO MASSIVA DE TESTES - ACOES_PNGI")
    print("✅" * 40)
    print(f"\nDiretório: {TESTS_DIR}")
    print(f"Arquivos a processar: {len(FILES_TO_FIX)}")
    
    fixed_count = 0
    
    for filename in FILES_TO_FIX:
        filepath = TESTS_DIR / filename
        
        if not filepath.exists():
            print(f"\n⚠️  AVISO: Arquivo não encontrado: {filename}")
            continue
        
        if process_file(filepath):
            fixed_count += 1
    
    print("\n" + "="*80)
    print("RESUMO FINAL")
    print("="*80)
    print(f"✅ Arquivos corrigidos: {fixed_count}/{len(FILES_TO_FIX)}")
    print(f"📚 Arquivos sem alterações: {len(FILES_TO_FIX) - fixed_count}")
    
    if fixed_count > 0:
        print("\n🎉 Correções aplicadas com sucesso!")
        print("\n🛠️  PRÓXIMOS PASSOS:")
        print("  1. Executar: python manage.py test acoes_pngi.tests -v 2")
        print("  2. Verificar resultados")
        print("  3. Commitar mudanças se testes passarem")
    else:
        print("\n✔️  Todos os arquivos já estão corretos!")


if __name__ == '__main__':
    main()
