# accounts/templatetags/permission_tags.py
from django import template
from accounts.models import RolePermission

register = template.Library()

@register.simple_tag(takes_context=True)
def has_perm(context, permission_codename):
    """
    Verifica se o papel ativo tem uma permissão
    
    Uso no template:
        {% load permission_tags %}
        {% has_perm 'add_eixo' as can_add %}
        {% if can_add %}
            <button>Adicionar Eixo</button>
        {% endif %}
    """
    request = context.get('request')
    
    if not request or not request.user.is_authenticated:
        return False
    
    if request.user.is_superuser:
        return True
    
    if not hasattr(request, 'active_role') or not request.active_role:
        return False
    
    exists = RolePermission.objects.filter(
        role=request.active_role.role,
        permission__codename=permission_codename
    ).exists()
    
    return exists


@register.filter
def has_any_perm(user, permission_list):
    """
    Verifica se tem qualquer uma das permissões
    
    Uso:
        {% if user|has_any_perm:"add_eixo,change_eixo" %}
            ...
        {% endif %}
    """
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    # Implementação simplificada - melhorar conforme necessário
    return False
