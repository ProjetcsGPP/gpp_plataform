# GPP Plataform - Plataforma de Gestão Pública

Sistema de gestão integrada desenvolvido para o Governo do Espírito Santo, centralizando múltiplas aplicações de gestão pública em uma única plataforma.

## 📋 Visão Geral

A GPP Plataform é uma solução multi-tenant que oferece:

- **Portal Unificado**: Autenticação centralizada e gerenciamento de acesso
- **Ações PNGI**: Gestão de ações do Plano Nacional de Gestão da Inovação
- **Carga Org/Lot**: Sistema de carga e validação de organogramas e lotações
- **Arquitetura Modular**: Aplicações independentes com autenticação compartilhada

## 🏗️ Arquitetura

gpp_plataform/
├── accounts/ # Autenticação e gerenciamento de usuários
├── common/ # Utilitários e componentes compartilhados
├── db_service/ # Serviços de autenticação de aplicações (API clients)
├── portal/ # Portal principal (dashboard unificado)
├── acoes_pngi/ # Gestão de Ações PNGI
├── carga_org_lot/ # Carga de Organogramas e Lotações
└── gpp_plataform/ # Configurações do projeto Django

text

## 🚀 Tecnologias

- **Backend**: Django 6.0.1 + Django REST Framework
- **Banco de Dados**: PostgreSQL 17
- **Autenticação**: JWT + Session-based
- **API Documentation**: Swagger/OpenAPI (drf-yasg)
- **Frontend**: Templates Django + integração Next.js (em desenvolvimento)

## 📦 Instalação

### Pré-requisitos

- Python 3.13+
- PostgreSQL 17+
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/ProjetcsGPP/gpp_plataform.git
   cd gpp_plataform
Crie e ative o ambiente virtual:

bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
Instale as dependências:

bash
pip install -r requirements.txt
Configure o banco de dados:

Crie um banco PostgreSQL:

sql
CREATE DATABASE gpp_plataform;
CREATE USER gpp_user WITH PASSWORD 'sua_senha';
ALTER ROLE gpp_user SET client_encoding TO 'utf8';
ALTER ROLE gpp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE gpp_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE gpp_plataform TO gpp_user;
Configure as variáveis de ambiente:

Crie um arquivo .env na raiz do projeto:

text
DEBUG=True
SECRET_KEY=sua_chave_secreta_aqui
DATABASE_URL=postgres://gpp_user:sua_senha@localhost:5432/gpp_plataform
ALLOWED_HOSTS=localhost,127.0.0.1
PORTAL_AUTH_URL=http://localhost:8000
Execute as migrations:

bash
python manage.py migrate
Crie um superusuário:

bash
python manage.py createsuperuser
Execute o servidor de desenvolvimento:

bash
python manage.py runserver
Acesse a aplicação:

Portal: http://localhost:8000/

Admin: http://localhost:8000/admin/

API Docs: http://localhost:8000/swagger/

📚 Estrutura de URLs
APIs REST (para Next.js)
text
/api/v1/auth/              - Autenticação (JWT + Session)
/api/v1/portal/            - APIs do Portal
/api/v1/acoes_pngi/        - APIs de Ações PNGI
/api/v1/carga/             - APIs de Carga Org/Lot
Interface Web (Django Templates)
text
/                          - Portal principal
/admin/                    - Django Admin
/acoes-pngi/               - Aplicação Ações PNGI
/carga_org_lot/            - Aplicação Carga Org/Lot
🔐 Sistema de Autenticação
A plataforma implementa autenticação multi-tenant:

Usuários: Tabela única compartilhada (accounts.User)

Aplicações: Cada aplicação registrada tem código único

Roles: Perfis de acesso por aplicação

Attributes: Atributos customizados por usuário/aplicação

Fluxo de Autenticação
text
Portal Login → Validação de Credenciais → Verificação de Permissões → Acesso à Aplicação
🧩 Aplicações
1. Portal
Dashboard unificado com:

Autenticação centralizada

Listagem de aplicações disponíveis

Gerenciamento de perfil

Documentação completa

2. Ações PNGI
Gerenciamento de ações do PNGI:

Cadastro de eixos estratégicos

Gestão de situações de ações

Controle de vigências

Documentação completa

3. Carga Org/Lot
Sistema de carga de dados:

Upload de organogramas

Processamento de lotações

Validação e envio para API externa

Documentação completa

4. Common
Componentes compartilhados:

Serializers genéricos

Serviços de autenticação

Mixins e utilitários

Documentação completa

5. Accounts
Gerenciamento de usuários:

Modelo de usuário customizado

Sistema de roles e permissões

Atributos customizados

Documentação completa

🧪 Testes
bash
# Executar todos os testes
python manage.py test

# Testar aplicação específica
python manage.py test acoes_pngi

# Com cobertura
coverage run --source='.' manage.py test
coverage report
📊 Banco de Dados
Schemas
public: Tabelas de usuários, aplicações e autenticação

acoespngi: Tabelas específicas do PNGI

cargaorglot: Tabelas de carga de organogramas

Principais Tabelas
sql
public.tblusuario              -- Usuários
public.tblaplicacao            -- Aplicações registradas
public.accountsrole            -- Perfis de acesso
public.accountsuserrole        -- Usuários x Perfis x Aplicações
public.accountsattribute       -- Atributos customizados

acoespngi.tbleixos             -- Eixos estratégicos
acoespngi.tblvigenciapngi      -- Vigências do PNGI

cargaorglot.tblpatriarca       -- Patriarcas (órgãos raiz)
cargaorglot.tblorgaounidade    -- Unidades organizacionais
🛠️ Desenvolvimento
Código de Conduta
Use Python 3.13+

Siga PEP 8 para estilo de código

Documente todas as funções e classes

Escreva testes para novas funcionalidades

Use type hints quando possível

Estrutura de Branches
text
main              -- Produção
develop           -- Desenvolvimento
feature/*         -- Novas funcionalidades
bugfix/*          -- Correções de bugs
hotfix/*          -- Correções urgentes
Commits
Use Conventional Commits:

text
feat: Adiciona nova funcionalidade
fix: Corrige bug
docs: Atualiza documentação
style: Formatação de código
refactor: Refatoração de código
test: Adiciona testes
chore: Tarefas de manutenção
📝 Comandos Úteis
bash
# Criar nova aplicação
python manage.py startapp nome_app

# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Abrir shell Django
python manage.py shell

# Verificar problemas
python manage.py check

# Listar todas as URLs
python manage.py show_urls  # Requer django-extensions
🔧 Configuração de Produção
Variáveis de Ambiente
text
DEBUG=False
SECRET_KEY=chave_super_secreta_em_producao
DATABASE_URL=postgres://user:pass@host:5432/dbname
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
CORS_ALLOWED_ORIGINS=https://frontend.seudominio.com
PORTAL_AUTH_URL=https://portal.seudominio.com
Gunicorn
bash
gunicorn gpp_plataform.wsgi:application --bind 0.0.0.0:8000 --workers 4
Nginx (exemplo)
text
server {
    listen 80;
    server_name seudominio.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
📄 Licença
Este projeto é proprietário do Governo do Espírito Santo.

👥 Equipe
Desenvolvimento: Equipe GPP

Contato: contato@gpp.es.gov.br

🐛 Reportar Bugs
Para reportar bugs ou solicitar funcionalidades, abra uma issue no GitHub ou entre em contato com a equipe de desenvolvimento.

📖 Documentação Adicional
Guia de Instalação Detalhado

API Reference

Guia de Contribuição

Changelog