# accounts/context_processors.py
from .models import UserRole

def active_role_context(request):
    """
    Adiciona informações do papel ativo ao contexto de todos os templates
    """
    context = {
        'active_role': None,
        'active_role_name': None,
        'active_role_code': None,
        'user_roles_for_app': [],
    }
    
    if hasattr(request, 'active_role') and request.active_role:
        context['active_role'] = request.active_role
        context['active_role_name'] = request.active_role.role.nomeperfil
        context['active_role_code'] = request.active_role.role.codigoperfil
        
        # Busca todos os papéis do usuário para a aplicação atual
        if request.user.is_authenticated:
            app_code = request.active_role.aplicacao.codigointerno
            context['user_roles_for_app'] = UserRole.objects.filter(
                user=request.user,
                aplicacao__codigointerno=app_code
            ).select_related('role', 'aplicacao')
    
    return context
