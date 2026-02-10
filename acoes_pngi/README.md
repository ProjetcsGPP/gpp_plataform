# Ações PNGI - Gestão de Ações do PNGI

Aplicação para gerenciamento de ações do Plano Nacional de Gestão da Inovação (PNGI) do Governo do Espírito Santo.

## 📋 Visão Geral

A aplicação **Ações PNGI** permite:

- Cadastro e gestão de **Eixos Estratégicos**
- Controle de **Situações de Ações**
- Gerenciamento de **Vigências do PNGI**
- Dashboard com estatísticas e visualizações
- APIs REST para integração com frontend Next.js

## 🏭 Estrutura

```
acoes_pngi/
├── models.py              # 11 modelos (Eixo, Situação, Vigência, Ações, etc)
├── serializers.py         # Serializers DRF
├── permissions.py         # Sistema de permissões por role
├── views/
│   ├── README.md           # Documentação de views
│   ├── api_views.py        # Arquivo de compatibilidade
│   ├── web_views.py        # Arquivo de compatibilidade
│   ├── api_views/          # Módulos API especializados
│   │   ├── auth_views.py
│   │   ├── core_views.py
│   │   ├── acoes_views.py
│   │   ├── alinhamento_views.py
│   │   └── responsavel_views.py
│   └── web_views/          # Módulos Web especializados
│       ├── core_web_views.py
│       ├── acoes_web_views.py
│       ├── alinhamento_web_views.py
│       └── responsavel_web_views.py
├── urls/
│   ├── api_urls.py         # Rotas da API
│   └── web_urls.py         # Rotas web
├── templates/
│   └── acoes_pngi/
├── admin.py               # Configuração do Django Admin
└── migrations/            # Migrações do banco
```

## 🔐 Sistema de Permissões

### Roles Disponíveis

A aplicação utiliza 4 perfis com permissões hierárquicas:

| Role               | Código            | Permissões                                     |
|--------------------|-------------------|-----------------------------------------------|
| Coordenador PNGI   | COORDENADOR_PNGI  | Acesso total + gerencia configurações        |
| Gestor PNGI        | GESTOR_PNGI       | Acesso total às ações                         |
| Operador Ação     | OPERADOR_ACAO     | Operações em ações (sem configurações)     |
| Consultor PNGI     | CONSULTOR_PNGI    | Apenas leitura (sem escrita)                  |

### Classes de Permissão

```python
from acoes_pngi.permissions import (
    IsAcoesPNGIUser,      # Base - qualquer perfil com acesso
    CanViewAcoesPngi,     # Leitura - todos os perfis
    CanEditAcoesPngi,     # Edição - Coordenador, Gestor, Operador
    CanManageAcoesPngi,   # Gerenciamento - Coordenador, Gestor
)
```

### Uso nas Views

```python
from rest_framework import viewsets
from acoes_pngi.permissions import CanEditAcoesPngi

class AcoesViewSet(viewsets.ModelViewSet):
    permission_classes = [CanEditAcoesPngi]
    queryset = Acoes.objects.all()
    # ...
```

### Verificação Dupla

O sistema implementa verificação em dois níveis:

1. **Via JWT** (`request.auth`):
   - Verifica roles no token
   - Valida atributos específicos

2. **Fallback via Banco**:
   - Consulta `accounts_aplicacao` (codigointerno='ACOES_PNGI')
   - Consulta `accounts_role` (codigoperfil)
   - Verifica `accounts_userrole`

## 📊 Modelos

### Principais Entidades

- **Eixo**: Eixos estratégicos do PNGI (TD, TP, IDCL, PIRS, LCP)
- **SituacaoAcao**: Situações das ações (Atrasada, Concluída, etc)
- **VigenciaPNGI**: Períodos de vigência do PNGI
- **TipoEntraveAlerta**: Tipos de entraves/alertas
- **Acoes**: Ações do PNGI
- **AcaoPrazo**: Prazos associados às ações
- **AcaoDestaque**: Destaques de ações
- **TipoAnotacaoAlinhamento**: Tipos de anotações
- **AcaoAnotacaoAlinhamento**: Anotações de alinhamento
- **UsuarioResponsavel**: Usuários responsáveis
- **RelacaoAcaoUsuarioResponsavel**: Relação ação-responsável

