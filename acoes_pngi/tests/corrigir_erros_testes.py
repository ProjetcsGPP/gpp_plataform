#!/usr/bin/env python3
"""
Script para corrigir erros nos testes do acoes_pngi
Corrige:
1. Filtro booleano em api_views.py
2. Datetimes naive (incluindo datetime.now())
3. Imports de timezone
"""

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

    with open(arquivo, encoding="utf-8") as f:
        conteudo = f.read()

    # Padrão mais flexível para encontrar a linha problemática
    padrao_original = r"queryset\s*=\s*queryset\.filter\(\s*isacaoprazoativo\s*=\s*self\.request\.query_params\.get\(\s*['\"]isacaoprazoativo['\"]\s*\)\s*\)"

    # Código corrigido
    correcao = """# Converte string para booleano
        is_ativo = self.request.query_params.get('isacaoprazoativo')
        if is_ativo is not None:
            is_ativo_bool = is_ativo.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(isacaoprazoativo=is_ativo_bool)"""

    if re.search(padrao_original, conteudo):
        conteudo_novo = re.sub(padrao_original, correcao, conteudo)

        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo_novo)

        print(f"✅ Corrigido filtro booleano em: {arquivo}")
        return True
    else:
        print(f"⚠️  Filtro booleano já corrigido ou padrão não encontrado em {arquivo}")
        return False


def adicionar_import_timezone(conteudo):
    """Adiciona import do timezone se não existir"""
    if "from django.utils import timezone" in conteudo:
        return conteudo, False

    # Procura imports do Django
    if "from datetime import" in conteudo:
        conteudo = re.sub(
            r"(from datetime import [^\n]+)",
            r"\1\nfrom django.utils import timezone",
            conteudo,
            count=1,
        )
        return conteudo, True
    elif "from django" in conteudo:
        conteudo = re.sub(
            r"(from django\.test import [^\n]+)",
            r"\1\nfrom django.utils import timezone",
            conteudo,
            count=1,
        )
        return conteudo, True

    return conteudo, False


def corrigir_datetime_now():
    """Corrige datetime.now() para timezone.now() em todos os arquivos de teste"""
    arquivos_corrigidos = 0
    total_substituicoes = 0

    for arquivo_path in TESTS_DIR.glob("test_*.py"):
        with open(arquivo_path, encoding="utf-8") as f:
            conteudo = f.read()

        conteudo_original = conteudo

        # Adicionar import se necessário
        conteudo, import_adicionado = adicionar_import_timezone(conteudo)

        # Substituir datetime.now() por timezone.now()
        # Padrões:
        # 1. datetime.now() -> timezone.now()
        # 2. (datetime.now()) -> (timezone.now())
        substituicoes_now = len(re.findall(r"datetime\.now\(\)", conteudo))
        conteudo = re.sub(r"\bdatetime\.now\(\)", r"timezone.now()", conteudo)

        if conteudo != conteudo_original:
            with open(arquivo_path, "w", encoding="utf-8") as f:
                f.write(conteudo)

            arquivos_corrigidos += 1
            total_substituicoes += substituicoes_now
            print(
                f"  ✅ {arquivo_path.name}: {substituicoes_now} datetime.now() corrigidos"
            )
            if import_adicionado:
                print("     ✅ Import timezone adicionado")

    if arquivos_corrigidos > 0:
        print(
            f"\n✅ Total: {arquivos_corrigidos} arquivo(s), {total_substituicoes} correções"
        )
        return True
    else:
        print("⚠️  Nenhum datetime.now() encontrado para corrigir")
        return False


