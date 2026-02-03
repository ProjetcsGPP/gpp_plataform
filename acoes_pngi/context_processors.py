from django.urls import resolve
from accounts.models import Aplicacao, UserRole

def acoes_pngi_context(request):
    """
    Context processor para a aplicação Ações PNGI.
    Injeta informações da aplicação e perfis do usuário.
    """
    context = {}
    
    # Verifica se a request atual é de uma view do acoes_pngi
    try:
        resolver_match = resolve(request.path)
        app_name = resolver_match.app_name
        
        # Se não for do acoes_pngi, retorna contexto vazio
        if not app_name or 'acoes_pngi' not in app_name:
            return context
            
    except Exception:
        return context
    
    # Busca a aplicação Ações PNGI
    try:
        aplicacao = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
        
        # Injeta app_context com informações da aplicação
        context['app_context'] = {
            'name': aplicacao.nomeaplicacao,
            'code': aplicacao.codigointerno,
            'icon': 'fas fa-tasks',  # Ícone específico do Ações PNGI
        }
        
        # Se o usuário estiver autenticado, busca seus perfis
        if request.user.is_authenticated:
            # Busca todos os perfis do usuário nesta aplicação
            user_roles = UserRole.objects.filter(
                user=request.user,
                aplicacao=aplicacao
            ).select_related('role')
            
            # Monta lista de perfis com indicação de qual está ativo
            roles_list = []
            active_role_id = request.session.get('active_role_acoes_pngi')  # Perfil ativo na sessão
            
            for ur in user_roles:
                roles_list.append({
                    'id': ur.role.id,
                    'name': ur.role.nomeperfil,
                    'code': ur.role.codigoperfil,
                    'is_active': (active_role_id == ur.role.id) if active_role_id else (ur == user_roles.first())
                })
            
            context['user_roles_in_app'] = roles_list
            
    except Aplicacao.DoesNotExist:
        pass
    
    return context
