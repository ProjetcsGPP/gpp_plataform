from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def require_acoes_permission(perm_codename):
    """
    Decorator para views que requerem permissão específica
    
    Uso:
    @require_acoes_permission('add_eixo')
    def criar_eixo(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            
            if not request.user.has_app_perm('ACOES_PNGI', perm_codename):
                messages.error(
                    request,
                    f'Você não tem permissão: {perm_codename}'
                )
                return redirect('acoes_pngi:dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_acoes_role(*allowed_roles):
    """
    Decorator para verificar role específica
    
    Uso:
    @require_acoes_role('GESTOR_PNGI', 'COORDENADOR_PNGI')
    def configuracoes(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Buscar role do usuário
            from accounts.models import UserRole
            user_role = UserRole.objects.filter(
                user=request.user,
                aplicacao__codigointerno='ACOES_PNGI'
            ).select_related('role').first()
            
            if not user_role or user_role.role.codigoperfil not in allowed_roles:
                messages.error(
                    request,
                    f'Acesso negado. Role necessária: {", ".join(allowed_roles)}'
                )
                return redirect('acoes_pngi:dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def ajax_require_permission(perm_codename):
    """
    Decorator para views AJAX que retorna JSON
    
    Uso:
    @ajax_require_permission('delete_eixo')
    def deletar_eixo_ajax(request, pk):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            from django.http import JsonResponse
            
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Não autenticado'}, status=401)
            
            if not request.user.has_app_perm('ACOES_PNGI', perm_codename):
                return JsonResponse({
                    'error': 'Sem permissão',
                    'required': perm_codename
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
