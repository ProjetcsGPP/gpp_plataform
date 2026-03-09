## 5. carga_org_lot/README.md

```markdown
# Carga Org/Lot - Sistema de Carga de Organogramas e Lotações

Aplicação para upload, processamento e envio de organogramas e lotações para API externa do Governo do Espírito Santo.

## 📋 Visão Geral

A aplicação **Carga Org/Lot** permite:

- Upload de arquivos de organogramas (JSON, XML)
- Upload de planilhas de lotações (Excel, CSV)
- Validação e processamento de dados
- Envio para API externa
- Rastreamento de status de cargas
- Gestão de patriarcas (órgãos raiz)

## 🏗️ Estrutura

carga_org_lot/
├── models.py # Patriarca, Versão, Unidade, Lotação, etc
├── serializers.py # Serializers DRF
├── views/
│ ├── api_views.py # ViewSets para APIs REST
│ └── web_views.py # Views tradicionais (templates)
├── urls/
│ ├── api_urls.py # Rotas da API
│ └── web_urls.py # Rotas web
├── templates/
│ └── carga_org_lot/
│ ├── login.html
│ └── dashboard.html
├── admin.py # Configuração do Django Admin
└── migrations/ # Migrações do banco

text

## 📊 Modelos Principais

### Patriarca

Órgão raiz da hierarquia organizacional.

**Campos**:
```python
idpatriarca            # PK
idexternopatriarca     # UUID externo
strsiglapatriarca      # Sigla do órgão (max 20 chars)
strnome                # Nome do órgão
idstatusprogresso      # Status do progresso
datacriacao            # Data de criação
idusuariocriacao       # Usuário que criou
datalteracao           # Data de alteração
idusuarioalteracao     # Usuário que alterou
Status de Progresso:

Nova Carga

Organograma em Progresso

Lotação em Progresso

Pronto para Carga

Carga em Processamento

Carga Finalizada

OrganogramaVersao
Versão de um organograma processado.

Campos:

python
idorganogramaversao        # PK
idpatriarca                # FK para Patriarca
strorigem                  # Origem do arquivo
strtipoarquivooriginal     # Tipo (JSON, XML)
strnomearquivooriginal     # Nome do arquivo
datprocessamento           # Data de processamento
strstatusprocessamento     # Status ('Sucesso', 'Erro')
strmensagemprocessamento   # Mensagem de erro (se houver)
flgativo                   # Se está ativo
OrgaoUnidade
Unidade organizacional (nó da árvore hierárquica).

Campos:

python
idorgaounidade         # PK
idorganogramaversao    # FK para OrganogramaVersao
idpatriarca            # FK para Patriarca
strnome                # Nome da unidade
strsigla               # Sigla da unidade
idorgaounidadepai      # FK recursiva (pai)
strnumerohierarquia    # Caminho hierárquico (ex: "1.2.3")
intnivelhierarquia     # Nível na hierarquia
flgativo               # Se está ativo
LotacaoVersao
Versão de uma carga de lotações.

Campos:

python
idlotacaoversao        # PK
idpatriarca            # FK para Patriarca
strorigem              # Origem do arquivo
strtipoarquivo         # Tipo (Excel, CSV)
strnomearquivo         # Nome do arquivo
datprocessamento       # Data de processamento
strstatusprocessamento # Status
flgativo               # Se está ativo
Lotacao
Registro de lotação de servidor.

Campos:

python
idlotacao              # PK
idlotacaoversao        # FK para LotacaoVersao
idpatriarca            # FK para Patriarca
idorgaounidade         # FK para OrgaoUnidade
strcpf                 # CPF do servidor
strmatricula           # Matrícula
strnome                # Nome do servidor
strcargo               # Cargo
datadmissao            # Data de admissão
flgativo               # Se está ativo
🔌 APIs REST
Base URL: /api/v1/carga/

Endpoints
text
GET    /api/v1/carga/                         # Dashboard API
POST   /api/v1/carga/upload/                  # Upload de arquivo
🖥️ Interface Web
Base URL: /carga_org_lot/

Páginas
text
GET    /carga_org_lot/                # Redirect para login
GET    /carga_org_lot/login/          # Página de login
GET    /carga_org_lot/dashboard/      # Dashboard (requer auth)
POST   /carga_org_lot/logout/         # Logout
Dashboard
Funcionalidades:

Upload de organogramas (JSON/XML)

Upload de lotações (Excel/CSV)

Visualização de patriarcas cadastrados

Histórico de cargas

