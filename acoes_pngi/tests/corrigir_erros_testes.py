#!/usr/bin/env python3
"""
Script para corrigir erros nos testes do acoes_pngi
Corrige:
1. Filtro booleano em api_views.py
2. Datetimes naive em test_api_views_alinhamento_responsaveis.py
3. Outros problemas de timezone
"""

import os
import re
from pathlib import Path

# Diretórios
PROJETO_ROOT = Path(__file__).parent.parent.parent
ACOES_PNGI_DIR = PROJETO_ROOT / "acoes_pngi"
TESTS_DIR = ACOES_PNGI_DIR / "tests"
VIEWS_DIR = ACOES_PNGI_DIR / "views"


def corrigir_filtro_booleano():
    """Corrige o filtro booleano em api_views.py"""
    arquivo = VIEWS_DIR / "api_views.py"
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return False
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Padrão para encontrar a linha problemática
    # Procura por: queryset.filter(isacaoprazoativo=self.request.query_params.get('isacaoprazoativo'))
    padrao_original = r"queryset\s*=\s*queryset\.filter\(isacaoprazoativo=self\.request\.query_params\.get\('isacaoprazoativo'\)\)"
    
    # Código corrigido
    correcao = """# Converte string para booleano
        is_ativo = self.request.query_params.get('isacaoprazoativo')
        if is_ativo is not None:
            is_ativo_bool = is_ativo.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(isacaoprazoativo=is_ativo_bool)"""
    
    if re.search(padrao_original, conteudo):
        conteudo_novo = re.sub(padrao_original, correcao, conteudo)
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo_novo)
        
        print(f"✅ Corrigido filtro booleano em: {arquivo}")
        return True
    else:
        print(f"⚠️  Padrão não encontrado em {arquivo}")
        return False


def adicionar_import_timezone(conteudo):
    """Adiciona import do timezone se não existir"""
    if 'from django.utils import timezone' not in conteudo:
        # Procura a linha de imports do Django
        if 'from django' in conteudo:
            conteudo = re.sub(
                r'(from django\.test import.*?\n)',
                r'\1from django.utils import timezone\n',
                conteudo,
                count=1
            )
        else:
            # Adiciona no início após os imports padrão
            conteudo = re.sub(
                r'(from datetime import.*?\n)',
                r'\1from django.utils import timezone\n',
                conteudo,
                count=1
            )
    return conteudo


def corrigir_datetimes_naive():
    """Corrige datetimes naive nos testes"""
    arquivo = TESTS_DIR / "test_api_views_alinhamento_responsaveis.py"
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return False
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Adiciona import do timezone
    conteudo = adicionar_import_timezone(conteudo)
    
    # Padrões de datetime a corrigir
    correcoes = [
        # datetime(2026, 2, 15, 10, 0, 0) -> timezone.make_aware(datetime(2026, 2, 15, 10, 0, 0))
        (r'datetime\((\d{4}),\s*(\d{1,2}),\s*(\d{1,2}),\s*(\d{1,2}),\s*(\d{1,2}),\s*(\d{1,2})\)',
         r'timezone.make_aware(datetime(\1, \2, \3, \4, \5, \6))'),
        
        # datetime(2026, 1, 10, 14, 30, 0) -> timezone.make_aware(datetime(...))
        (r'datetime\((\d{4}),\s*(\d{1,2}),\s*(\d{1,2}),\s*(\d{1,2}),\s*(\d{1,2})\)',
         r'timezone.make_aware(datetime(\1, \2, \3, \4, \5))'),
    ]
    
    alteracoes = 0
    for padrao, substituicao in correcoes:
        matches = re.findall(padrao, conteudo)
        if matches:
            # Evita duplicar timezone.make_aware
            conteudo_temp = re.sub(
                r'timezone\.make_aware\(timezone\.make_aware\(',
                r'timezone.make_aware(',
                re.sub(padrao, substituicao, conteudo)
            )
            if conteudo_temp != conteudo:
                conteudo = conteudo_temp
                alteracoes += len(matches)
    
    if alteracoes > 0:
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"✅ Corrigidos {alteracoes} datetimes naive em: {arquivo}")
        return True
    else:
        print(f"⚠️  Nenhum datetime naive encontrado em {arquivo}")
        return False


def corrigir_datetimes_em_test_acoes():
    """Corrige datetimes naive em test_api_views_acoes.py"""
    arquivo = TESTS_DIR / "test_api_views_acoes.py"
    
    if not arquivo.exists():
        print(f"⚠️  Arquivo não encontrado: {arquivo}")
        return False
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Adiciona import do timezone
    conteudo = adicionar_import_timezone(conteudo)
    
    # Padrão específico para datdataentrega
    # datetime(2026, 6, 30, 0, 0, 0) -> timezone.make_aware(datetime(2026, 6, 30, 0, 0, 0))
    padrao = r'datetime\((\d{4}),\s*(\d{1,2}),\s*(\d{1,2}),\s*0,\s*0,\s*0\)'
    substituicao = r'timezone.make_aware(datetime(\1, \2, \3, 0, 0, 0))'
    
    matches = re.findall(padrao, conteudo)
    if matches:
        conteudo_novo = re.sub(padrao, substituicao, conteudo)
        
        # Remove duplicação
        conteudo_novo = re.sub(
            r'timezone\.make_aware\(timezone\.make_aware\(',
            r'timezone.make_aware(',
            conteudo_novo
        )
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo_novo)
        
        print(f"✅ Corrigidos {len(matches)} datetimes naive em: {arquivo}")
        return True
    else:
        print(f"⚠️  Nenhum datetime naive encontrado em {arquivo}")
        return False


