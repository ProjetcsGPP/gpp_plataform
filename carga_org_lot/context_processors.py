"""
Context Processors para Carga Org/Lot
Injeta informações da aplicação nos templates
"""

from accounts.models import UserRole


def carga_org_lot_context(request):
    """
    Injeta contexto específico do Carga Org/Lot nos templates.
    
    Retorna:
        - app_context: Informações sobre a aplicação atual
        - user_roles_carga: Perfis do usuário na aplicação Carga
    """
    context = {}
    
    # Detecta se está em uma view do carga_org_lot
    if request.resolver_match and request.resolver_match.app_name == 'carga_org_lot':
        context['app_context'] = {
            'code': 'CARGA_ORG_LOT',
            'name': 'Carga Org/Lot',
            'icon': 'fas fa-sitemap',
            'url_namespace': 'carga_org_lot',
        }
        
        # Se usuário autenticado, busca seus perfis nesta app
        if request.user.is_authenticated:
            user_roles = UserRole.objects.filter(
                user=request.user,
                aplicacao__codigointerno='CARGA_ORG_LOT'
            ).select_related('role', 'aplicacao')
            
            context['user_roles_in_app'] = [
                {
                    'id': ur.id,
                    'name': ur.role.name,
                    'description': ur.role.description,
                    'is_active': hasattr(request.user, 'active_role') and request.user.active_role == ur
                }
                for ur in user_roles
            ]
    
    return context