Veja documentação completa em: [models.py](./models.py)

## 🔌 APIs REST

Base URL: `/api/v1/acoes_pngi/`

### Endpoints de Autenticação

```
POST   /api/v1/acoes_pngi/auth/portal/        # Autenticação via portal
```

### Endpoints de Usuários

```
POST   /api/v1/acoes_pngi/users/sync/         # Sincronizar usuário
GET    /api/v1/acoes_pngi/users/list/         # Listar usuários
GET    /api/v1/acoes_pngi/users/{email}/      # Buscar por email
```

### Endpoints de Eixos

```
GET    /api/v1/acoes_pngi/eixos/              # Listar eixos
POST   /api/v1/acoes_pngi/eixos/              # Criar eixo
GET    /api/v1/acoes_pngi/eixos/{id}/         # Detalhe de eixo
PUT    /api/v1/acoes_pngi/eixos/{id}/         # Atualizar eixo
DELETE /api/v1/acoes_pngi/eixos/{id}/         # Deletar eixo
GET    /api/v1/acoes_pngi/eixos/list_light/   # Listagem otimizada
```

### Endpoints de Situações

```
GET    /api/v1/acoes_pngi/situacoes/          # Listar situações
POST   /api/v1/acoes_pngi/situacoes/          # Criar situação
GET    /api/v1/acoes_pngi/situacoes/{id}/     # Detalhe
PUT    /api/v1/acoes_pngi/situacoes/{id}/     # Atualizar
DELETE /api/v1/acoes_pngi/situacoes/{id}/     # Deletar
```

### Endpoints de Vigências

```
GET    /api/v1/acoes_pngi/vigencias/                # Listar vigências
POST   /api/v1/acoes_pngi/vigencias/                # Criar vigência
GET    /api/v1/acoes_pngi/vigencias/{id}/           # Detalhe
PUT    /api/v1/acoes_pngi/vigencias/{id}/           # Atualizar
DELETE /api/v1/acoes_pngi/vigencias/{id}/           # Deletar
GET    /api/v1/acoes_pngi/vigencias/vigencia_ativa/ # Vigência ativa
GET    /api/v1/acoes_pngi/vigencias/vigente/        # Vigências vigentes
POST   /api/v1/acoes_pngi/vigencias/{id}/ativar/    # Ativar vigência
```

### Endpoints de Ações

```
GET    /api/v1/acoes_pngi/acoes/                      # Listar ações
POST   /api/v1/acoes_pngi/acoes/                      # Criar ação
GET    /api/v1/acoes_pngi/acoes/{id}/                 # Detalhe
PUT    /api/v1/acoes_pngi/acoes/{id}/                 # Atualizar
DELETE /api/v1/acoes_pngi/acoes/{id}/                 # Deletar
GET    /api/v1/acoes_pngi/acoes/{id}/prazos_ativos/   # Prazos ativos
GET    /api/v1/acoes_pngi/acoes/{id}/responsaveis_list/ # Responsáveis
```

Veja documentação completa em: [views/README.md](./views/README.md)

## 🖥️ Interface Web

Base URL: `/acoes-pngi/`

### Páginas Principais

```
GET    /acoes-pngi/                  # Login (redireciona)
GET    /acoes-pngi/login/            # Página de login
GET    /acoes-pngi/dashboard/        # Dashboard (requer auth)
POST   /acoes-pngi/logout/           # Logout
```

### Dashboard

Exibe:
- Total de eixos cadastrados
- Total de situações
- Total de vigências
- Vigências ativas
- Últimos 5 eixos criados
- Vigência atual (se houver)

## 🎯 Casos de Uso

### 1. Cadastrar Novo Eixo (via API)

```python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/acoes_pngi/eixos/',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'strdescricaoeixo': 'Sustentabilidade',
        'stralias': 'SUST'
    }
)

if response.status_code == 201:
    eixo = response.json()
    print(f"Eixo criado: {eixo['strdescricaoeixo']}")
```

