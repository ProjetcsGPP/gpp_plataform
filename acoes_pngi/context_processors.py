"""
Context processors para disponibilizar dados em todos os templates do Ações PNGI.

Este módulo fornece um sistema automatizado de permissões que:
- Carrega dinamicamente as permissões do usuário baseado em seu role
- Disponibiliza variáveis de permissão nos templates
- Agrupa permissões por modelo para facilitar uso
"""

from django.contrib.contenttypes.models import ContentType
from accounts.models import UserRole, RolePermission
from django.contrib.auth.models import Permission
from django.core.cache import cache


def acoes_permissions(request):
    """
    Context processor que disponibiliza permissões do Ações PNGI automaticamente.
    
    Carrega todas as permissões do role do usuário e cria variáveis no contexto:
    - can_<action>_<model>: Para cada permissão individual
    - can_manage_<model>: Se tem add/change
    - can_full_<model>: Se tem todas as 4 permissões
    
    Uso nos templates:
        {% if can_add_eixo %}
            <a href="{% url 'acoes_pngi_web:eixo_create' %}">Novo Eixo</a>
        {% endif %}
        
        {% if can_manage_eixo %}
            <!-- Usuário pode adicionar OU editar eixos -->
        {% endif %}
    
    Returns:
        dict: Dicionário com flags de permissão e metadados do usuário
    """
    # Modelos do acoes_pngi para garantir que as chaves sempre existam
    ACOES_MODELS = [
        'eixo', 'situacaoacao', 'vigenciapngi', 'acao', 'acaoxml',
        'acaopngilog', 'eixoxml', 'situacaoacaoxml', 'vigenciapngixml'
    ]
    
    # Inicializar contexto com todas as permissões = False
    context = {
        # Flags gerais de acesso
        'has_acoes_access': False,
        'acoes_role': None,
        'acoes_role_display': None,
        'acoes_permissions_list': [],  # Lista de todas as permissões
    }
    
    # Inicializar todas as permissões como False
    for model in ACOES_MODELS:
        for action in ['add', 'change', 'delete', 'view']:
            context[f'can_{action}_{model}'] = False
        context[f'can_manage_{model}'] = False
        context[f'can_full_{model}'] = False
        context[f'can_edit_{model}'] = False
    
    # Grupos de permissões (compatibilidade com versão antiga)
    context['can_manage_config'] = False
    context['can_delete_any'] = False
    
    # Se usuário não está autenticado, retorna permissões vazias
    if not request.user.is_authenticated:
        return context
    
    # Buscar UserRole do usuário para ACOES_PNGI
    user_role = UserRole.objects.filter(
        user=request.user,
        aplicacao__codigointerno='ACOES_PNGI'
    ).select_related('role', 'aplicacao').first()
    
    if not user_role:
        return context
    
    # Usuário tem acesso
    context['has_acoes_access'] = True
    context['acoes_role'] = user_role.role.codigoperfil
    context['acoes_role_display'] = user_role.role.nomeperfil
    
    # Cache key único por usuário e role
    cache_key = f'acoes_perms_{request.user.id}_{user_role.role.id}'
    cached_perms = cache.get(cache_key)
    
    if cached_perms:
        context.update(cached_perms)
        return context
    
    # Buscar todas as permissões do role
    role_permissions = RolePermission.objects.filter(
        role=user_role.role
    ).select_related('permission', 'permission__content_type').values_list(
        'permission__codename',
        'permission__content_type__model',
        'permission__name'
    )
    
    # Dicionário para agrupar permissões por modelo
    models_perms = {}
    
    # Processar cada permissão
    for codename, model, name in role_permissions:
        # Adicionar flag individual: can_<action>_<model>
        context[f'can_{codename}'] = True
        
        # Adicionar à lista de permissões
        context['acoes_permissions_list'].append({
            'codename': codename,
            'model': model,
            'name': name
        })
        
        # Agrupar por modelo
        if model not in models_perms:
            models_perms[model] = {
                'add': False,
                'change': False,
                'delete': False,
                'view': False
            }
        
        # Identificar tipo de ação
        action = codename.split('_')[0]  # add, change, delete, view
        if action in models_perms[model]:
            models_perms[model][action] = True
    
    # Criar flags agregadas por modelo
    for model, perms in models_perms.items():
        # can_manage_<model>: tem add OU change
        context[f'can_manage_{model}'] = perms['add'] or perms['change']
        
        # can_full_<model>: tem todas as 4 permissões
        context[f'can_full_{model}'] = all(perms.values())
        
        # can_edit_<model>: alias para change
        context[f'can_edit_{model}'] = perms['change']
    
    # Grupos de permissões (compatibilidade com versão antiga)
    context['can_manage_config'] = (
        context.get('can_manage_eixo', False) or
        context.get('can_manage_situacaoacao', False) or
        context.get('can_manage_vigenciapngi', False)
    )
    
    context['can_delete_any'] = (
        context.get('can_delete_eixo', False) or
        context.get('can_delete_situacaoacao', False) or
        context.get('can_delete_vigenciapngi', False)
    )
    
    # Cachear por 15 minutos
    permissions_to_cache = {k: v for k, v in context.items() if k not in ['has_acoes_access', 'acoes_role', 'acoes_role_display']}
    cache.set(cache_key, permissions_to_cache, 900)  # 15 minutos
    
    return context


def get_user_app_permissions(user, app_code):
    """
    Helper para obter todas as permissões de um usuário em uma aplicação.
    
    Args:
        user: Instância do usuário
        app_code: Código da aplicação (ex: 'ACOES_PNGI')
    
    Returns:
        set: Conjunto de codenames de permissões
    """
    user_role = UserRole.objects.filter(
        user=user,
        aplicacao__codigointerno=app_code
    ).select_related('role').first()
    
    if not user_role:
        return set()
    
    perms = RolePermission.objects.filter(
        role=user_role.role
    ).values_list('permission__codename', flat=True)
    
    return set(perms)
