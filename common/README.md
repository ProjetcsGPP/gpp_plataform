## 3. common/README.md

```markdown
# Common - Componentes Compartilhados

Aplicação que centraliza utilitários, serializers, serviços e componentes reutilizáveis entre todas as aplicações da GPP Plataform.

## 📋 Visão Geral

A aplicação `common` fornece:

- **Serializers Genéricos**: Classes base para serialização consistente
- **Serviços de Autenticação**: PortalAuthService para integração entre apps
- **Middlewares**: Contexto de aplicação e utilitários
- **Base Classes**: Mixins e classes abstratas reutilizáveis

## 🏗️ Estrutura

common/
├── serializers/
│ ├── init.py
│ ├── base_serializers.py # BaseModelSerializer, TimestampedModelSerializer
│ ├── user_serializers.py # Serializers de User genéricos
│ └── auth_serializers.py # Serializers de autenticação
├── services/
│ ├── init.py
│ └── portal_auth.py # PortalAuthService
├── middleware/
│ ├── init.py
│ └── app_context.py # AppContextMiddleware
├── utils/
│ └── init.py
└── README.md

text

## 🔧 Serializers

### BaseModelSerializer

Serializer base com comportamentos comuns para todos os modelos.

**Recursos**:
- Remoção automática de campos `None` (opcional)
- Validações customizáveis
- Formatação consistente

**Exemplo de uso**:
```python
from common.serializers import BaseModelSerializer

class MeuModelSerializer(BaseModelSerializer):
    class Meta:
        model = MeuModel
        fields = '__all__'
        remove_null_fields = True  # Remove campos None da resposta
TimestampedModelSerializer
Serializer para modelos com campos de timestamp (created_at, updated_at).

Recursos:

Formatação automática de datas: '%Y-%m-%d %H:%M:%S'

Campos read-only por padrão

Herda de BaseModelSerializer

Exemplo de uso:

python
from common.serializers import TimestampedModelSerializer

class EixoSerializer(TimestampedModelSerializer):
    class Meta:
        model = Eixo
        fields = [
            'ideixo',
            'strdescricaoeixo',
            'stralias',
            'created_at',    # Automaticamente formatado
            'updated_at'     # Automaticamente formatado
        ]
        read_only_fields = ['ideixo', 'created_at', 'updated_at']
UserSerializer
Serializer completo para o modelo User com roles e atributos.

Recursos:

Retorna roles do usuário para a aplicação do contexto

Retorna atributos customizados da aplicação

Filtragem automática por APP_CODE

Exemplo de uso:

python
from common.serializers import UserSerializer

# Na view
serializer = UserSerializer(
    user,
    context={
        'app_code': 'ACOES_PNGI',  # Filtra roles/atributos por app
        'request': request
    }
)

# Resposta incluirá:
# - Dados básicos do usuário
# - roles: lista de roles para ACOES_PNGI
# - attributes: dict de atributos para ACOES_PNGI
UserListSerializer
Versão otimizada para listagem de usuários (sem roles/atributos).

python
from common.serializers import UserListSerializer

users = User.objects.filter(is_active=True)
serializer = UserListSerializer(users, many=True)
UserCreateSerializer
Serializer para criação/sincronização de usuários via portal.

Exemplo de uso:

python
from common.serializers import UserCreateSerializer

serializer = UserCreateSerializer(
    data={
        'email': 'novo@example.com',
        'name': 'Novo Usuário',
        'roles': ['GESTOR_PNGI'],
        'attributes': {'can_upload': 'true'}
    },
    context={'app_code': 'ACOES_PNGI'}
)

if serializer.is_valid():
    user = serializer.save()  # Cria/atualiza usuário com roles e atributos
    created = serializer.validated_data['_created']
UserUpdateSerializer
Serializer para atualização parcial de usuários.

python
from common.serializers import UserUpdateSerializer

serializer = UserUpdateSerializer(
    user,
    data={'is_active': False},
    partial=True
)

if serializer.is_valid():
    serializer.save()

## 🔄 AppContextMiddleware

### O Que É?

Middleware que detecta automaticamente qual aplicação está sendo acessada baseado na URL, disponibilizando essas informações em `request.app_context` para todas as views e serializers.

### Como Funciona?