Status de processamento

🔐 Permissões
Roles Disponíveis
GESTOR_CARGA: Acesso total (upload, processamento, envio)

VISUALIZADOR_CARGA: Apenas visualização

Atributos
can_upload: Permite realizar uploads ('true' ou 'false')

max_patriarcas: Número máximo de patriarcas permitidos

Verificação na View
python
from accounts.models import Attribute

# Verifica se pode fazer upload
can_upload = Attribute.objects.filter(
    user=request.user,
    aplicacao__codigointerno='CARGA_ORG_LOT',
    key='can_upload',
    value='true'
).exists()

if not can_upload:
    messages.error(request, 'Você não tem permissão para fazer upload')
    return redirect('carga_org_lot_web:dashboard')
🎯 Casos de Uso
1. Upload de Organograma
python
from carga_org_lot.models import Patriarca, OrganogramaVersao
import json

# Processar arquivo JSON
with open('organograma.json', 'r') as f:
    data = json.load(f)

# Criar patriarca
patriarca = Patriarca.objects.create(
    idexternopatriarca=data['uuid'],
    strsiglapatriarca=data['sigla'],
    strnome=data['nome'],
    idstatusprogresso=1,  # Nova Carga
    idusuariocriacao=request.user.idusuario
)

# Criar versão
versao = OrganogramaVersao.objects.create(
    idpatriarca=patriarca,
    strorigem='Upload Manual',
    strtipoarquivooriginal='JSON',
    strnomearquivooriginal='organograma.json',
    strstatusprocessamento='Sucesso',
    flgativo=True
)

# Processar unidades...
2. Validar Lotação
python
from carga_org_lot.models import Lotacao, OrgaoUnidade

def validar_lotacao(cpf, matricula, idorgaounidade):
    """Valida se lotação é válida"""

    # Verifica se unidade existe
    try:
        unidade = OrgaoUnidade.objects.get(
            idorgaounidade=idorgaounidade,
            flgativo=True
        )
    except OrgaoUnidade.DoesNotExist:
        return False, "Unidade não encontrada"

    # Verifica duplicidade
    existe = Lotacao.objects.filter(
        strcpf=cpf,
        flgativo=True
    ).exists()

    if existe:
        return False, "Servidor já possui lotação ativa"

    return True, "Válido"
3. Enviar para API Externa
python
import requests
from carga_org_lot.models import OrganogramaJSON, StatusTokenEnvioCarga

def enviar_organograma(idorganogramajson):
    """Envia organograma para API externa"""

    # Busca o organograma
    org_json = OrganogramaJSON.objects.get(
        idorganogramajson=idorganogramajson
    )

    # Solicita token
    token_response = requests.post(
        'https://api.externa.gov.br/auth/token',
        json={'client_id': 'xxx', 'client_secret': 'yyy'}
    )

    if token_response.status_code != 200:
        # Marca como erro
        org_json.strstatusenvio = 'Erro'
        org_json.strmensagemretorno = 'Falha ao obter token'
        org_json.save()
        return False

    token = token_response.json()['access_token']

    # Envia organograma
    response = requests.post(
        'https://api.externa.gov.br/organogramas',
        headers={'Authorization': f'Bearer {token}'},
        json=org_json.jsconteudo
    )

    # Atualiza status
    org_json.datenvioapi = timezone.now()

    if response.status_code == 201:
        org_json.strstatusenvio = 'Enviado com sucesso'
        org_json.save()
        return True
    else:
        org_json.strstatusenvio = 'Erro no envio'
        org_json.strmensagemretorno = response.text
        org_json.save()
        return False
🧪 Testes
bash
# Testar aplicação
python manage.py test carga_org_lot

# Testar processamento
python manage.py test carga_org_lot.tests.test_processing
📚 Relacionamentos
text
carga_org_lot
  ├── Depende de: accounts (autenticação)
  ├── Usa: common (serializers)
  └── Schema DB: cargaorglot
🛠️ Configuração
Adicionar ao INSTALLED_APPS
python
INSTALLED_APPS = [
    # ...
    'carga_org_lot',
]
Configurar API Externa
python
# settings.py
API_EXTERNA_URL = 'https://api.externa.gov.br'
API_EXTERNA_CLIENT_ID = 'seu_client_id'
API_EXTERNA_CLIENT_SECRET = 'seu_client_secret'
📖 Referências
Documentação API Externa

Formato de Organogramas

Carga Org/Lot - Sistema de Carga de Organogramas e Lotações
