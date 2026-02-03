"""
Template tags customizadas para verificação de permissões no Ações PNGI.

Este módulo fornece tags que simplificam verificações de permissões nos templates.
"""

from django import template
from accounts.models import UserRole

register = template.Library()


@register.simple_tag(takes_context=True)
def has_perm(context, permission_codename):
    """
    Verifica se o usuário tem uma permissão específica no Ações PNGI.
    
    Uso:
        {% load acoes_permissions %}
        {% has_perm 'add_eixo' as can_add %}
        {% if can_add %}
            <button>Criar Eixo</button>
        {% endif %}
    
    Args:
        context: Contexto do template
        permission_codename: Codename da permissão (ex: 'add_eixo')
    
    Returns:
        bool: True se tem a permissão, False caso contrário
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False
    
    # Usar o método has_app_perm do modelo User customizado
    return request.user.has_app_perm('ACOES_PNGI', permission_codename)


@register.simple_tag(takes_context=True)
def can_manage(context, model_name):
    """
    Verifica se o usuário pode gerenciar um modelo (add OU change).
    
    Uso:
        {% can_manage 'eixo' as can_manage_eixo %}
        {% if can_manage_eixo %}
            <a href="...">Gerenciar Eixos</a>
        {% endif %}
    
    Args:
        context: Contexto do template
        model_name: Nome do modelo (ex: 'eixo')
    
    Returns:
        bool: True se pode adicionar OU editar
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False
    
    can_add = request.user.has_app_perm('ACOES_PNGI', f'add_{model_name}')
    can_change = request.user.has_app_perm('ACOES_PNGI', f'change_{model_name}')
    
    return can_add or can_change


@register.simple_tag(takes_context=True)
def has_any_perm(context, *permission_codenames):
    """
    Verifica se o usuário tem QUALQUER uma das permissões listadas.
    
    Uso:
        {% has_any_perm 'add_eixo' 'change_eixo' 'delete_eixo' as has_eixo_perm %}
        {% if has_eixo_perm %}
            <div>Você pode gerenciar eixos</div>
        {% endif %}
    
    Args:
        context: Contexto do template
        *permission_codenames: Lista de codenames de permissões
    
    Returns:
        bool: True se tem pelo menos uma permissão
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False
    
    for perm in permission_codenames:
        if request.user.has_app_perm('ACOES_PNGI', perm):
            return True
    
    return False


@register.simple_tag(takes_context=True)
def has_all_perms(context, *permission_codenames):
    """
    Verifica se o usuário tem TODAS as permissões listadas.
    
    Uso:
        {% has_all_perms 'add_eixo' 'change_eixo' 'view_eixo' as is_eixo_admin %}
        {% if is_eixo_admin %}
            <div>Administrador de Eixos</div>
        {% endif %}
    
    Args:
        context: Contexto do template
        *permission_codenames: Lista de codenames de permissões
    
    Returns:
        bool: True se tem todas as permissões
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False
    
    for perm in permission_codenames:
        if not request.user.has_app_perm('ACOES_PNGI', perm):
            return False
    
    return True


@register.simple_tag(takes_context=True)
def get_user_role(context):
    """
    Obtém o role do usuário no Ações PNGI.
    
    Uso:
        {% get_user_role as user_role %}
        <p>Seu perfil: {{ user_role.nomeperfil }}</p>
    
    Args:
        context: Contexto do template
    
    Returns:
        Role ou None: Instância do Role ou None se não encontrado
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return None
    
    user_role = UserRole.objects.filter(
        user=request.user,
        aplicacao__codigointerno='ACOES_PNGI'
    ).select_related('role').first()
    
    return user_role.role if user_role else None


@register.filter
def has_model_perm(user, model_action):
    """
    Filter para verificar permissão inline.
    
    Uso:
        {% if user|has_model_perm:'add_eixo' %}
            <button>Adicionar</button>
        {% endif %}
    
    Args:
        user: Instância do usuário
        model_action: String no formato '<action>_<model>' (ex: 'add_eixo')
    
    Returns:
        bool: True se tem a permissão
    """
    if not user or not user.is_authenticated:
        return False
    
    return user.has_app_perm('ACOES_PNGI', model_action)


@register.inclusion_tag('acoes_pngi/components/permission_badge.html', takes_context=True)
def permission_badge(context, permission_codename, label=None):
    """
    Renderiza um badge visual indicando se o usuário tem a permissão.
    
    Uso:
        {% permission_badge 'add_eixo' 'Criar Eixo' %}
    
    Args:
        context: Contexto do template
        permission_codename: Codename da permissão
        label: Label opcional para o badge
    
    Returns:
        dict: Contexto para o template do badge
    """
    request = context.get('request')
    has_permission = False
    
    if request and request.user.is_authenticated:
        has_permission = request.user.has_app_perm('ACOES_PNGI', permission_codename)
    
    return {
        'has_permission': has_permission,
        'label': label or permission_codename,
        'permission_codename': permission_codename
    }
