# Ações PNGI - Sistema de Gerenciamento

[![Django](https://img.shields.io/badge/Django-6.0.1-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red.svg)](https://www.django-rest-framework.org/)

Aplicação Django para gerenciamento de ações do Programa Nacional de Gestão e Inovação (PNGI) do governo do Espírito Santo.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Características Principais](#-características-principais)
- [Arquitetura](#-arquitetura)
- [Modelos de Dados](#-modelos-de-dados)
- [Sistema de Permissões](#-sistema-de-permissões)
- [API REST](#-api-rest)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Testes](#-testes)
- [Deploy](#-deploy)

---

## 🎯 Visão Geral

A aplicação **Ações PNGI** faz parte da **Plataforma GPP** (Gestão de Pessoas Públicas) e gerencia o ciclo completo de ações estratégicas do PNGI, incluindo:

- **Eixos Estratégicos**: Organização das ações em áreas temáticas
- **Situações de Ações**: Controle do status e fluxo de trabalho
- **Vigências**: Períodos de planejamento e execução
- **Autenticação Multi-Aplicação**: Integração com portal centralizado
- **Sistema de Permissões Granular**: Controle fino de acesso por modelo e operação

---

## ✨ Características Principais

### 🔐 **Sistema de Permissões Automatizado**

- **Verificação automática** baseada em Django permissions e custom permissions
- **Cache de permissões** (15 minutos) para otimização de performance
- **Permissões granulares** por modelo (add, change, delete, view)
- **Role-based access control (RBAC)** com perfis hierárquicos:
  - `GESTOR_PNGI` (Gestor Nacional)
  - `COORDENADOR_PNGI` (Coordenador)
  - `ANALISTA_PNGI` (Analista)
  - `VISUALIZADOR_PNGI` (Somente leitura)

### 🚀 **API REST Moderna**

- **Django REST Framework** com ViewSets ModelViewSet
- **Serializers otimizados** com validações customizadas
- **Endpoints RESTful** seguindo convenções HTTP
- **Autenticação JWT** via portal centralizado
- **Paginação** e **filtros avançados**
- **Swagger/OpenAPI** para documentação interativa

### 🎨 **Interface Web Integrada**

- **Templates Django** com context processors inteligentes
- **Template tags customizadas** para verificação de permissões
- **Context processors** para injeção automática de dados
- **Decorators** para proteção de views

### ⚡ **Performance e Escalabilidade**

- **Cache de permissões** com Django cache framework
- **Serializers otimizados** para listagens (menos campos)
- **Select_related e prefetch_related** em queries complexas
- **Database indexes** em campos críticos

---

## 🏗️ Arquitetura

```
acoes_pngi/
├── management/
│   └── commands/          # Comandos Django personalizados
│       └── create_app_permissions.py
├── migrations/            # Migrações do banco de dados
├── services/             # Lógica de negócio
├── templates/            # Templates HTML
│   └── acoes_pngi/
├── templatetags/         # Template tags personalizadas
│   └── acoes_pngi_tags.py
├── tests/               # Testes automatizados
├── urls/                # Roteamento de URLs
│   ├── api_urls.py     # URLs da API REST
│   └── web_urls.py     # URLs das views web
├── utils/               # Utilitários
│   └── permissions.py  # Helpers de permissões
├── views/               # Views separadas
│   ├── api_views.py    # ViewSets da API
│   └── web_views.py    # Views web
├── admin.py            # Configuração Django Admin
├── apps.py             # Configuração da aplicação
├── context_processors.py  # Context processors
├── decorators.py       # Decorators personalizados
├── models.py           # Modelos de dados
├── permissions.py      # Classes de permissão DRF
└── serializers.py      # Serializers DRF
```

### 🧩 **Separação de Responsabilidades**

**1. Models (models.py)**
- Definição de estruturas de dados
- Validações de modelo
- Propriedades calculadas

**2. Serializers (serializers.py)**
- Serialização/Desserialização JSON
- Validações de API
- Transformação de dados

**3. Permissions (permissions.py + utils/permissions.py)**
- Classes de permissão DRF
- Helpers com cache
- Decorators para views

**4. Views**
- `api_views.py`: ViewSets REST
- `web_views.py`: Views tradicionais Django

**5. Services**
- Lógica de negócio complexa
- Operações transacionais
- Integrações externas

---

## 📊 Modelos de Dados

### **Eixo** (Eixos Estratégicos)

```python
class Eixo(models.Model):
    ideixo = AutoField(primary_key=True)
    strdescricaoeixo = CharField(max_length=100)  # Descrição
    stralias = CharField(max_length=5, unique=True)  # Sigla (UPPERCASE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Validações:**
- `stralias` deve estar em UPPERCASE
- `stralias` máximo 5 caracteres
- `strdescricaoeixo` não pode estar vazio

**Exemplo:**
```json
{
  "ideixo": 1,
  "strdescricaoeixo": "Gestão de Pessoas",
  "stralias": "GP",
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T10:00:00Z"
}
```

---

### **SituacaoAcao** (Situações de Ações)

```python
class SituacaoAcao(models.Model):
    idsituacaoacao = AutoField(primary_key=True)
    strdescricaosituacao = CharField(max_length=15, unique=True)
    # Tabela estática - sem timestamps
```

**Características:**
- Tabela de referência estática
- Raramente modificada
- Sem campos `created_at/updated_at`

**Valores Típicos:**
- `PLANEJADA`
- `EM ANDAMENTO`
- `CONCLUÍDA`
- `CANCELADA`

---

### **VigenciaPNGI** (Períodos de Vigência)

```python
class VigenciaPNGI(models.Model):
    idvigenciapngi = AutoField(primary_key=True)
    strdescricaovigenciapngi = CharField(max_length=100)
    datiniciovigencia = DateField()
    datfinalvigencia = DateField()
    isvigenciaativa = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Validações:**
- `datfinalvigencia` > `datiniciovigencia`
- Apenas uma vigência pode estar ativa por vez

**Propriedades Calculadas:**
- `esta_vigente`: Verifica se está no período ativo
- `duracao_dias`: Calcula duração em dias

**Exemplo:**
```json
{
  "idvigenciapngi": 1,
  "strdescricaovigenciapngi": "PNGI 2024-2027",
  "datiniciovigencia": "2024-01-01",
  "datfinalvigencia": "2027-12-31",
  "isvigenciaativa": true,
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T10:00:00Z"
}
```

---

## 🔒 Sistema de Permissões

### **Arquitetura de Permissões**

```
┌─────────────────────────────────────────────┐
│   Usuário autenticado                       │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│   UserRole (User + Aplicacao + Role)        │
│   - Define papel na aplicação               │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│   RolePermission (Role + Permission)        │
│   - Mapeia permissões do perfil             │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│   Django Permissions                        │
│   - add_eixo, change_eixo, delete_eixo...  │
└─────────────────────────────────────────────┘
```

### **Hierarquia de Perfis**

| Perfil | Permissões | Descrição |
|--------|-----------|------------|
| **GESTOR_PNGI** | Todas | Gestor nacional, controle total |
| **COORDENADOR_PNGI** | add, change, view | Coordenador, sem delete |
| **ANALISTA_PNGI** | add, change, view | Analista, operações básicas |
| **VISUALIZADOR_PNGI** | view | Somente leitura |

### **Permissões por Modelo**

**Eixo:**
- `acoes_pngi.add_eixo`
- `acoes_pngi.change_eixo`
- `acoes_pngi.delete_eixo`
- `acoes_pngi.view_eixo`

**SituacaoAcao:**
- `acoes_pngi.add_situacaoacao`
- `acoes_pngi.change_situacaoacao`
- `acoes_pngi.delete_situacaoacao`
- `acoes_pngi.view_situacaoacao`

**VigenciaPNGI:**
- `acoes_pngi.add_vigenciapngi`
- `acoes_pngi.change_vigenciapngi`
- `acoes_pngi.delete_vigenciapngi`
- `acoes_pngi.view_vigenciapngi`

### **Verificação de Permissões**

**Em ViewSets (API):**
```python
class EixoViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAcoesPermission]  # Automático!
```

**Em Views Web:**
```python
@permission_required_or_403('acoes_pngi.add_eixo')
def criar_eixo(request):
    ...
```

**Em Templates:**
```django
{% load acoes_pngi_tags %}

{% if request.user|has_permission:'add_eixo':'ACOES_PNGI' %}
    <button>Criar Eixo</button>
{% endif %}
```

**Com Helpers (cache automático):**
```python
from acoes_pngi.utils.permissions import get_user_app_permissions

perms = get_user_app_permissions(request.user, 'ACOES_PNGI')
if 'add_eixo' in perms:
    # Usuário pode criar eixos
```

---

## 🌐 API REST

### **Base URL**
```
/api/v1/acoes_pngi/
```

### **Autenticação**

**1. Obter Token JWT:**
```http
POST /api/v1/auth/token/
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}
```

**Resposta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Nome do Usuário"
  }
}
```

**2. Usar Token:**
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

### **Endpoints de Eixos**

#### **Listar Eixos**
```http
GET /api/v1/acoes_pngi/eixos/
Authorization: Bearer {token}
```

**Resposta:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "ideixo": 1,
      "strdescricaoeixo": "Gestão de Pessoas",
      "stralias": "GP",
      "created_at": "2026-01-30T10:00:00Z",
      "updated_at": "2026-01-30T10:00:00Z"
    }
  ]
}
```

#### **Listagem Otimizada (cache)**
```http
GET /api/v1/acoes_pngi/eixos/list_light/
```

Retorna apenas campos essenciais para melhor performance.

#### **Criar Eixo**
```http
POST /api/v1/acoes_pngi/eixos/
Content-Type: application/json

{
  "strdescricaoeixo": "Inovação Tecnológica",
  "stralias": "IT"
}
```

**Requer:** `add_eixo`

#### **Atualizar Eixo**
```http
PATCH /api/v1/acoes_pngi/eixos/1/

{
  "strdescricaoeixo": "Inovação e Tecnologia"
}
```

**Requer:** `change_eixo`

#### **Deletar Eixo**
```http
DELETE /api/v1/acoes_pngi/eixos/1/
```

**Requer:** `delete_eixo`

---

### **Endpoints de Situações**

```http
GET    /api/v1/acoes_pngi/situacoes/
POST   /api/v1/acoes_pngi/situacoes/
GET    /api/v1/acoes_pngi/situacoes/{id}/
PATCH  /api/v1/acoes_pngi/situacoes/{id}/
DELETE /api/v1/acoes_pngi/situacoes/{id}/
```

---

### **Endpoints de Vigências**

```http
GET    /api/v1/acoes_pngi/vigencias/
POST   /api/v1/acoes_pngi/vigencias/
GET    /api/v1/acoes_pngi/vigencias/{id}/
PATCH  /api/v1/acoes_pngi/vigencias/{id}/
DELETE /api/v1/acoes_pngi/vigencias/{id}/

# Custom actions
GET    /api/v1/acoes_pngi/vigencias/vigencia_ativa/
POST   /api/v1/acoes_pngi/vigencias/{id}/ativar/
```

**Ativar Vigência:**
```http
POST /api/v1/acoes_pngi/vigencias/1/ativar/
```

Desativa todas as vigências e ativa a especificada.

**Requer:** Perfil Coordenador ou superior (`IsCoordenadorOrAbove`)

---

### **Endpoint de Permissões**

```http
GET /api/v1/acoes_pngi/permissions/
Authorization: Bearer {token}
```

**Resposta:**
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "name": "Nome do Usuário",
  "role": "GESTOR_PNGI",
  "permissions": [
    "add_eixo",
    "change_eixo",
    "delete_eixo",
    "view_eixo",
    "add_situacaoacao",
    "change_situacaoacao",
    "delete_situacaoacao",
    "view_situacaoacao"
  ],
  "is_superuser": false,
  "groups": {
    "can_manage_config": true,
    "can_manage_acoes": false,
    "can_delete": true
  },
  "specific": {
    "eixo": {
      "can_add": true,
      "can_change": true,
      "can_delete": true,
      "can_view": true
    },
    "situacaoacao": {
      "can_add": true,
      "can_change": true,
      "can_delete": true,
      "can_view": true
    },
    "vigenciapngi": {
      "can_add": true,
      "can_change": true,
      "can_delete": true,
      "can_view": true
    }
  }
}
```

Use este endpoint no frontend (Next.js) para renderizar elementos condicionalmente.

---

## 🚀 Instalação

### **Pré-requisitos**

- Python 3.13+
- PostgreSQL 16+
- pip ou poetry

### **1. Clone o repositório**

```bash
git clone https://github.com/ProjetcsGPP/gpp_plataform.git
cd gpp_plataform
```

### **2. Crie ambiente virtual**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### **3. Instale dependências**

```bash
pip install -r requirements.txt
```

### **4. Configure variáveis de ambiente**

Crie `.env` na raiz do projeto:

```env
# Database
DATABASE_NAME=gpp_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Cache
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
```

### **5. Execute migrações**

```bash
python manage.py migrate
```

### **6. Crie permissões da aplicação**

```bash
python manage.py create_app_permissions ACOES_PNGI
```

### **7. Crie superusuário**

```bash
python manage.py createsuperuser
```

### **8. Execute o servidor**

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/acoes_pngi/

---

## ⚙️ Configuração

### **Configuração do Cache**

**settings.py:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'TIMEOUT': 900,  # 15 minutos
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### **Configuração de Permissões Customizadas**

**apps.py:**
```python
class AcoesPngiConfig(AppConfig):
    app_code = 'ACOES_PNGI'
    app_display_name = 'Ações PNGI'
    
    custom_permissions = [
        ('pode_ativar_vigencia', 'Pode ativar vigências'),
        ('pode_gerar_relatorios', 'Pode gerar relatórios'),
    ]
```

### **Integração com Portal Centralizado**

**settings.py:**
```python
PORTAL_AUTH_URL = 'https://portal.example.com/auth/'
PORTAL_API_KEY = 'your-api-key'
```

---

## 💻 Uso

### **Interface Web**

Acesse:
- Lista de Eixos: `/acoes_pngi/eixos/`
- Admin: `/admin/`

### **API REST**

Documentação interativa:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

### **Exemplos de Código**

**Python (requests):**
```python
import requests

# Autenticar
response = requests.post(
    'http://localhost:8000/api/v1/auth/token/',
    json={'username': 'user@example.com', 'password': 'password'}
)
token = response.json()['access']

# Listar eixos
response = requests.get(
    'http://localhost:8000/api/v1/acoes_pngi/eixos/',
    headers={'Authorization': f'Bearer {token}'}
)
eixos = response.json()['results']
```

**JavaScript (fetch):**
```javascript
// Autenticar
const response = await fetch('/api/v1/auth/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'user@example.com', password: 'password' })
});
const { access } = await response.json();

// Listar eixos
const eixosResponse = await fetch('/api/v1/acoes_pngi/eixos/', {
  headers: { 'Authorization': `Bearer ${access}` }
});
const { results: eixos } = await eixosResponse.json();
```

---

## 🧪 Testes

### **Executar todos os testes**

```bash
python manage.py test acoes_pngi
```

### **Executar testes específicos**

```bash
python manage.py test acoes_pngi.tests.test_permissions
python manage.py test acoes_pngi.tests.test_api
```

### **Cobertura de testes**

```bash
coverage run --source='acoes_pngi' manage.py test acoes_pngi
coverage report
coverage html  # Gera relatório HTML
```

### **Testes de API com PowerShell**

```powershell
cd TestesPowerShell
.\Acoes_PNGI_test_permissions_API.ps1
```

---

## 🚢 Deploy

### **Checklist de Produção**

- [ ] `DEBUG = False`
- [ ] Configurar `ALLOWED_HOSTS`
- [ ] Usar servidor WSGI/ASGI (Gunicorn, uWSGI)
- [ ] Configurar cache Redis
- [ ] Configurar HTTPS/SSL
- [ ] Configurar backup do banco de dados
- [ ] Configurar logs centralizados
- [ ] Executar `collectstatic`
- [ ] Verificar variáveis de ambiente

### **Gunicorn**

```bash
gunicorn gpp_plataform.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

### **Nginx (exemplo)**

```nginx
server {
    listen 80;
    server_name acoes.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/gpp_plataform/staticfiles/;
    }

    location /media/ {
        alias /var/www/gpp_plataform/media/;
    }
}
```

### **Docker**

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "gpp_plataform.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 📚 Documentação Adicional

- **Django**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **PostgreSQL**: https://www.postgresql.org/docs/

---

## 📝 Changelog

### **v2.0.0 (2026-01-30)**

#### ✨ **Novidades**
- Sistema de permissões automatizado com cache
- API REST completa com Django REST Framework
- Serializers otimizados para listagens
- Endpoint `/permissions/` para frontend Next.js
- Template tags customizadas para verificação de permissões
- Context processors para injeção automática de dados
- Helpers de permissões com cache (15 minutos)

#### 🔧 **Melhorias**
- Refatoração completa da estrutura de views (separação API/Web)
- Organização de URLs em módulos separados
- Validações aprimoradas em models e serializers
- Performance otimizada com cache e queries eficientes
- Documentação completa com exemplos

#### 🐛 **Correções**
- Modelo `SituacaoAcao` sem timestamps (tabela estática)
- Admin Django atualizado para refletir mudanças nos modelos
- Triggers PostgreSQL removidos para compatibilidade
- Sequences PostgreSQL sincronizadas

#### 🗑️ **Removido**
- Campos `created_at` e `updated_at` de `SituacaoAcao`
- Arquivos de documentação antigos consolidados
- Código legado de permissões manuais

---

## 👥 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é propriedade do Governo do Estado do Espírito Santo - SEGER.

---

## 📞 Contato

**Equipe GPP - SEGER/ES**
- Email: gpp@seger.es.gov.br
- Website: https://seger.es.gov.br

---

**Desenvolvido com ❤️ pela equipe GPP**

📋 MATRIZ DE PERMISSÕES FINAL E CORRETA
Entidade/Ação	                                  GESTOR  COORDENADOR OPERADOR	CONSULTOR
CONFIGURAÇÕES - Nível 1 (Apenas GESTOR)				
SituacaoAcao (R)	                              Sim     Sim	        Sim	        Sim
SituacaoAcao (W/D)	                            Sim	   	Não	    	Não	    	Não
TipoEntraveAlerta (R)	                          Sim	   	Sim	    	Sim	        Sim
TipoEntraveAlerta (W/D)	                        Sim	   	Não	    	Não	        Não
CONFIGURAÇÕES - Nível 2 (GESTOR e COORDENADOR)				
Eixo (R)	                                      Sim	   	Sim	    	Sim	        Sim
Eixo (W/D)	                                    Sim	   	Sim	    	Não	        Não
VigenciaPNGI (R)	                              Sim	   	Sim	    	Sim	        Sim
VigenciaPNGI (W/D)	                            Sim	   	Sim	    	Não	        Não
TipoAnotacaoAlinhamento (R)	                    Sim	   	Sim	    	Sim         Sim
TipoAnotacaoAlinhamento (W/D)	                  Sim	   	Sim	    	Não	        Não
OPERAÇÕES (GESTOR, COORDENADOR e OPERADOR)				
Acoes (R)	                                      Sim	   	Sim	    	Sim	        Sim
Acoes (W/D)	                                    Sim	   	Sim	    	Sim	        Não
AcaoPrazo (R)	                                  Sim	   	Sim	    	Sim	        Sim
AcaoPrazo (W/D)	                                Sim	   	Sim	    	Sim	        Não
AcaoDestaque (R)	                              Sim	   	Sim	    	Sim	        Sim
AcaoDestaque (W/D)	                            Sim	   	Sim	    	Sim	        Não
AcaoAnotacaoAlinhamento (R)	                    Sim	   	Sim	    	Sim	        Sim
AcaoAnotacaoAlinhamento (W/D)	                  Sim	   	Sim	    	Sim	        Não
UsuarioResponsavel (R)	                        Sim	   	Sim	    	Sim	        Sim
UsuarioResponsavel (W/D)	                      Sim	   	Sim     	Sim	        Não
RelacaoAcaoUsuarioResponsavel (R)	              Sim	   	Sim	    	Sim	        Sim
RelacaoAcaoUsuarioResponsavel (W/D)	            Sim	   	Sim	    	Sim	        Não
GESTÃO DE USUÁRIOS				
Usuários/Roles (R)	                            Sim	   	Sim	    	Sim         Sim
Usuários/Roles (W/D)	                          Sim	   	Não	    	Não	        Não
Legenda:

R = Read (GET, HEAD, OPTIONS)
W = Write (POST, PUT, PATCH)
D = Delete (DELETE)