### 2. Ativar Nova Vigência

```python
from acoes_pngi.models import VigenciaPNGI
from datetime import date

# Cria e ativa automaticamente
nova_vigencia = VigenciaPNGI.objects.create(
    strdescricaovigenciapngi='PNGI 2028-2032',
    datiniciovigencia=date(2028, 1, 1),
    datfinalvigencia=date(2032, 12, 31),
    isvigenciaativa=True  # Desativa outras
)
```

### 3. Verificar Permissão de Usuário

```python
from acoes_pngi.permissions import CanEditAcoesPngi

permission = CanEditAcoesPngi()
has_permission = permission.has_permission(request, view)

if has_permission:
    # Permite edição
    ...
```

## 🧪 Testes

```bash
# Testar aplicação
python manage.py test acoes_pngi

# Testar modelos
python manage.py test acoes_pngi.tests.test_models

# Testar APIs
python manage.py test acoes_pngi.tests.test_api_views

# Testar permissões
python manage.py test acoes_pngi.tests.test_permissions
```

## 📚 Relacionamentos

```
acoes_pngi
  ├── Depende de: accounts (autenticação e autorização)
  ├── Usa: common (serializers e serviços)
  └── Schema DB: acoespngi
```

## 🛠️ Configuração

### 1. Adicionar ao INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ...
    'acoes_pngi',
]
```

### 2. Registrar Aplicação no Banco

```sql
INSERT INTO accounts_aplicacao (codigointerno, nome)
VALUES ('ACOES_PNGI', 'Ações PNGI');
```

### 3. Criar Roles

```sql
-- Coordenador
INSERT INTO accounts_role (nomeperfil, codigoperfil, aplicacao_id)
SELECT 'Coordenador - Gerencia Configurações', 'COORDENADOR_PNGI', id
FROM accounts_aplicacao WHERE codigointerno = 'ACOES_PNGI';

-- Gestor
INSERT INTO accounts_role (nomeperfil, codigoperfil, aplicacao_id)
SELECT 'Gestor Acoes PNGI', 'GESTOR_PNGI', id
FROM accounts_aplicacao WHERE codigointerno = 'ACOES_PNGI';

-- Operador
INSERT INTO accounts_role (nomeperfil, codigoperfil, aplicacao_id)
SELECT 'Operador - Apenas Ações', 'OPERADOR_ACAO', id
FROM accounts_aplicacao WHERE codigointerno = 'ACOES_PNGI';

-- Consultor
INSERT INTO accounts_role (nomeperfil, codigoperfil, aplicacao_id)
SELECT 'Consultor - Apenas Leitura', 'CONSULTOR_PNGI', id
FROM accounts_aplicacao WHERE codigointerno = 'ACOES_PNGI';
```

### 4. Executar Migrações

```bash
python manage.py makemigrations acoes_pngi
python manage.py migrate acoes_pngi
```

## 📝 Documentação Adicional

- [Estrutura de Views](./views/README.md)
- [Documentação de Views Específicas](./VIEWS_DOCUMENTATION.md)
- [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)
- [Django Permissions](https://docs.djangoproject.com/en/stable/topics/auth/)

## 👥 Manutenção

### Padrão de Código

A aplicação segue o padrão arquitetural de `carga_org_lot`:

- Views modulares em `views/api_views/` e `views/web_views/`
- Permissões hierárquicas com verificação dupla
- Serializers otimizados com `ListSerializer`
- Router específico em `db_router.py`

### Ao Adicionar Novas Funcionalidades

1. Criar modelo em `models.py`
2. Criar serializer em `serializers.py`
3. Criar ViewSet em `views/api_views/[categoria]_views.py`
4. Criar CBVs em `views/web_views/[categoria]_web_views.py`
5. Adicionar exports nos `__init__.py`
6. Adicionar rotas em `urls/`
7. Atualizar documentação

---

**Desenvolvido por:** Equipe GPP - SEGER/ES  
**Documentação atualizada:** Fevereiro 2026