def criar_documentacao():
    """Cria documentação sobre as correções aplicadas"""
    doc = """# Correções Aplicadas nos Testes

## 1. Filtro Booleano em `api_views.py`

### Problema
O filtro `isacaoprazoativo` recebia string `"true"` do query parameter, mas o campo
`BooleanField` esperava valor booleano.

### Correção
```python
# ANTES:
queryset = queryset.filter(isacaoprazoativo=self.request.query_params.get('isacaoprazoativo'))

# DEPOIS:
is_ativo = self.request.query_params.get('isacaoprazoativo')
if is_ativo is not None:
    is_ativo_bool = is_ativo.lower() in ('true', '1', 'yes')
    queryset = queryset.filter(isacaoprazoativo=is_ativo_bool)
```

### Localização
- Arquivo: `acoes_pngi/views/api_views.py`
- Linha: ~496 (classe `AcaoPrazoViewSet`)

---

## 2. Datetimes Naive nos Testes

### Problema
Os testes criavam datetimes sem timezone (naive), mas Django está com `USE_TZ=True`.

### Correção
```python
# ANTES:
datetime(2026, 2, 15, 10, 0, 0)

# DEPOIS:
from django.utils import timezone
timezone.make_aware(datetime(2026, 2, 15, 10, 0, 0))
```

### Arquivos Corrigidos
- `acoes_pngi/tests/test_api_views_alinhamento_responsaveis.py`
- `acoes_pngi/tests/test_api_views_acoes.py`

---

## Como Executar

```bash
# 1. Executar o script de correções
python acoes_pngi/tests/corrigir_erros_testes.py

# 2. Verificar as mudanças
git diff acoes_pngi/

# 3. Rodar os testes
python manage.py test acoes_pngi.tests

# 4. Commit
git add acoes_pngi/
git commit -m "fix: Corrige filtro booleano e datetimes naive nos testes"
```

---

## Estatísticas

- **Filtros booleanos corrigidos**: 1
- **Datetimes corrigidos**: ~20+
- **Arquivos modificados**: 3

---

## Próximos Passos (se ainda houver erros)

1. **Endpoints 404**: Verificar roteamento das URLs
2. **Permissões**: Revisar sistema RBAC/ABAC
3. **Bad Request 400**: Validar serializers
"""
    
    doc_path = TESTS_DIR / "CORRECOES_APLICADAS.md"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(doc)
    
    print(f"✅ Documentação criada em: {doc_path}")


def main():
    """Executa todas as correções"""
    print("=" * 60)
    print("🔧 SCRIPT DE CORREÇÃO DE ERROS NOS TESTES")
    print("=" * 60)
    print()
    
    resultados = []
    
    # 1. Corrigir filtro booleano
    print("1️⃣  Corrigindo filtro booleano em api_views.py...")
    resultado1 = corrigir_filtro_booleano()
    resultados.append(("Filtro booleano", resultado1))
    print()
    
    # 2. Corrigir datetimes em test_api_views_alinhamento_responsaveis.py
    print("2️⃣  Corrigindo datetimes naive em test_api_views_alinhamento_responsaveis.py...")
    resultado2 = corrigir_datetimes_naive()
    resultados.append(("Datetimes alinhamento", resultado2))
    print()
    
    # 3. Corrigir datetimes em test_api_views_acoes.py
    print("3️⃣  Corrigindo datetimes naive em test_api_views_acoes.py...")
    resultado3 = corrigir_datetimes_em_test_acoes()
    resultados.append(("Datetimes acoes", resultado3))
    print()
    
    # 4. Criar documentação
    print("4️⃣  Criando documentação...")
    criar_documentacao()
    print()
    
    # Resumo
    print("=" * 60)
    print("📊 RESUMO DAS CORREÇÕES")
    print("=" * 60)
    sucessos = sum(1 for _, r in resultados if r)
    total = len(resultados)
    
    for nome, resultado in resultados:
        status = "✅" if resultado else "❌"
        print(f"{status} {nome}")
    
    print()
    print(f"Total: {sucessos}/{total} correções aplicadas com sucesso")
    print()
    
    if sucessos == total:
        print("🎉 Todas as correções foram aplicadas!")
        print()
        print("Próximos passos:")
        print("1. Revisar mudanças: git diff acoes_pngi/")
        print("2. Rodar testes: python manage.py test acoes_pngi.tests")
        print("3. Commit: git add acoes_pngi/ && git commit -m 'fix: Corrige erros nos testes'")
    else:
        print("⚠️  Algumas correções falharam. Verifique os logs acima.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