```python
# Configurado em settings.py
MIDDLEWARE = [
    # ...
    'common.middleware.app_context.AppContextMiddleware',  # ← Adicione
]
O middleware analisa a URL da requisição e identifica a aplicação:

URL	Aplicação Detectada
/api/v1/acoes_pngi/*	ACOES_PNGI
/acoes-pngi/*	ACOES_PNGI
/api/v1/carga/*	CARGA_ORG_LOT
/carga_org_lot/*	CARGA_ORG_LOT
/api/v1/portal/*	PORTAL
/api/v1/auth/*	PORTAL
/	PORTAL
/admin/*	None (sem contexto)
/static/*	None (sem contexto)
Estrutura do app_context
python
request.app_context = {
    'code': 'ACOES_PNGI',           # Código da aplicação
    'instance': <Aplicacao object>,  # Objeto Aplicacao do banco
    'name': 'Gestão de Ações PNGI'  # Nome amigável
}
Uso nas Views
Antes (sem middleware):

python
@api_view(['POST'])
def portal_auth(request):
    app_code = 'ACOES_PNGI'  # ❌ Hardcoded
    
    portal_service = get_portal_auth_service(app_code)
    user = portal_service.authenticate_user(token)
    
    serializer = UserSerializer(
        user,
        context={'app_code': app_code, 'request': request}  # ❌ Manual
    )
    return Response(serializer.data)
Depois (com middleware):

python
@api_view(['POST'])
def portal_auth(request):
    app_code = request.app_context['code']  # ✅ Automático
    
    portal_service = get_portal_auth_service(app_code)
    user = portal_service.authenticate_user(token)
    
    serializer = UserSerializer(user, context={'request': request})  # ✅ Simples
    return Response(serializer.data)
Uso nos Serializers
Os serializers UserSerializer e UserCreateSerializer detectam automaticamente a aplicação:

python
# Na view, basta passar request
serializer = UserSerializer(user, context={'request': request})

# O serializer internamente faz:
# app_code = request.app_context['code']
# E filtra roles/attributes pela aplicação correta
Cache de Performance
O middleware mantém cache em memória dos objetos Aplicacao para evitar queries repetidas ao banco:

python
# Primeira requisição: busca do banco
GET /api/v1/acoes_pngi/eixos/  → Query ao banco

# Requisições seguintes: usa cache
GET /api/v1/acoes_pngi/situacoes/  → Usa cache (sem query)
GET /api/v1/acoes_pngi/vigencias/  → Usa cache (sem query)
Verificação de Permissões Simplificada
python
from accounts.models import UserRole

def minha_view(request):
    # ✅ Usa app_context automaticamente
    app_code = request.app_context['code']
    
    has_access = UserRole.objects.filter(
        user=request.user,
        aplicacao__codigointerno=app_code
    ).exists()
    
    if not has_access:
        return Response({'detail': 'Acesso negado'}, status=403)
    
    # ... lógica da view
Decorator Auxiliar
Use o decorator @require_app_access() para validação automática:

python
from common.decorators import require_app_access

@require_app_access()
def dashboard_view(request):
    # ✅ Acesso já validado automaticamente
    # ✅ request.app_context já disponível
    
    app = request.app_context['instance']
    return render(request, 'dashboard.html', {'app': app})
Testes
Execute os testes do middleware:

bash
# Testar middleware
python manage.py test common.tests.test_middleware

# Testar integração com serializers
python manage.py test common.tests.test_serializers

# Testar tudo de common
python manage.py test common
Logs
O middleware registra logs em nível DEBUG:

python
import logging
logger = logging.getLogger(__name__)

# Em settings.py, configure logging para ver:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'common.middleware.app_context': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Ative para ver detecções
        },
    },
}
Exemplo de log:

text
DEBUG Request /api/v1/acoes_pngi/eixos/ → App: ACOES_PNGI
INFO App cache carregado: ['PORTAL', 'ACOES_PNGI', 'CARGA_ORG_LOT']
Troubleshooting
Problema: request.app_context['code'] é None

Solução: Verifique se a URL está mapeada em AppContextMiddleware.URL_TO_APP. Se não estiver, adicione:

python
# common/middleware/app_context.py
URL_TO_APP = {
    # ... existentes
    '/nova-app/': 'NOVA_APP',  # ← Adicione
}
Problema: Serializer não filtra roles corretamente

Solução: Certifique-se de passar context={'request': request} ao serializar:

python
# ❌ Errado
serializer = UserSerializer(user)

# ✅ Correto
serializer = UserSerializer(user, context={'request': request})
Compatibilidade
O middleware é retrocompatível. Se request.app_context não estiver disponível (ex: testes antigos), os serializers fazem fallback para context['app_code'] manual:

python
# Ainda funciona (para compatibilidade)
serializer = UserSerializer(
    user,
    context={'app_code': 'ACOES_PNGI'}  # Fallback manual
)
AppContextMiddleware - Detecção automática de aplicação por URL

text

## 5. Criar Decorator Auxiliar

### common/decorators.py

```python
"""
Decorators reutilizáveis usando contexto de aplicação.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from accounts.models import UserRole


def require_app_access(redirect_to='portal:home', api_mode=False):
    """
    Decorator que verifica se usuário tem acesso à aplicação do contexto.
    
    Args:
        redirect_to: Nome da URL para redirecionar se não tiver acesso (modo web)
        api_mode: Se True, retorna JSON 403 ao invés de redirect (modo API)
    
    Uso (Web):
        @require_app_access()
        def dashboard(request):
            # Usuário autenticado e com acesso garantido
            ...
    
    Uso (API):
        @require_app_access(api_mode=True)
        def api_view(request):
            # Retorna 403 JSON se não tiver acesso
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verifica autenticação
            if not request.user.is_authenticated:
                if api_mode:
                    return JsonResponse(
                        {'detail': 'Autenticação necessária'},
                        status=401
                    )
                messages.error(request, 'Faça login para continuar')
                return redirect('portal:login')
            
            # Pega app do contexto (adicionado pelo middleware)
            if not hasattr(request, 'app_context'):
                if api_mode:
                    return JsonResponse(
                        {'detail': 'Contexto de aplicação não disponível'},
                        status=500
                    )
                messages.error(request, 'Erro de configuração do sistema')
                return redirect(redirect_to)
            
            app_code = request.app_context.get('code')
            app_name = request.app_context.get('name')
            
            if not app_code:
                if api_mode:
                    return JsonResponse(
                        {'detail': 'Aplicação não identificada'},
                        status=500
                    )
                messages.error(request, 'Aplicação não identificada')
                return redirect(redirect_to)
            
            # Verifica permissão
            has_access = UserRole.objects.filter(
                user=request.user,
                aplicacao__codigointerno=app_code
            ).exists()
            
            if not has_access:
                if api_mode:
                    return JsonResponse(
                        {'detail': f'Acesso negado a {app_name}'},
                        status=403
                    )
                messages.error(
                    request,
                    f'Você não tem permissão para acessar {app_name}'
                )
                return redirect(redirect_to)
            
            # Tudo OK, executa a view
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def require_attribute(attribute_key, expected_value='true', api_mode=False):
    """
    Decorator que verifica se usuário tem atributo específico para a aplicação.
    
    Args:
        attribute_key: Chave do atributo (ex: 'can_upload')
        expected_value: Valor esperado (default: 'true')
        api_mode: Se True, retorna JSON ao invés de redirect
    
    Uso:
        @require_attribute('can_upload')
        def upload_view(request):
            # Usuário tem atributo can_upload=true garantido
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            from accounts.models import Attribute
            
            # Verifica autenticação
            if not request.user.is_authenticated:
                if api_mode:
                    return JsonResponse({'detail': 'Autenticação necessária'}, status=401)
                return redirect('portal:login')
            
            # Pega app do contexto
            app_code = request.app_context.get('code')
            
            if not app_code:
                if api_mode:
                    return JsonResponse({'detail': 'Aplicação não identificada'}, status=500)
                messages.error(request, 'Aplicação não identificada')
                return redirect('portal:home')
            
            # Verifica atributo
            has_attribute = Attribute.objects.filter(
                user=request.user,
                aplicacao__codigointerno=app_code,
                key=attribute_key,
                value=expected_value
            ).exists()
            
            if not has_attribute:
                if api_mode:
                    return JsonResponse(
                        {'detail': f'Permissão {attribute_key} necessária'},
                        status=403
                    )
                messages.error(
                    request,
                    f'Você não tem permissão para realizar esta ação'
                )
                return redirect('portal:home')
            
            # Tudo OK
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
Exemplo de uso dos decorators:
python
# acoes_pngi/views/web_views.py

from common.decorators import require_app_access, require_attribute

@require_app_access()
def acoes_pngi_dashboard(request):
    """Dashboard - acesso já validado"""
    app = request.app_context['instance']
    
    # ... lógica
    return render(request, 'acoes_pngi/dashboard.html', {'app': app})


@require_app_access()
@require_attribute('can_upload')
def upload_view(request):
    """Upload - requer acesso E atributo can_upload"""
    
    # Usuário garantido ter permissão
    # ... processar upload
    return render(request, 'upload.html')
6. Comandos para Implementar
bash
# 1. Criar arquivos
touch common/middleware/__init__.py
touch common/middleware/app_context.py
touch common/decorators.py
touch common/tests/__init__.py
touch common/tests/test_middleware.py
touch common/tests/test_serializers.py

# 2. Adicionar middleware ao settings.py
# (edite manualmente gpp_plataform/settings.py)

# 3. Executar testes
python manage.py test common.tests

# 4. Verificar funcionamento
python manage.py runserver
# Acesse http://localhost:8000/api/v1/acoes_pngi/eixos/

# 5. Commit
git add .
git commit -m "feat: Implementa AppContextMiddleware com detecção automática de aplicação

- Adiciona middleware para detectar app por URL
- Atualiza serializers para usar request.app_context
- Cria decorators @require_app_access e @require_attribute
- Adiciona testes completos do middleware
- Atualiza documentação do common/README.md
- Melhora performance com cache de aplicações"

git push origin main