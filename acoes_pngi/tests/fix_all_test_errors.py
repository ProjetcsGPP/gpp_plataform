#!/usr/bin/env python3
"""fix_all_test_errors.py

Script para corrigir TODOS os erros restantes nos testes (76 erros).

Execução:
    python acoes_pngi/tests/fix_all_test_errors.py

Problemas corrigidos:
1. ✅ Import Errors (3 arquivos) - Remove 'from .base import BaseTestCase'
2. ✅ ValidationError datfinalvigencia - Adiciona campo obrigatório
3. ✅ IndexError list index out of range - Garante fixtures antes de testes
4. ✅ AssertionError 0 != 1/2 - Adiciona ideixo e idsituacaoacao nas Acoes
5. ✅ AttributeError self.eixo/vigencia - Adiciona atributos no setUp()
"""

import os
import re
from pathlib import Path


class TestErrorFixer:
    """Corrige erros nos arquivos de teste"""
    
    def __init__(self, tests_dir):
        self.tests_dir = Path(tests_dir)
        self.changes_made = []
    
    def fix_all(self):
        """Executa todas as correções"""
        print("🔧 Iniciando correção de TODOS os erros de teste...")
        print("=" * 70)
        
        # 1. Remover imports de BaseTestCase (Import Errors)
        self.fix_import_errors()
        
        # 2. Adicionar datfinalvigencia em VigenciaPNGI
        self.fix_vigencia_validation_errors()
        
        # 3. Corrigir AttributeError self.eixo e self.vigencia
        self.fix_attribute_errors()
        
        # 4. Garantir fixtures completas antes de testes de filtros
        self.fix_index_errors_and_assertions()
        
        print("\n" + "=" * 70)
        print(f"✅ Correções concluídas! Total de mudanças: {len(self.changes_made)}")
        self._print_summary()
    
    # ========================================================================
    # 1. CORRIGIR IMPORT ERRORS - Remove BaseTestCase
    # ========================================================================
    
    def fix_import_errors(self):
        """Remove imports de BaseTestCase que não existe"""
        print("\n1️⃣  Corrigindo Import Errors (BaseTestCase)...")
        
        files_to_fix = [
            'test_diagnostic_api.py',
            'test_web_acoes_views.py',
            'test_web_views_complete.py'
        ]
        
        for filename in files_to_fix:
            filepath = self.tests_dir / filename
            if not filepath.exists():
                print(f"   ⚠️  Arquivo não encontrado: {filename}")
                continue
            
            content = filepath.read_text(encoding='utf-8')
            original_content = content
            
            # Remover import de BaseTestCase
            patterns = [
                r'from \.base import BaseTestCase\n',
                r'from acoes_pngi\.tests\.base import BaseTestCase\n',
                r'from tests\.base import BaseTestCase\n',
            ]
            
            for pattern in patterns:
                content = re.sub(pattern, '', content)
            
            # Substituir herança de BaseTestCase por TestCase
            content = re.sub(
                r'class (\w+)\(BaseTestCase\):',
                r'class \1(TestCase):',
                content
            )
            
            if content != original_content:
                filepath.write_text(content, encoding='utf-8')
                self.changes_made.append(f"✅ {filename}: Removido BaseTestCase")
                print(f"   ✅ {filename}")
    
    # ========================================================================
    # 2. CORRIGIR VALIDATION ERRORS - Adicionar datfinalvigencia
    # ========================================================================
    
    def fix_vigencia_validation_errors(self):
        """Adiciona datfinalvigencia em todas criações de VigenciaPNGI"""
        print("\n2️⃣  Corrigindo ValidationError (datfinalvigencia)...")
        
        test_files = list(self.tests_dir.glob('test_*.py'))
        
        for filepath in test_files:
            content = filepath.read_text(encoding='utf-8')
            original_content = content
            
            # Padrão: VigenciaPNGI.objects.create SEM datfinalvigencia
            pattern = r'(VigenciaPNGI\.objects\.create\([^)]*datiniciovigencia=date\((\d{4}),\s*(\d{1,2}),\s*(\d{1,2})\))(?![^)]*datfinalvigencia)'
            
            def add_datfinalvigencia(match):
                full_match = match.group(0)
                year = int(match.group(2))
                
                # Se já termina com ), adicionar datfinalvigencia antes do )
                if full_match.endswith(')'):
                    return full_match[:-1] + f',\n            datfinalvigencia=date({year}, 12, 31)'
                else:
                    return full_match + f',\n            datfinalvigencia=date({year}, 12, 31)'
            
            # Primeira passagem: adicionar vírgula se não houver
            content = re.sub(
                r'(datiniciovigencia=date\(\d{4},\s*\d{1,2},\s*\d{1,2}\))(\s*\))',
                r'\1,\n            datfinalvigencia=date(2026, 12, 31)\2',
                content
            )
            
            # Segunda passagem: casos com outros campos após datiniciovigencia
            content = re.sub(
                r'(VigenciaPNGI\.objects\.create\([^)]*datiniciovigencia=date\((\d{4}),\s*\d{1,2},\s*\d{1,2}\),)(\s+is)',
                r'\1\n            datfinalvigencia=date(\2, 12, 31),\3',
                content
            )
            
            if content != original_content:
                filepath.write_text(content, encoding='utf-8')
                self.changes_made.append(f"✅ {filepath.name}: Adicionado datfinalvigencia")
                print(f"   ✅ {filepath.name}")
    
    # ========================================================================
    # 3. CORRIGIR ATTRIBUTE ERRORS - Adicionar self.eixo e self.vigencia
    # ========================================================================
    
    def fix_attribute_errors(self):
        """Adiciona self.eixo e self.vigencia no setUp() onde estão faltando"""
        print("\n3️⃣  Corrigindo AttributeError (self.eixo, self.vigencia)...")
        
        filepath = self.tests_dir / 'test_api_views.py'
        if not filepath.exists():
            print(f"   ⚠️  Arquivo não encontrado: test_api_views.py")
            return
        
        content = filepath.read_text(encoding='utf-8')
        original_content = content
        
        # Encontrar classes que herdam de BaseAPITestCase
        class_pattern = r'class (\w+APITests)\(BaseAPITestCase\):'
        classes = re.findall(class_pattern, content)
        
        for class_name in classes:
            # Verificar se a classe tem setup_test_data
            setup_pattern = rf'(class {class_name}\(BaseAPITestCase\):.*?def setup_test_data\(self\):.*?)(def |\nclass |\Z)'
            match = re.search(setup_pattern, content, re.DOTALL)
            
            if match:
                setup_content = match.group(1)
                
                # Se não tem self.vigencia, adicionar
                if 'self.vigencia =' not in setup_content:
                    # Procurar onde criar VigenciaPNGI e adicionar self.
                    content = re.sub(
                        rf'(class {class_name}\(BaseAPITestCase\):.*?def setup_test_data\(self\):.*?)(vigencia = VigenciaPNGI)',
                        r'\1self.vigencia = VigenciaPNGI',
                        content,
                        flags=re.DOTALL
                    )
                
                # Se não tem self.eixo, adicionar
                if 'self.eixo =' not in setup_content:
                    content = re.sub(
                        rf'(class {class_name}\(BaseAPITestCase\):.*?def setup_test_data\(self\):.*?)(eixo = Eixo)',
                        r'\1self.eixo = Eixo',
                        content,
                        flags=re.DOTALL
                    )
                
                # Se não tem self.situacao, adicionar
                if 'self.situacao =' not in setup_content:
                    content = re.sub(
                        rf'(class {class_name}\(BaseAPITestCase\):.*?def setup_test_data\(self\):.*?)(situacao = SituacaoAcao)',
                        r'\1self.situacao = SituacaoAcao',
                        content,
                        flags=re.DOTALL
                    )
        
        if content != original_content:
            filepath.write_text(content, encoding='utf-8')
            self.changes_made.append(f"✅ test_api_views.py: Adicionado self.eixo e self.vigencia")
            print(f"   ✅ test_api_views.py")
    
    # ========================================================================
    # 4. CORRIGIR INDEX ERRORS E ASSERTION ERRORS
    # ========================================================================
    
    def fix_index_errors_and_assertions(self):
        """Corrige IndexErrors e AssertionErrors (0 != 1/2) garantindo fixtures"""
        print("\n4️⃣  Corrigindo IndexError e AssertionError (fixtures incompletas)...")
        
        test_files = [
            'test_api_views.py',
            'test_api_acoes_views.py',
            'test_api_alinhamento_views.py',
            'test_api_responsavel_views.py'
        ]
        
        for filename in test_files:
            filepath = self.tests_dir / filename
            if not filepath.exists():
                continue
            
            content = filepath.read_text(encoding='utf-8')
            original_content = content
            
            # Padrão: Acoes.objects.create SEM ideixo ou idsituacaoacao
            # Adicionar ideixo quando falta
            content = self._add_missing_fk_to_acoes(content, 'ideixo', 'self.eixo')
            
            # Adicionar idsituacaoacao quando falta
            content = self._add_missing_fk_to_acoes(content, 'idsituacaoacao', 'self.situacao')
            
            # Garantir que setup_test_data cria Eixo e SituacaoAcao
            content = self._ensure_setup_creates_dependencies(content)
            
            if content != original_content:
                filepath.write_text(content, encoding='utf-8')
                self.changes_made.append(f"✅ {filename}: Fixtures completas")
                print(f"   ✅ {filename}")
    
    def _add_missing_fk_to_acoes(self, content, fk_name, fk_value):
        """Adiciona FK faltando em Acoes.objects.create()"""
        
        # Padrão: Acoes.objects.create(...) que não tem o FK
        pattern = rf'(Acoes\.objects\.create\([^)]*idvigenciapngi=[^)]*?)(\s*\))'
        
        def add_fk(match):
            create_call = match.group(1)
            closing = match.group(2)
            
            # Se já tem o FK, não adicionar
            if fk_name in create_call:
                return match.group(0)
            
            # Adicionar FK antes do )
            return f"{create_call},\n            {fk_name}={fk_value}{closing}"
        
        return re.sub(pattern, add_fk, content)
    
    def _ensure_setup_creates_dependencies(self, content):
        """Garante que setup_test_data cria Eixo e SituacaoAcao"""
        
        # Procurar setup_test_data methods
        setup_pattern = r'(def setup_test_data\(self\):)(.*?)(def |\Z)'
        
        def enhance_setup(match):
            method_def = match.group(1)
            method_body = match.group(2)
            next_def = match.group(3)
            
            # Se não tem criação de Eixo, adicionar
            if 'Eixo.objects.create' not in method_body:
                eixo_creation = '''
        
        # Criar Eixo (se não existe)
        if not hasattr(self, 'eixo') or self.eixo is None:
            self.eixo = Eixo.objects.create(
                stralias='E1',
                strdescricaoeixo='Eixo 1 - Gestão'
            )
'''
                method_body = eixo_creation + method_body
            
            # Se não tem criação de SituacaoAcao, adicionar
            if 'SituacaoAcao.objects.create' not in method_body:
                situacao_creation = '''
        
        # Criar SituacaoAcao (se não existe)
        if not hasattr(self, 'situacao') or self.situacao is None:
            self.situacao = SituacaoAcao.objects.create(
                strdescricaosituacao='Em Andamento'
            )
'''
                method_body = situacao_creation + method_body
            
            return method_def + method_body + next_def
        
        return re.sub(setup_pattern, enhance_setup, content, flags=re.DOTALL)
    
    # ========================================================================
    # RELATÓRIO FINAL
    # ========================================================================
    
    def _print_summary(self):
        """Imprime sumário das correções"""
        print("\n📊 SUMÁRIO DAS CORREÇÕES:")
        print("-" * 70)
        
        categories = {
            'Import Errors': [],
            'ValidationError': [],
            'AttributeError': [],
            'Fixtures': []
        }
        
        for change in self.changes_made:
            if 'BaseTestCase' in change:
                categories['Import Errors'].append(change)
            elif 'datfinalvigencia' in change:
                categories['ValidationError'].append(change)
            elif 'self.eixo' in change or 'self.vigencia' in change:
                categories['AttributeError'].append(change)
            else:
                categories['Fixtures'].append(change)
        
        for category, changes in categories.items():
            if changes:
                print(f"\n{category} ({len(changes)} arquivos):")
                for change in changes:
                    print(f"  • {change}")
        
        print("\n" + "=" * 70)
        print("🎉 Script concluído com sucesso!")
        print("\n💡 Próximos passos:")
        print("   1. Rodar os testes novamente: python manage.py test acoes_pngi.tests")
        print("   2. Verificar se os 76 erros foram reduzidos")
        print("   3. Analisar logs para erros restantes")


def main():
    """Função principal"""
    # Obter diretório de testes
    script_dir = Path(__file__).parent
    tests_dir = script_dir
    
    print("🚀 Fix All Test Errors")
    print("=" * 70)
    print(f"📁 Diretório de testes: {tests_dir}")
    
    # Executar correções
    fixer = TestErrorFixer(tests_dir)
    fixer.fix_all()


if __name__ == '__main__':
    main()
