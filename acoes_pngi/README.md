## 4. acoes_pngi/README.md

```markdown
# Ações PNGI - Gestão de Ações do PNGI

Aplicação para gerenciamento de ações do Plano Nacional de Gestão da Inovação (PNGI) do Governo do Espírito Santo.

## 📋 Visão Geral

A aplicação **Ações PNGI** permite:

- Cadastro e gestão de **Eixos Estratégicos**
- Controle de **Situações de Ações**
- Gerenciamento de **Vigências do PNGI**
- Dashboard com estatísticas e visualizações
- APIs REST para integração com frontend Next.js

## 🏗️ Estrutura

acoes_pngi/
├── models.py # Eixo, SituacaoAcao, VigenciaPNGI
├── serializers.py # Serializers DRF
├── views/
│ ├── api_views.py # ViewSets para APIs REST
│ └── web_views.py # Views tradicionais (templates)
├── urls/
│ ├── api_urls.py # Rotas da API
│ └── web_urls.py # Rotas web
├── templates/
│ └── acoes_pngi/
│ ├── login.html
│ └── dashboard.html
├── admin.py # Configuração do Django Admin
└── migrations/ # Migrações do banco

text

## 📊 Modelos

### Eixo

Representa os eixos estratégicos do PNGI.

**Campos**:
```python
ideixo              # PK (AutoField)
strdescricaoeixo    # Descrição do eixo (max 255 chars)
stralias            # Alias em maiúsculas (max 5 chars)
created_at          # Data de criação
updated_at          # Data de atualização
Eixos cadastrados:

TD - Transformação Digital

TP - Transferências e Parcerias

IDCL - Inovação e Desenvolvimento de Competências e Lideranças

PIRS - Patrimônio Imobiliário e Responsabilidade Socioambiental

LCP - Logística e Compras Públicas

Exemplo de uso:

python
from acoes_pngi.models import Eixo

# Criar eixo
eixo = Eixo.objects.create(
    strdescricaoeixo='Transformação Digital',
    stralias='TD'
)

# Buscar eixos
eixos = Eixo.objects.all()
eixo_td = Eixo.objects.get(stralias='TD')
SituacaoAcao
Situações possíveis de uma ação do PNGI.

Campos:

python
idsituacaoacao       # PK (AutoField)
strdescricaosituacao # Descrição em maiúsculas (max 100 chars)
Situações cadastradas:

ATRASADA

CONCLUÍDA

REPACTUADA

EM ANDAMENTO

CANCELADA

NÃO INICIADA

AGUARDANDO FEED

Exemplo de uso:

python
from acoes_pngi.models import SituacaoAcao

# Criar situação
situacao = SituacaoAcao.objects.create(
    strdescricaosituacao='EM ANDAMENTO'
)

# Buscar situações
situacoes = SituacaoAcao.objects.all()
VigenciaPNGI
Períodos de vigência do PNGI.

Campos:

python
idvigenciapngi           # PK (AutoField)
strdescricaovigenciapngi # Descrição (max 200 chars)
datiniciovigencia        # Data de início
datfinalvigencia         # Data de término
isvigenciaativa          # Se está ativa (apenas uma por vez)
created_at               # Data de criação
updated_at               # Data de atualização
Regras:

Apenas uma vigência pode estar ativa por vez

Data final deve ser posterior à data inicial

Ao ativar uma vigência, as demais são desativadas automaticamente

Exemplo de uso:

python
from acoes_pngi.models import VigenciaPNGI
from datetime import date

# Criar vigência
vigencia = VigenciaPNGI.objects.create(
    strdescricaovigenciapngi='PNGI 2024-2028',
    datiniciovigencia=date(2024, 1, 1),
    datfinalvigencia=date(2028, 12, 31),
    isvigenciaativa=True  # Desativa outras automaticamente
)

# Buscar vigência ativa
vigencia_atual = VigenciaPNGI.objects.filter(isvigenciaativa=True).first()
🔌 APIs REST
Base URL: /api/v1/acoes_pngi/

Endpoints de Eixos
text
GET    /api/v1/acoes_pngi/eixos/              # Listar eixos
POST   /api/v1/acoes_pngi/eixos/              # Criar eixo
GET    /api/v1/acoes_pngi/eixos/{id}/         # Detalhe de eixo
PUT    /api/v1/acoes_pngi/eixos/{id}/         # Atualizar eixo
PATCH  /api/v1/acoes_pngi/eixos/{id}/         # Atualização parcial
DELETE /api/v1/acoes_pngi/eixos/{id}/         # Deletar eixo
GET    /api/v1/acoes_pngi/eixos/list_light/   # Listagem otimizada
Exemplo de request (criar eixo):

bash
curl -X POST http://localhost:8000/api/v1/acoes_pngi/eixos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "strdescricaoeixo": "Novo Eixo",
    "stralias": "NE"
  }'
