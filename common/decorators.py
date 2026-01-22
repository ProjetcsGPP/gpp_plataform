"""
Decorators reutilizáveis usando contexto de aplicação
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import UserRole


def require_app_access(redirect_to='portal:home'):
    """
    Decorator que verifica se usuário tem acesso à aplicação do contexto.
    
    Uso:
        @require_app_access()
        def minha_view(request):
            # Usuário tem acesso garantido
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verifica autenticação
            if not request.user.is_authenticated:
                messages.error(request, 'Faça login para continuar')
                return redirect('portal:login')
            
            # Pega app do contexto
            app_code = request.app_context.get('code')
            
            if not app_code:
                messages.error(request, 'Aplicação não identificada')
                return redirect(redirect_to)
            
            # Verifica permissão
            has_access = UserRole.objects.filter(
                user=request.user,
                aplicacao__codigointerno=app_code
            ).exists()
            
            if not has_access:
                messages.error(
                    request,
                    f'Você não tem permissão para acessar {request.app_context["name"]}'
                )
                return redirect(redirect_to)
            
            # Tudo OK, executa a view
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
