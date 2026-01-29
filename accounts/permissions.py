# accounts/permissions.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserRole, RolePermission

def get_user_permissions_for_active_role(user, app_code):
    """
    Retorna lista de codenames de permissões para o papel ativo do usuário
    
    Args:
        user: Instância do usuário
        app_code: Código da aplicação (ex: 'ACOES_PNGI')
    
    Returns:
        QuerySet de codenames ou lista vazia
    """
    if user.is_superuser:
        from django.contrib.auth.models import Permission
        return Permission.objects.all().values_list('codename', flat=True)
    
    session_key = f'active_role_{app_code}'
    # Não use request.session aqui, receba role_id como parâmetro
    # Esta função será melhorada no decorator
    
    return []


def has_permission(permission_codename):
    """
    Decorator para verificar se o papel ativo tem uma permissão específica
    
    Uso:
        @has_permission('add_eixo')
        def minha_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            # Superuser tem tudo
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Verifica se tem papel ativo
            if not hasattr(request, 'active_role') or not request.active_role:
                messages.error(request, 'Você precisa selecionar um perfil de acesso')
                return redirect('accounts:select_role', app_code='PORTAL')
            
            # Busca permissões do papel ativo
            role_permissions = RolePermission.objects.filter(
                role=request.active_role.role
            ).select_related('permission')
            
            permission_codenames = [
                rp.permission.codename for rp in role_permissions
            ]
            
            # Verifica se tem a permissão
            if permission_codename in permission_codenames:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request, 
                    f'Seu perfil "{request.active_role.role.nomeperfil}" não possui permissão para esta ação'
                )
                return redirect('portal:dashboard')
        
        return wrapper
    return decorator


def has_any_permission(*permission_codenames):
    """
    Decorator para verificar se tem QUALQUER UMA das permissões listadas
    
    Uso:
        @has_any_permission('add_eixo', 'change_eixo', 'view_eixo')
        def minha_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if not hasattr(request, 'active_role') or not request.active_role:
                messages.error(request, 'Você precisa selecionar um perfil de acesso')
                return redirect('accounts:select_role', app_code='PORTAL')
            
            role_permissions = RolePermission.objects.filter(
                role=request.active_role.role
            ).select_related('permission')
            
            user_codenames = {rp.permission.codename for rp in role_permissions}
            
            # Verifica se tem QUALQUER uma das permissões
            if any(perm in user_codenames for perm in permission_codenames):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Você não possui permissão para acessar esta página')
                return redirect('portal:dashboard')
        
        return wrapper
    return decorator


def has_all_permissions(*permission_codenames):
    """
    Decorator para verificar se tem TODAS as permissões listadas
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if not hasattr(request, 'active_role') or not request.active_role:
                messages.error(request, 'Você precisa selecionar um perfil de acesso')
                return redirect('accounts:select_role', app_code='PORTAL')
            
            role_permissions = RolePermission.objects.filter(
                role=request.active_role.role
            ).select_related('permission')
            
            user_codenames = {rp.permission.codename for rp in role_permissions}
            
            # Verifica se tem TODAS as permissões
            if all(perm in user_codenames for perm in permission_codenames):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Você não possui todas as permissões necessárias')
                return redirect('portal:dashboard')
        
        return wrapper
    return decorator