Endpoints de Situações
text
GET    /api/v1/acoes_pngi/situacoes/          # Listar situações
POST   /api/v1/acoes_pngi/situacoes/          # Criar situação
GET    /api/v1/acoes_pngi/situacoes/{id}/     # Detalhe de situação
PUT    /api/v1/acoes_pngi/situacoes/{id}/     # Atualizar situação
DELETE /api/v1/acoes_pngi/situacoes/{id}/     # Deletar situação
Endpoints de Vigências
text
GET    /api/v1/acoes_pngi/vigencias/                # Listar vigências
POST   /api/v1/acoes_pngi/vigencias/                # Criar vigência
GET    /api/v1/acoes_pngi/vigencias/{id}/           # Detalhe de vigência
PUT    /api/v1/acoes_pngi/vigencias/{id}/           # Atualizar vigência
DELETE /api/v1/acoes_pngi/vigencias/{id}/           # Deletar vigência
GET    /api/v1/acoes_pngi/vigencias/vigencia_ativa/ # Vigência ativa
POST   /api/v1/acoes_pngi/vigencias/{id}/ativar/    # Ativar vigência
Exemplo (buscar vigência ativa):

bash
curl http://localhost:8000/api/v1/acoes_pngi/vigencias/vigencia_ativa/ \
  -H "Authorization: Bearer {token}"
Endpoints de Autenticação
text
POST   /api/v1/acoes_pngi/auth/portal/        # Autenticação via portal
Endpoints de Usuários
text
POST   /api/v1/acoes_pngi/users/sync/         # Sincronizar usuário
GET    /api/v1/acoes_pngi/users/list/         # Listar usuários
GET    /api/v1/acoes_pngi/users/{email}/      # Buscar por email
🖥️ Interface Web
Base URL: /acoes-pngi/

Páginas
text
GET    /acoes-pngi/                  # Login (redireciona)
GET    /acoes-pngi/login/            # Página de login
GET    /acoes-pngi/dashboard/        # Dashboard (requer auth)
POST   /acoes-pngi/logout/           # Logout
Login
Validação de email e senha

Verificação de permissões (UserRole)

Redirecionamento automático se já autenticado

Dashboard
Exibe:

Total de eixos cadastrados

Total de situações

Total de vigências

Vigências ativas

Últimos 5 eixos criados

Vigência atual (se houver)

🔐 Permissões
Roles Disponíveis
GESTOR_PNGI: Acesso total à aplicação

USER_PNGI: Acesso de leitura

Verificação de Acesso
python
from accounts.models import UserRole

# Na view
has_access = UserRole.objects.filter(
    user=request.user,
    aplicacao__codigointerno='ACOES_PNGI'
).exists()

if not has_access:
    # Negar acesso
    ...
🎯 Casos de Uso
1. Cadastrar Novo Eixo (via API)
python
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
2. Ativar Nova Vigência
python
from acoes_pngi.models import VigenciaPNGI
from datetime import date

# Cria e ativa automaticamente
nova_vigencia = VigenciaPNGI.objects.create(
    strdescricaovigenciapngi='PNGI 2028-2032',
    datiniciovigencia=date(2028, 1, 1),
    datfinalvigencia=date(2032, 12, 31),
    isvigenciaativa=True  # Desativa outras
)
3. Buscar Estatísticas para Dashboard
python
from acoes_pngi.models import Eixo, SituacaoAcao, VigenciaPNGI

stats = {
    'total_eixos': Eixo.objects.count(),
    'total_situacoes': SituacaoAcao.objects.count(),
    'total_vigencias': VigenciaPNGI.objects.count(),
    'vigencias_ativas': VigenciaPNGI.objects.filter(
        isvigenciaativa=True
    ).count(),
}
🧪 Testes
bash
# Testar aplicação
python manage.py test acoes_pngi

# Testar modelos
python manage.py test acoes_pngi.tests.test_models

# Testar APIs
python manage.py test acoes_pngi.tests.test_api_views
📚 Relacionamentos
text
acoes_pngi
  ├── Depende de: accounts (autenticação)
  ├── Usa: common (serializers e serviços)
  └── Schema DB: acoespngi
🛠️ Configuração
Adicionar ao INSTALLED_APPS
python
INSTALLED_APPS = [
    # ...
    'acoes_pngi',
]
Registrar no Portal
sql
INSERT INTO tblaplicacao (codigointerno, nomeaplicacao, baseurl, isshowinportal)
VALUES ('ACOES_PNGI', 'Gestão de Ações PNGI', 'http://localhost:8000/acoes-pngi/', true);
Criar Role
sql
INSERT INTO accountsrole (nomeperfil, codigoperfil, aplicacaoid)
SELECT 'Gestor PNGI', 'GESTOR_PNGI', idaplicacao
FROM tblaplicacao WHERE codigointerno = 'ACOES_PNGI';
📖 Referências
PNGI - Documentação Oficial

DRF ViewSets

Ações PNGI - Gestão de Ações do Plano Nacional de Gestão da Inovação