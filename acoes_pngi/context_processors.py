"""
Context processors para disponibilizar dados em todos os templates do Ações PNGI.
"""

from accounts.models import UserRole


def acoes_permissions(request):
    """
    Disponibiliza permissões do Ações PNGI para todos os templates.
    
    Uso nos templates:
        {% if can_add_eixo %}
            <a href="{% url 'acoes_pngi_web:eixo_create' %}">Novo Eixo</a>
        {% endif %}
    """
    context = {
        # Flags gerais de acesso
        'has_acoes_access': False,
        'acoes_role': None,
        'acoes_role_display': None,
        
        # Permissões de Eixos
        'can_add_eixo': False,
        'can_change_eixo': False,
        'can_delete_eixo': False,
        'can_view_eixo': False,
        
        # Permissões de Situações
        'can_add_situacao': False,
        'can_change_situacao': False,
        'can_delete_situacao': False,
        'can_view_situacao': False,
        
        # Permissões de Vigências
        'can_add_vigencia': False,
        'can_change_vigencia': False,
        'can_delete_vigencia': False,
        'can_view_vigencia': False,
        
        # Grupos de permissões
        'can_manage_config': False,
        'can_manage_acoes': False,
        'can_delete_any': False,
    }
    
    # Se usuário não está autenticado, retorna permissões vazias
    if not request.user.is_authenticated:
        return context
    
    # Verifica se usuário tem acesso ao Ações PNGI
    user_role = UserRole.objects.filter(
        user=request.user,
        aplicacao__codigointerno='ACOES_PNGI'
    ).select_related('role').first()
    
    if not user_role:
        return context
    
    # Usuário tem acesso
    context['has_acoes_access'] = True
    context['acoes_role'] = user_role.role.codigoperfil  # ← CORRIGIDO
    context['acoes_role_display'] = user_role.role.nomeperfil  # ← CORRIGIDO
    
    # Permissões de Eixos
    context['can_add_eixo'] = request.user.has_app_perm('ACOES_PNGI', 'add_eixo')
    context['can_change_eixo'] = request.user.has_app_perm('ACOES_PNGI', 'change_eixo')
    context['can_delete_eixo'] = request.user.has_app_perm('ACOES_PNGI', 'delete_eixo')
    context['can_view_eixo'] = request.user.has_app_perm('ACOES_PNGI', 'view_eixo')
    
    # Permissões de Situações
    context['can_add_situacao'] = request.user.has_app_perm('ACOES_PNGI', 'add_situacaoacao')
    context['can_change_situacao'] = request.user.has_app_perm('ACOES_PNGI', 'change_situacaoacao')
    context['can_delete_situacao'] = request.user.has_app_perm('ACOES_PNGI', 'delete_situacaoacao')
    context['can_view_situacao'] = request.user.has_app_perm('ACOES_PNGI', 'view_situacaoacao')
    
    # Permissões de Vigências
    context['can_add_vigencia'] = request.user.has_app_perm('ACOES_PNGI', 'add_vigenciapngi')
    context['can_change_vigencia'] = request.user.has_app_perm('ACOES_PNGI', 'change_vigenciapngi')
    context['can_delete_vigencia'] = request.user.has_app_perm('ACOES_PNGI', 'delete_vigenciapngi')
    context['can_view_vigencia'] = request.user.has_app_perm('ACOES_PNGI', 'view_vigenciapngi')
    
    # Grupos de permissões (para simplificar uso nos templates)
    context['can_manage_config'] = (
        context['can_add_eixo'] or
        context['can_add_situacao'] or
        context['can_add_vigencia']
    )
    
    context['can_manage_acoes'] = False  # TODO: quando implementar modelo de Ações
    
    context['can_delete_any'] = (
        context['can_delete_eixo'] or
        context['can_delete_situacao'] or
        context['can_delete_vigencia']
    )
    
    return context
