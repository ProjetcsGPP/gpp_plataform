"""
Context Processors para Carga Org/Lot
Injeta informações da aplicação nos templates
"""

from accounts.models import UserRole, Aplicacao


def carga_org_lot_context(request):
    """
    Injeta contexto específico do Carga Org/Lot nos templates.
    
    Retorna:
        - app_context: Informações sobre a aplicação atual
        - user_roles_in_app: Perfis do usuário na aplicação Carga
    """
    context = {}
    
    # Detecta se está em uma view do carga_org_lot
    if request.resolver_match and request.resolver_match.app_name == 'carga_org_lot':
        # Busca informações da aplicação
        try:
            aplicacao = Aplicacao.objects.get(codigointerno='CARGA_ORG_LOT')
            
            context['app_context'] = {
                'code': aplicacao.codigointerno,
                'name': aplicacao.nomeaplicacao,
                'icon': 'fas fa-sitemap',
                'url_namespace': 'carga_org_lot',
            }
        except Aplicacao.DoesNotExist:
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
            
            # Pega o perfil ativo da sessão
            active_role_id = request.session.get('active_role_carga_org_lot')
            
            context['user_roles_in_app'] = [
                {
                    'id': ur.role.id,
                    'name': ur.role.nomeperfil,  # Campo correto do modelo Role
                    'code': ur.role.codigoperfil,
                    'is_active': (active_role_id == ur.role.id) if active_role_id else (ur == user_roles.first())
                }
                for ur in user_roles
            ]
    
    return context
