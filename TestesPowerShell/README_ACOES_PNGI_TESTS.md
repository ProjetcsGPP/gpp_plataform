# Testes Automáticos - Ações PNGI

## 📝 Índice

- [Visão Geral](#visão-geral)
- [Scripts Disponíveis](#scripts-disponíveis)
- [Pré-requisitos](#pré-requisitos)
- [Como Executar](#como-executar)
- [Estrutura dos Testes](#estrutura-dos-testes)
- [Troubleshooting](#troubleshooting)

---

## 📋 Visão Geral

Conjunto completo de testes automatizados para a aplicação **Ações PNGI**, cobrindo:

- ✅ **Testes Unitários Django** (pytest/unittest)
- ✅ **Views Web** (renderização de templates)
- ✅ **APIs REST** (todos os endpoints CRUD)
- ✅ **Sistema de Permissões** (4 roles hierárquicos)
- ✅ **Novas Entidades** (Ações, Prazos, Destaques, etc)
- ✅ **Custom Actions** (endpoints especializados)

---

## 📋 Scripts Disponíveis

### 1. **Test-AcoesPNGI-Complete-v2.ps1**

**Teste mais completo e recomendado**

```powershell
.\Test-AcoesPNGI-Complete-v2.ps1
```

**O que testa:**
- Testes unitários Django
- Views Web (login, dashboard)
- Todos os endpoints API (11 entidades)
- Custom actions (list_light, vigencia_ativa, ativos)

**Quando usar:**
- Antes de fazer deploy
- Após alterações no código
- CI/CD pipeline

**Parâmetros:**
```powershell
-BaseURL "http://localhost:8000"  # URL do servidor
-APIVersion "v1"                  # Versão da API
-Verbose                          # Exibe detalhes
```

---

### 2. **Test-AcoesPNGI-NewTables.ps1**

**Foco nas novas entidades**

```powershell
.\Test-AcoesPNGI-NewTables.ps1
```

**O que testa:**
- ✅ Ações (com filtros: idvigenciapngi, search, ordering)
- ✅ Prazos (action: ativos, filtros: idacao, isacaoprazoativo)
- ✅ Destaques (filtros: idacao, ordenacao)
- ✅ Tipos de Anotação (search, ordering)
- ✅ Anotações de Alinhamento (filtros: idacao, idtipo)
- ✅ Usuários Responsáveis (filtros: strorgao, search)
- ✅ Relações Ação-Responsável (filtros: idacao)

**Quando usar:**
- Após criar/modificar as novas tabelas
- Testar filtros e buscas
- Verificar custom actions

**Parâmetros:**
```powershell
-BaseURL "http://localhost:8000"
-Token "seu-token-jwt"  # Opcional, para testes autenticados
```

---

### 3. **Test-AcoesPNGI-Permissions-v2.ps1**

**Teste de permissões hierárquicas**

```powershell
.\Test-AcoesPNGI-Permissions-v2.ps1
```

**O que testa:**
- Sistema de autenticação JWT
- Verificação dupla (JWT + banco)
- CRUD com validação de permissões
- 4 roles hierárquicos:
  - `COORDENADOR_PNGI`: Acesso total + gerencia config
  - `GESTOR_PNGI`: Acesso total às ações
  - `OPERADOR_ACAO`: Operações em ações
  - `CONSULTOR_PNGI`: Apenas leitura

**Quando usar:**
- Após mudanças no sistema de permissões
- Validar roles de novos usuários
- Teste de segurança

**Requer:**
- Email e senha de usuário válido
- Solicita credenciais interativamente

---

### 4. **Test-AcoesPNGI-Fast.ps1** (existente)

**Teste rápido das entidades core**

```powershell
.\Test-AcoesPNGI-Fast.ps1
```

**O que testa:**
- Eixo, Situação, Vigência (endpoints básicos)

**Quando usar:**
- Testes rápidos durante desenvolvimento
- Verificação rápida de funcionalidade

---

## ⚙️ Pré-requisitos

### 1. Ambiente Python

```bash
# Virtualenv ativado
cd C:\Projects\gpp_plataform
.\venv\Scripts\Activate.ps1

# Servidor Django rodando
python manage.py runserver
```

### 2. Dados de Teste

**Para testes completos, certifique-se de ter:**
- Pelo menos 1 vigência cadastrada
- Pelo menos 1 eixo cadastrado
- Pelo menos 1 usuário responsável (opcional)

**Criar dados via Django Admin ou shell:**

```python
python manage.py shell

from acoes_pngi.models import Eixo, VigenciaPNGI
from datetime import date

# Criar eixo
Eixo.objects.create(strdescricaoeixo="Teste", stralias="TST")

# Criar vigência
VigenciaPNGI.objects.create(
    strdescricaovigenciapngi="Vigência Teste 2026",
    datiniciovigencia=date(2026, 1, 1),
    datfinalvigencia=date(2026, 12, 31),
    isvigenciaativa=False
)
```

### 3. Permissões PowerShell

```powershell
# Permitir execução de scripts (admin)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🚀 Como Executar

### Teste Completo (Recomendado)

```powershell
cd C:\Projects\gpp_plataform\TestesPowerShell
.\Test-AcoesPNGI-Complete-v2.ps1
```

**Saída esperada:**
```
════════════════════════════════════════
 TESTE COMPLETO v2 - Ações PNGI v2 (acoes_pngi)
════════════════════════════════════════

✓ Unit Tests: PASSOU
✓ Web Views:  3 passou, 0 falhou
✓ API CRUD:   11 passou, 0 falhou
✓ Actions:    4 passou, 0 falhou

Total: 18 testes passaram

🎉 TODOS OS TESTES PASSARAM!
```

### Teste de Novas Tabelas

```powershell
.\Test-AcoesPNGI-NewTables.ps1
```

**Com token JWT:**
```powershell
$token = "eyJ..."
.\Test-AcoesPNGI-NewTables.ps1 -Token $token
```

### Teste de Permissões

```powershell
.\Test-AcoesPNGI-Permissions-v2.ps1
```

**O script solicitará:**
```
Email do usuário: seu.email@seger.es.gov.br
Senha: ********
```

---

## 📊 Estrutura dos Testes

### Entidades Testadas

#### Core (4)
- ✅ Eixo (`/eixos/`)
- ✅ Situação (`/situacoes/`)
- ✅ Vigência (`/vigencias/`)
- ✅ Tipo Entrave/Alerta (`/tipos-entrave-alerta/`)

#### Ações (3)
- ✅ Ações (`/acoes/`)
- ✅ Prazos (`/prazos/`)
- ✅ Destaques (`/destaques/`)

#### Alinhamento (2)
- ✅ Tipos de Anotação (`/tipos-anotacao-alinhamento/`)
- ✅ Anotações (`/anotacoes-alinhamento/`)

#### Responsáveis (2)
- ✅ Usuários Responsáveis (`/usuarios-responsaveis/`)
- ✅ Relações (`/relacoes-acao-responsavel/`)

**Total: 11 entidades**

### Operações Testadas

Para cada entidade:
1. **LIST** (GET) - Listar todos
2. **CREATE** (POST) - Criar novo registro
3. **RETRIEVE** (GET /id/) - Buscar por ID
4. **UPDATE** (PATCH /id/) - Atualizar parcial
5. **DELETE** (DELETE /id/) - Deletar registro

### Custom Actions Testadas

- `/eixos/list_light/` - Listagem otimizada
- `/vigencias/vigencia_ativa/` - Vigência ativa
- `/vigencias/vigente/` - Vigências vigentes
- `/vigencias/{id}/ativar/` - Ativar vigência
- `/prazos/ativos/` - Apenas prazos ativos
- `/acoes/{id}/prazos_ativos/` - Prazos de uma ação
- `/acoes/{id}/responsaveis_list/` - Responsáveis de uma ação

### Filtros Testados

**Ações:**
- `?search=termo` - Busca em apelido, descrição, entrega
- `?idvigenciapngi=1` - Filtrar por vigência
- `?idtipoentravealerta=1` - Filtrar por tipo
- `?ordering=strapelido` - Ordenar por campo

**Prazos:**
- `?idacao=1` - Filtrar por ação
- `?isacaoprazoativo=true` - Apenas ativos

**Alinhamento:**
- `?idacao=1` - Filtrar por ação
- `?idtipoanotacaoalinhamento=1` - Filtrar por tipo
- `?search=termo` - Busca em descrição

**Responsáveis:**
- `?strorgao=SEGER` - Filtrar por órgão
- `?search=nome` - Buscar por nome/email

---

## 🔧 Troubleshooting

### Erro: "manage.py não encontrado"

```powershell
# Navegue para raiz do projeto
cd C:\Projects\gpp_plataform

# Execute daqui
.\TestesPowerShell\Test-AcoesPNGI-Complete-v2.ps1
```

### Erro: "Virtualenv não encontrado"

```bash
# Crie o virtualenv
python -m venv venv

# Ative
.\venv\Scripts\Activate.ps1

# Instale dependências
pip install -r requirements.txt
```

### Erro: "Servidor não está rodando"

```bash
# Em outro terminal, inicie o servidor
python manage.py runserver
```

### Erro: "Token inválido" (Permissões)

```bash
# Verifique:
1. Email e senha corretos
2. Usuário tem role configurado
3. Aplicação ACOES_PNGI existe no banco
4. Role existe e está vinculado à aplicação
```

### Erro: 404 em custom actions

**Algumas actions retornam 404 se não houver dados:**
- `/vigencias/vigencia_ativa/` - Normal se nenhuma vigência ativa
- `/acoes/1/prazos_ativos/` - Normal se a ação não tem prazos ativos

Isso é **esperado** e não indica erro.

### Erro: IDs não encontrados

**Em Test-AcoesPNGI-NewTables.ps1**, ajuste os IDs conforme seus dados:

```powershell
# Edite o script e altere:
?idacao=1          # Para ID de ação existente
?idvigenciapngi=1  # Para ID de vigência existente
```

---

## 📚 Referências

- [Documentação Ações PNGI](../acoes_pngi/README.md)
- [Documentação de Views](../acoes_pngi/views/README.md)
- [Sistema de Permissões](../acoes_pngi/permissions.py)
- [API Endpoints](../acoes_pngi/urls/api_urls.py)

---

## ✅ Checklist de Testes

Antes de fazer deploy:

- [ ] Executar `Test-AcoesPNGI-Complete-v2.ps1`
- [ ] Todos os testes passaram
- [ ] Testar com cada role (Coordenador, Gestor, Operador, Consultor)
- [ ] Verificar logs do servidor
- [ ] Testar em ambiente de staging

---

**Última Atualização:** Fevereiro 2026
**Versão dos Testes:** 2.0
**Mantenedor:** Equipe GPP - SEGER/ES
