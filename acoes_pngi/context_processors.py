"""
Context Processors para Ações PNGI
Injeta informações da aplicação nos templates com estrutura padronizada

Padrão: Segue o mesmo modelo de carga_org_lot/context_processors.py
"""

from django.urls import resolve
from accounts.models import Aplicacao, UserRole
import logging

logger = logging.getLogger(__name__)


def acoes_permissions(request):
    """
    Context processor de permissões para Ações PNGI.
    Injeta permissões do usuário na aplicação.
    
    Retorna:
        - acoes_permissions: Lista de codenomes de permissão (ex: ['view_eixo', 'add_eixo'])
        - acoes_models_perms: Dict com permissões por modelo
    """
    context = {
        'acoes_permissions': [],
        'acoes_models_perms': {},
    }
    
    if request.user.is_authenticated:
        try:
            # Busca permissões do usuário para a app ACOES_PNGI
            permissions = request.user.get_app_permissions('ACOES_PNGI')
            context['acoes_permissions'] = list(permissions)
            
            # Organiza permissões por modelo para fácil acesso nos templates
            models_with_perms = {
                'eixo': {'view': False, 'add': False, 'change': False, 'delete': False},
                'situacaoacao': {'view': False, 'add': False, 'change': False, 'delete': False},
                'vigenciapngi': {'view': False, 'add': False, 'change': False, 'delete': False},
            }
            
            for perm in permissions:
                for model_name in models_with_perms:
                    if model_name in perm:
                        # Extrai a operação (view, add, change, delete)
                        for operation in ['view', 'add', 'change', 'delete']:
                            if f'{operation}_{model_name}' == perm:
                                models_with_perms[model_name][operation] = True
                                break
            
            context['acoes_models_perms'] = models_with_perms
            
        except Exception as e:
            logger.error(f"Erro ao carregar permissões de Ações PNGI: {str(e)}")
    
    return context


def acoes_pngi_context(request):
    """
    Context processor para a aplicação Ações PNGI.
    Injeta informações da aplicação e perfis do usuário.
    
    Padrão: Baseado em carga_org_lot/context_processors.py
    
    Retorna:
        - app_context: Informações sobre a aplicação atual
            - code: Código interno (ACOES_PNGI)
            - name: Nome da aplicação
            - icon: Ícone FontAwesome
            - url_namespace: Namespace da URL
        
        - user_roles_in_app: Lista de perfis do usuário na aplicação
            - id: ID do perfil (role)
            - name: Nome do perfil (nomeperfil)
            - code: Código do perfil (codigoperfil)
            - is_active: Se é o perfil ativo na sessão
    
    Exemplo de uso em template:
        {% if app_context %}
            <h1>{{ app_context.name }}</h1>
        {% endif %}
        
        {% for role in user_roles_in_app %}
            <span class="{% if role.is_active %}active{% endif %}">
                {{ role.name }}
            </span>
        {% endfor %}
    """
    context = {}
    
    # Detecta se está em uma view do acoes_pngi
    if request.resolver_match and request.resolver_match.app_name == 'acoes_pngi':
        # Busca informações da aplicação
        try:
            aplicacao = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
            
            context['app_context'] = {
                'code': aplicacao.codigointerno,
                'name': aplicacao.nomeaplicacao,
                'icon': 'fas fa-tasks',  # Ícone específico para Ações PNGI
                'url_namespace': 'acoes_pngi',
            }
        except Aplicacao.DoesNotExist:
            # Fallback se aplicação não existir no BD
            context['app_context'] = {
                'code': 'ACOES_PNGI',
                'name': 'Ações PNGI',
                'icon': 'fas fa-tasks',
                'url_namespace': 'acoes_pngi',
            }
        
        # Se usuário autenticado, busca seus perfis nesta app
        if request.user.is_authenticated:
            try:
                user_roles = UserRole.objects.filter(
                    user=request.user,
                    aplicacao__codigointerno='ACOES_PNGI'
                ).select_related('role', 'aplicacao')
                
                # Pega o perfil ativo da sessão
                active_role_id = request.session.get('active_role_acoes_pngi')
                
                context['user_roles_in_app'] = [
                    {
                        'id': ur.role.id,
                        'name': ur.role.nomeperfil,  # Campo correto do modelo Role
                        'code': ur.role.codigoperfil,
                        'is_active': (active_role_id == ur.role.id) if active_role_id else (ur == user_roles.first())
                    }
                    for ur in user_roles
                ]
            except Exception as e:
                logger.error(f"Erro ao carregar perfis do usuário em Ações PNGI: {str(e)}")
                context['user_roles_in_app'] = []
    
    return context


def acoes_pngi_models_context(request):
    """
    Context processor adicional que injeta informações específicas dos modelos
    de Ações PNGI para uso em templates.
    
    Útil para formulários e listas que precisam de metadata dos modelos.
    
    Retorna:
        - acoes_models_info: Dict com informações sobre os modelos
            - eixo: Info sobre modelo Eixo
            - situacao_acao: Info sobre modelo SituacaoAcao
            - vigencia_pngi: Info sobre modelo VigenciaPNGI
    
    Exemplo:
        {% for model_key, model_info in acoes_models_info.items %}
            <h3>{{ model_info.verbose_name_plural }}</h3>
        {% endfor %}
    """
    context = {}
    
    # Apenas carrega se estiver no contexto de acoes_pngi
    if request.resolver_match and request.resolver_match.app_name == 'acoes_pngi':
        try:
            from acoes_pngi.models import Eixo, SituacaoAcao, VigenciaPNGI
            
            context['acoes_models_info'] = {
                'eixo': {
                    'model_name': 'eixo',
                    'verbose_name': Eixo._meta.verbose_name,
                    'verbose_name_plural': Eixo._meta.verbose_name_plural,
                    'app_label': Eixo._meta.app_label,
                    'db_table': Eixo._meta.db_table,
                },
                'situacao_acao': {
                    'model_name': 'situacaoacao',
                    'verbose_name': SituacaoAcao._meta.verbose_name,
                    'verbose_name_plural': SituacaoAcao._meta.verbose_name_plural,
                    'app_label': SituacaoAcao._meta.app_label,
                    'db_table': SituacaoAcao._meta.db_table,
                },
                'vigencia_pngi': {
                    'model_name': 'vigenciapngi',
                    'verbose_name': VigenciaPNGI._meta.verbose_name,
                    'verbose_name_plural': VigenciaPNGI._meta.verbose_name_plural,
                    'app_label': VigenciaPNGI._meta.app_label,
                    'db_table': VigenciaPNGI._meta.db_table,
                },
            }
        except Exception as e:
            logger.error(f"Erro ao carregar informações de modelos em Ações PNGI: {str(e)}")
            context['acoes_models_info'] = {}
    
    return context


# ============================================================================
# DOCUMENTAÇÃO DE INTEGRAÇÃO NO settings.py
# ============================================================================
#
# Para integrar os context processors no settings.py:
#
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#                 # ... outros context processors ...
#                 
#                 # ACOES_PNGI Context Processors
#                 'acoes_pngi.context_processors.acoes_permissions',
#                 'acoes_pngi.context_processors.acoes_pngi_context',
#                 'acoes_pngi.context_processors.acoes_pngi_models_context',  # Opcional
#             ],
#         },
#     },
# ]
#
# ============================================================================
