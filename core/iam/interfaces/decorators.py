"""IAM Decorators for Web Views

Provides function decorators for Django views that enforce
authorization rules using IAM services.
"""

from functools import wraps
from typing import List, Callable
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from ..services.authorization_service import AuthorizationService


def require_permission(app_code: str, permission_codename: str) -> Callable:
    """Decorator requiring specific permission
    
    Args:
        app_code: Application code (e.g., 'ACOES_PNGI')
        permission_codename: Permission codename (e.g., 'add_eixo')
        
    Returns:
        Decorated view function
        
    Example:
        >>> @require_permission('ACOES_PNGI', 'add_eixo')
        >>> def create_eixo(request):
        >>>     # Only users with 'add_eixo' permission can access
        >>>     return render(request, 'eixo_form.html')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request: HttpRequest, *args, **kwargs):
            if AuthorizationService.user_has_permission(
                request.user, app_code, permission_codename
            ):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request,
                    f'Você não possui permissão para esta ação. '
                    f'Permissão necessária: {permission_codename}'
                )
                return redirect('portal:dashboard')
        return wrapper
    return decorator


def require_any_permission(
    app_code: str,
    *permission_codenames: str
) -> Callable:
    """Decorator requiring ANY of the listed permissions
    
    Args:
        app_code: Application code
        *permission_codenames: Permission codenames
        
    Example:
        >>> @require_any_permission('ACOES_PNGI', 'add_eixo', 'change_eixo')
        >>> def manage_eixo(request, pk=None):
        >>>     # Can add OR change eixo
        >>>     ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request: HttpRequest, *args, **kwargs):
            if AuthorizationService.user_has_any_permission(
                request.user, app_code, list(permission_codenames)
            ):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request,
                    'Você não possui nenhuma das permissões necessárias '
                    'para acessar esta página'
                )
                return redirect('portal:dashboard')
        return wrapper
    return decorator


def require_all_permissions(
    app_code: str,
    *permission_codenames: str
) -> Callable:
    """Decorator requiring ALL listed permissions
    
    Args:
        app_code: Application code
        *permission_codenames: Permission codenames
        
    Example:
        >>> @require_all_permissions(
        >>>     'ACOES_PNGI', 'view_eixo', 'change_eixo', 'delete_eixo'
        >>> )
        >>> def full_eixo_management(request):
        >>>     # Must have all three permissions
        >>>     ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request: HttpRequest, *args, **kwargs):
            if AuthorizationService.user_has_all_permissions(
                request.user, app_code, list(permission_codenames)
            ):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request,
                    'Você não possui todas as permissões necessárias '
                    'para acessar esta página'
                )
                return redirect('portal:dashboard')
        return wrapper
    return decorator


def require_role(app_code: str, *role_codes: str) -> Callable:
    """Decorator requiring one of the specified roles
    
    Args:
        app_code: Application code
        *role_codes: Role codes
        
    Example:
        >>> @require_role('ACOES_PNGI', 'GESTOR_PNGI', 'COORDENADOR_PNGI')
        >>> def management_view(request):
        >>>     # Only gestores and coordenadores can access
        >>>     ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request: HttpRequest, *args, **kwargs):
            if AuthorizationService.user_has_any_role(
                request.user, app_code, list(role_codes)
            ):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request,
                    f'Acesso restrito. Perfis permitidos: {", ".join(role_codes)}'
                )
                return redirect('portal:dashboard')
        return wrapper
    return decorator


def require_any_role(app_code: str, *role_codes: str) -> Callable:
    """Alias for require_role (semantic clarity)
    
    Example:
        >>> @require_any_role('ACOES_PNGI', 'GESTOR_PNGI', 'COORDENADOR_PNGI')
        >>> def view_func(request):
        >>>     ...
    """
    return require_role(app_code, *role_codes)