def corrigir_datetimes_estaticos():
    """Corrige datetimes estáticos como datetime(2026, 2, 15, 10, 0, 0)"""
    arquivos_corrigidos = 0
    total_substituicoes = 0

    # Padrões de datetime estáticos
    padroes = [
        # datetime(2026, 2, 15, 10, 0, 0)
        (
            r"\bdatetime\((\d{4}),\s*(\d{1,2}),\s*(\d{1,2}),\s*(\d{1,2}),\s*(\d{1,2}),\s*(\d{1,2})\)",
            r"timezone.make_aware(datetime(\1, \2, \3, \4, \5, \6))",
        ),
        # datetime(2026, 1, 10, 14, 30)
        (
            r"\bdatetime\((\d{4}),\s*(\d{1,2}),\s*(\d{1,2}),\s*(\d{1,2}),\s*(\d{1,2})\)(?!,)",
            r"timezone.make_aware(datetime(\1, \2, \3, \4, \5))",
        ),
    ]

    for arquivo_path in TESTS_DIR.glob("test_*.py"):
        with open(arquivo_path, encoding="utf-8") as f:
            conteudo = f.read()

        conteudo_original = conteudo

        # Adicionar import se necessário
        conteudo, import_adicionado = adicionar_import_timezone(conteudo)

        # Aplicar correções
        substituicoes_arquivo = 0
        for padrao, substituicao in padroes:
            matches = re.findall(padrao, conteudo)
            if matches:
                # Evita duplicar timezone.make_aware
                conteudo_temp = re.sub(padrao, substituicao, conteudo)
                # Remove duplicações
                conteudo_temp = re.sub(
                    r"timezone\.make_aware\(timezone\.make_aware\(",
                    r"timezone.make_aware(",
                    conteudo_temp,
                )
                if conteudo_temp != conteudo:
                    substituicoes_arquivo += len(matches)
                    conteudo = conteudo_temp

        if conteudo != conteudo_original:
            with open(arquivo_path, "w", encoding="utf-8") as f:
                f.write(conteudo)

            arquivos_corrigidos += 1
            total_substituicoes += substituicoes_arquivo
            if substituicoes_arquivo > 0:
                print(
                    f"  ✅ {arquivo_path.name}: {substituicoes_arquivo} datetimes estáticos corrigidos"
                )
            if import_adicionado:
                print("     ✅ Import timezone adicionado")

    if arquivos_corrigidos > 0:
        print(
            f"\n✅ Total: {arquivos_corrigidos} arquivo(s), {total_substituicoes} correções"
        )
        return True
    else:
        print("⚠️  Nenhum datetime estático encontrado para corrigir")
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
Os testes usavam `datetime.now()` e `datetime(...)` sem timezone, mas Django está com `USE_TZ=True`.

### Correções Aplicadas

#### A. datetime.now()
```python
# ANTES:
from datetime import datetime
datdataanotacaoalinhamento=datetime.now()

# DEPOIS:
from django.utils import timezone
datdataanotacaoalinhamento=timezone.now()
```

#### B. Datetimes estáticos
```python
# ANTES:
datetime(2026, 2, 15, 10, 0, 0)

# DEPOIS:
from django.utils import timezone
timezone.make_aware(datetime(2026, 2, 15, 10, 0, 0))
```

### Arquivos Corrigidos
- Todos os arquivos `test_*.py` em `acoes_pngi/tests/`

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
- **datetime.now() corrigidos**: Varia por arquivo
- **Datetimes estáticos corrigidos**: Varia por arquivo
- **Imports timezone adicionados**: Automático

---

## Próximos Passos (se ainda houver erros)

1. **Endpoints 404**: Verificar roteamento das URLs
2. **Permissões**: Revisar sistema RBAC/ABAC
3. **Bad Request 400**: Validar serializers
"""

    doc_path = TESTS_DIR / "CORRECOES_APLICADAS.md"
    with open(doc_path, "w", encoding="utf-8") as f:
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

    # 2. Corrigir datetime.now()
    print("2️⃣  Corrigindo datetime.now() em arquivos de teste...")
    resultado2 = corrigir_datetime_now()
    resultados.append(("datetime.now()", resultado2))
    print()

    # 3. Corrigir datetimes estáticos
    print("3️⃣  Corrigindo datetimes estáticos...")
    resultado3 = corrigir_datetimes_estaticos()
    resultados.append(("Datetimes estáticos", resultado3))
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
        status = "✅" if resultado else "⚠️ "
        print(f"{status} {nome}")

    print()
    print(f"Total: {sucessos}/{total} tipos de correção aplicados")
    print()

    if sucessos > 0:
        print("✅ Correções aplicadas com sucesso!")
        print()
        print("Próximos passos:")
        print("1. Revisar mudanças: git diff acoes_pngi/")
        print("2. Rodar testes: python manage.py test acoes_pngi.tests")
        print(
            "3. Commit: git add acoes_pngi/ && git commit -m 'fix: Corrige erros nos testes'"
        )
    else:
        print("⚠️  Nenhuma correção foi necessária ou já foram aplicadas.")

    print("=" * 60)


if __name__ == "__main__":
    main()
