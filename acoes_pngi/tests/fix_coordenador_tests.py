"""
Script para corrigir testes de COORDENADOR_PNGI.

HIERARQUIA CORRETA:
- GESTOR_PNGI: CRUD completo em TUDO (44 perms)
- COORDENADOR_PNGI: view configs + CRUD negócio/filhas (29 perms)
- OPERADOR_ACAO: view configs/negócio + add/view filhas (15 perms)
- CONSULTOR_PNGI: view em tudo (11 perms)

USO:
    python acoes_pngi/tests/fix_coordenador_tests.py
"""

import re
from pathlib import Path


def fix_eixo_tests(content):
    """Corrige testes de Eixo para COORDENADOR_PNGI."""
    
    # 1. test_coordenador_can_create_eixo -> test_coordenador_cannot_create_eixo
    content = re.sub(
        r'def test_coordenador_can_create_eixo\(self\):\s+'
        r'"""COORDENADOR_PNGI pode criar eixo"""\s+'
        r'self\.authenticate_as\(\'coordenador\'\)\s+'
        r'data = \{[^}]+\}\s+'
        r'response = self\.client\.post\(\'/api/v1/acoes_pngi/eixos/\', data, format=\'json\'\)\s+'
        r'self\.assertEqual\(response\.status_code, status\.HTTP_201_CREATED\)\s+'
        r'self\.assertEqual\(response\.data\[\'strdescricaoeixo\'\], \'Novo Eixo Coordenador\'\)\s+'
        r'self\.assertEqual\(response\.data\[\'stralias\'\], \'NCOOR\'\)',
        
        '''def test_coordenador_cannot_create_eixo(self):
        """COORDENADOR_PNGI NÃO pode criar eixo (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {
            'strdescricaoeixo': 'Tentativa Coordenador',
            'stralias': 'NCOOR'
        }
        response = self.client.post('/api/v1/acoes_pngi/eixos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)''',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # 2. test_coordenador_can_update_eixo -> test_coordenador_cannot_update_eixo
    content = re.sub(
        r'def test_coordenador_can_update_eixo\(self\):\s+'
        r'"""COORDENADOR_PNGI pode atualizar eixo"""\s+'
        r'self\.authenticate_as\(\'coordenador\'\)\s+'
        r'data = \{\'strdescricaoeixo\': \'Eixo Atualizado pelo Coordenador\'\}\s+'
        r'response = self\.client\.patch\(\s+'
        r'f\'/api/v1/acoes_pngi/eixos/\{self\.eixo\.ideixo\}/\',\s+'
        r'data,\s+'
        r'format=\'json\'\s+'
        r'\)\s+'
        r'self\.assertEqual\(response\.status_code, status\.HTTP_200_OK\)\s+'
        r'self\.assertEqual\(response\.data\[\'strdescricaoeixo\'\], \'Eixo Atualizado pelo Coordenador\'\)',
        
        '''def test_coordenador_cannot_update_eixo(self):
        """COORDENADOR_PNGI NÃO pode atualizar eixo (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {'strdescricaoeixo': 'Tentativa Update'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)''',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # 3. test_coordenador_can_delete_eixo -> test_coordenador_cannot_delete_eixo
    content = re.sub(
        r'def test_coordenador_can_delete_eixo\(self\):\s+'
        r'"""COORDENADOR_PNGI pode deletar eixo"""\s+'
        r'# Criar eixo temporário para deletar\s+'
        r'eixo_temp = Eixo\.objects\.create\([^)]+\)\s+'
        r'\s+'
        r'self\.authenticate_as\(\'coordenador\'\)\s+'
        r'response = self\.client\.delete\(f\'/api/v1/acoes_pngi/eixos/\{eixo_temp\.ideixo\}/\'\)\s+'
        r'self\.assertEqual\(response\.status_code, status\.HTTP_204_NO_CONTENT\)\s+'
        r'\s+'
        r'# Verificar que foi deletado\s+'
        r'self\.assertFalse\(Eixo\.objects\.filter\(ideixo=eixo_temp\.ideixo\)\.exists\(\)\)',
        
        '''def test_coordenador_cannot_delete_eixo(self):
        """COORDENADOR_PNGI NÃO pode deletar eixo (apenas view em configs)"""
        self.authenticate_as('coordenador')
        response = self.client.delete(f'/api/v1/acoes_pngi/eixos/{self.eixo.ideixo}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)''',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    return content


def fix_situacao_tests(content):
    """Corrige testes de SituacaoAcao para COORDENADOR_PNGI."""
    
    # 1. test_coordenador_can_create_situacao -> test_coordenador_cannot_create_situacao
    content = re.sub(
        r'def test_coordenador_can_create_situacao\(self\):\s+'
        r'"""COORDENADOR_PNGI pode criar situação"""\s+'
        r'self\.authenticate_as\(\'coordenador\'\)\s+'
        r'data = \{\'strdescricaosituacao\': \'CONCLUIDA\'\}\s+'
        r'response = self\.client\.post\(\'/api/v1/acoes_pngi/situacoes/\', data, format=\'json\'\)\s+'
        r'self\.assertEqual\(response\.status_code, status\.HTTP_201_CREATED\)',
        
        '''def test_coordenador_cannot_create_situacao(self):
        """COORDENADOR_PNGI NÃO pode criar situação (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {'strdescricaosituacao': 'CONCLUIDA'}
        response = self.client.post('/api/v1/acoes_pngi/situacoes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)''',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # 2. test_coordenador_can_update_situacao -> test_coordenador_cannot_update_situacao
    content = re.sub(
        r'def test_coordenador_can_update_situacao\(self\):\s+'
        r'"""COORDENADOR_PNGI pode atualizar situação"""\s+'
        r'self\.authenticate_as\(\'coordenador\'\)\s+'
        r'data = \{\'strdescricaosituacao\': \'ATUALIZADA\'\}\s+'
        r'response = self\.client\.patch\(\s+'
        r'f\'/api/v1/acoes_pngi/situacoes/\{self\.situacao\.idsituacaoacao\}/\',\s+'
        r'data,\s+'
        r'format=\'json\'\s+'
        r'\)\s+'
        r'self\.assertEqual\(response\.status_code, status\.HTTP_200_OK\)',
        
        '''def test_coordenador_cannot_update_situacao(self):
        """COORDENADOR_PNGI NÃO pode atualizar situação (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {'strdescricaosituacao': 'ATUALIZADA'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/situacoes/{self.situacao.idsituacaoacao}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)''',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # 3. test_coordenador_can_delete_situacao -> test_coordenador_cannot_delete_situacao
    content = re.sub(
        r'def test_coordenador_can_delete_situacao\(self\):\s+'
        r'"""COORDENADOR_PNGI pode deletar situação"""\s+'
        r'situacao_temp = SituacaoAcao\.objects\.create\(strdescricaosituacao=\'TEMP\'\)\s+'
        r'\s+'
        r'self\.authenticate_as\(\'coordenador\'\)\s+'
        r'response = self\.client\.delete\(f\'/api/v1/acoes_pngi/situacoes/\{situacao_temp\.idsituacaoacao\}/\'\)\s+'
        r'self\.assertEqual\(response\.status_code, status\.HTTP_204_NO_CONTENT\)',
        
        '''def test_coordenador_cannot_delete_situacao(self):
        """COORDENADOR_PNGI NÃO pode deletar situação (apenas view em configs)"""
        self.authenticate_as('coordenador')
        response = self.client.delete(f'/api/v1/acoes_pngi/situacoes/{self.situacao.idsituacaoacao}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)''',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    return content


def fix_vigencia_tests(content):
    """Corrige testes de VigenciaPNGI para COORDENADOR_PNGI."""
    
    # 1. test_coordenador_can_create_vigencia -> test_coordenador_cannot_create_vigencia
    content = re.sub(
        r'def test_coordenador_can_create_vigencia\(self\):\s+'
        r'"""COORDENADOR_PNGI pode criar vigência"""\s+'
        r'self\.authenticate_as\(\'coordenador\'\)\s+'
        r'data = \{[^}]+\}\s+'
        r'response = self\.client\.post\(\'/api/v1/acoes_pngi/vigencias/\', data, format=\'json\'\)\s+'
        r'self\.assertEqual\(response\.status_code, status\.HTTP_201_CREATED\)',
        
        '''def test_coordenador_cannot_create_vigencia(self):
        """COORDENADOR_PNGI NÃO pode criar vigência (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {
            'strdescricaovigenciapngi': 'PNGI 2027',
            'datiniciovigencia': '2027-01-01',
            'datfinalvigencia': '2027-12-31',
            'isvigenciaativa': False
        }
        response = self.client.post('/api/v1/acoes_pngi/vigencias/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)''',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # 2. test_coordenador_can_update_vigencia -> test_coordenador_cannot_update_vigencia
    content = re.sub(
        r'def test_coordenador_can_update_vigencia\(self\):\s+'
        r'"""COORDENADOR_PNGI pode atualizar vigência"""\s+'
        r'self\.authenticate_as\(\'coordenador\'\)\s+'
        r'data = \{\'strdescricaovigenciapngi\': \'PNGI 2026 - Atualizado\'\}\s+'
        r'response = self\.client\.patch\(\s+'
        r'f\'/api/v1/acoes_pngi/vigencias/\{self\.vigencia\.idvigenciapngi\}/\',\s+'
        r'data,\s+'
        r'format=\'json\'\s+'
        r'\)\s+'
        r'self\.assertEqual\(response\.status_code, status\.HTTP_200_OK\)',
        
        '''def test_coordenador_cannot_update_vigencia(self):
        """COORDENADOR_PNGI NÃO pode atualizar vigência (apenas view em configs)"""
        self.authenticate_as('coordenador')
        data = {'strdescricaovigenciapngi': 'PNGI 2026 - Atualizado'}
        response = self.client.patch(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)''',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # 3. test_coordenador_can_delete_vigencia -> test_coordenador_cannot_delete_vigencia
    content = re.sub(
        r'def test_coordenador_can_delete_vigencia\(self\):\s+'
        r'"""COORDENADOR_PNGI pode deletar vigência"""\s+'
        r'vigencia_temp = VigenciaPNGI\.objects\.create\([^)]+\)\s+'
        r'\s+'
        r'self\.authenticate_as\(\'coordenador\'\)\s+'
        r'response = self\.client\.delete\(\s+'
        r'f\'/api/v1/acoes_pngi/vigencias/\{vigencia_temp\.idvigenciapngi\}/\'\s+'
        r'\)\s+'
        r'self\.assertEqual\(response\.status_code, status\.HTTP_204_NO_CONTENT\)',
        
        '''def test_coordenador_cannot_delete_vigencia(self):
        """COORDENADOR_PNGI NÃO pode deletar vigência (apenas view em configs)"""
        self.authenticate_as('coordenador')
        response = self.client.delete(
            f'/api/v1/acoes_pngi/vigencias/{self.vigencia.idvigenciapngi}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)''',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    return content


def main():
    """Executa correções nos testes."""
    test_file = Path(__file__).parent / 'test_api_views.py'
    
    print(f"📂 Lendo arquivo: {test_file}")
    content = test_file.read_text(encoding='utf-8')
    
    print("🔧 Aplicando correções...")
    
    # Eixo
    print("  - Corrigindo testes de Eixo...")
    content = fix_eixo_tests(content)
    
    # SituacaoAcao
    print("  - Corrigindo testes de SituacaoAcao...")
    content = fix_situacao_tests(content)
    
    # VigenciaPNGI
    print("  - Corrigindo testes de VigenciaPNGI...")
    content = fix_vigencia_tests(content)
    
    # Salvar
    print(f"💾 Salvando alterações em: {test_file}")
    test_file.write_text(content, encoding='utf-8')
    
    print("✅ Correções aplicadas com sucesso!")
    print("\n📋 RESUMO DAS MUDANÇAS:")
    print("   - COORDENADOR NÃO pode criar/editar/deletar CONFIGS")
    print("   - COORDENADOR pode apenas VIEW em CONFIGS")
    print("   - GESTOR tem CRUD completo em CONFIGS")
    print("\n🧪 Rode os testes:")
    print("   python manage.py test acoes_pngi.tests.test_api_views")


if __name__ == '__main__':
    main()
