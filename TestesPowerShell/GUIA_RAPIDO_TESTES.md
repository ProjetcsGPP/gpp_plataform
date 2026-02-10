# 🚀 Guia Rápido - Testes Ações PNGI

## ⚡ Execução Rápida

### 1️⃣ Testes Unitários Python (Django)

```bash
# Navegar para raiz do projeto
cd C:\Projects\gpp_plataform

# Ativar virtualenv
.\venv\Scripts\Activate.ps1

# Executar todos os testes
python manage.py test acoes_pngi

# Executar com verbose
python manage.py test acoes_pngi -v 2

# Executar apenas testes de models
python manage.py test acoes_pngi.tests.test_models

# Executar apenas testes de permissões
python manage.py test acoes_pngi.tests.test_permissions
```

### 2️⃣ Teste Completo Web + API (PowerShell)

```powershell
cd C:\Projects\gpp_plataform\TestesPowerShell

# Teste COMPLETO (RECOMENDADO)
.\Test-AcoesPNGI-Complete-v2.ps1

# Com verbose para debug
.\Test-AcoesPNGI-Complete-v2.ps1 -Verbose

# Para servidor diferente
.\Test-AcoesPNGI-Complete-v2.ps1 -BaseURL "http://192.168.1.100:8000"
```

### 3️⃣ Teste das Novas Tabelas

```powershell
# Foco em Ações, Prazos, Destaques, Alinhamento, Responsáveis
.\Test-AcoesPNGI-NewTables.ps1

# Com token JWT para testes autenticados
$token = "eyJhbGc..."
.\Test-AcoesPNGI-NewTables.ps1 -Token $token
```

### 4️⃣ Teste de Permissões

```powershell
# Teste interativo com solicitação de credenciais
.\Test-AcoesPNGI-Permissions-v2.ps1

# Será solicitado:
# Email: seu.email@seger.es.gov.br
# Senha: ******** (SecureString)
```

---

## 🎯 Workflows Recomendados

### Durante Desenvolvimento

```bash
# 1. Testes unitários rápidos
python manage.py test acoes_pngi.tests.test_models -v 2

# 2. Se passou, testar API
powershell -File .\TestesPowerShell\Test-AcoesPNGI-NewTables.ps1
```

### Antes de Commit

```bash
# Testes unitários completos
python manage.py test acoes_pngi -v 2

# Se passou, teste completo
powershell -File .\TestesPowerShell\Test-AcoesPNGI-Complete-v2.ps1
```

### Antes de Deploy

```powershell
# 1. Testes unitários
python manage.py test acoes_pngi

# 2. Teste completo
.\Test-AcoesPNGI-Complete-v2.ps1

# 3. Teste de permissões com cada role
.\Test-AcoesPNGI-Permissions-v2.ps1
# (Testar com: COORDENADOR, GESTOR, OPERADOR, CONSULTOR)
```

---

## ✅ Checklist de Teste

### Testes Básicos
- [ ] Testes unitários passaram
- [ ] Servidor Django está rodando
- [ ] Endpoints API respondem (200/401/403)
- [ ] Views web renderizam (200/302)

### Testes Completos
- [ ] CRUD de Eixo funciona
- [ ] CRUD de Situação funciona
- [ ] CRUD de Vigência funciona
- [ ] CRUD de Ações funciona
- [ ] CRUD de Prazos funciona
- [ ] CRUD de Destaques funciona
- [ ] Custom actions funcionam
- [ ] Filtros funcionam
- [ ] Busca funciona

### Testes de Permissões
- [ ] COORDENADOR: Acesso total
- [ ] GESTOR: Acesso total ações
- [ ] OPERADOR: Operações básicas
- [ ] CONSULTOR: Apenas leitura

---

## 🐞 Debug de Erros Comuns

### Erro: "manage.py não encontrado"
```bash
# Certifique-se de estar na raiz
cd C:\Projects\gpp_plataform
pwd  # Deve mostrar: C:\Projects\gpp_plataform
```

### Erro: "Servidor não responde"
```bash
# Terminal 1: Iniciar servidor
python manage.py runserver

# Terminal 2: Executar testes
powershell .\TestesPowerShell\Test-AcoesPNGI-Complete-v2.ps1
```

### Erro: "Token inválido"
```bash
# Verificar:
1. Email e senha corretos
2. Usuário tem role configurado
3. Aplicação ACOES_PNGI existe
4. Role está ativo
```

### Erro: "404 em custom actions"
```
Algumas actions retornam 404 se não houver dados:
- /vigencias/vigencia_ativa/ - OK se nenhuma vigência ativa
- /prazos/ativos/ - OK se nenhum prazo ativo

Isso é NORMAL e não indica erro.
```

---

## 📊 Saída Esperada

### Testes Unitários
```
Creating test database...
...................................
----------------------------------------------------------------------
Ran 35 tests in 2.345s

OK
```

### Teste Completo v2
```
══════════════════════════════
 RESUMO FINAL
══════════════════════════════

✓ Unit Tests: PASSOU
✓ Web Views:  3 passou, 0 falhou
✓ API CRUD:   11 passou, 0 falhou
✓ Actions:    4 passou, 0 falhou

Total: 18 testes passados
🎉 TODOS OS TESTES PASSARAM!
```

### Teste de Permissões
```
══════════════════════════════
 AUTENTICAÇÃO
══════════════════════════════
Email: gestor@seger.es.gov.br
✓ Token JWT obtido com sucesso

══════════════════════════════
 TESTANDO EIXO
══════════════════════════════

--- Listar Eixo ---
GET /api/v1/acoes_pngi/eixos/
✓ Sucesso (Status 200-299)

...

🎉 Todos os testes de permissões foram executados!
```

---

## 📚 Documentação Completa

- [README Testes Completo](./README_ACOES_PNGI_TESTS.md)
- [Troubleshooting](./README_TROUBLESHOOTING.md)
- [Comandos de Execução](./COMANDOS_EXECUCAO.md)

---

## 🔗 Links Úteis

- [Documentação Ações PNGI](../acoes_pngi/README.md)
- [Sistema de Permissões](../acoes_pngi/permissions.py)
- [Views API](../acoes_pngi/views/api_views/)
- [Models](../acoes_pngi/models/)

---

**⚡ Dica Final:** Execute o teste completo (`Test-AcoesPNGI-Complete-v2.ps1`) regularmente para garantir que tudo está funcionando!
