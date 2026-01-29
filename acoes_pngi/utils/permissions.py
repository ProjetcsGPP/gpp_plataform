"""
Utilitários para gerenciamento de permissões no Ações PNGI.

Este módulo fornece funções auxiliares para:
- Verificar permissões em views
- Cache de permissões
- Helpers para controle de acesso
"""

from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.core.cache import cache
from accounts.models import Role, RolePermission


def get_user_app_permissions(user, app_code='ACOES_PNGI', cache_timeout=900):
    """
    Obtém permissões do usuário com cache.
    
    Args:
        user: Instância do usuário
        app_code: Código da aplicação (padrão: 'ACOES_PNGI')
        cache_timeout: Tempo de cache em segundos (padrão: 15 minutos)
    
    Returns:
        set: Conjunto de codenames de permissões
    """
    if not user or not user.is_authenticated:
        return set()
    
    cache_key = f'user_permissions_{user.id}'
    cached = cache.get(cache_key)
    
    if cached is not None:
        return cached
    
    # Obter role do usuário através de idperfil
    if not hasattr(user, 'idperfil') or not user.idperfil:
        cache.set(cache_key, set(), cache_timeout)
        return set()
    
    # Filtrar apenas permissões da aplicação específica
    perms = set()
    role = user.idperfil
    
    # Verificar se o role pertence à aplicação correta
    if role.idaplicacao and role.idaplicacao.codigointerno == app_code:
        perms = set(RolePermission.objects.filter(
            idperfil=role
        ).values_list('permission__codename', flat=True))
    
    cache.set(cache_key, perms, cache_timeout)
    return perms


# Alias para compatibilidade
get_user_permissions_cached = get_user_app_permissions


def clear_user_permissions_cache(user, app_code='ACOES_PNGI'):
    """
    Limpa o cache de permissões de um usuário.
    
    Usar quando:
    - Role do usuário for alterado
    - Permissões do role forem modificadas
    
    Args:
        user: Instância do usuário
        app_code: Código da aplicação
    """
    cache_key = f'user_permissions_{user.id}'
    cache.delete(cache_key)
    
    # Também limpar cache do context processor se existir
    if hasattr(user, 'idperfil') and user.idperfil:
        cache_key_cp = f'acoes_perms_{user.id}_{user.idperfil.id}'
        cache.delete(cache_key_cp)


def require_app_permission(permission_codename, app_code='ACOES_PNGI', raise_exception=True):
    """
    Decorator para proteger views que requerem permissões específicas.
    
    Uso:
        @require_app_permission('add_eixo')
        def create_eixo(request):
            # ...
        
        @require_app_permission('change_eixo', raise_exception=False)
        def edit_eixo(request, pk):
            # Redireciona para dashboard se não tiver permissão
            # ...
    
    Args:
        permission_codename: Codename da permissão requerida
        app_code: Código da aplicação
        raise_exception: Se True, lança PermissionDenied. Se False, redireciona.
    
    Returns:
        function: Decorator
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if raise_exception:
                    raise PermissionDenied("Você precisa estar autenticado.")
                messages.error(request, "Você precisa estar autenticado.")
                return redirect('login')
            
            perms = get_user_app_permissions(request.user, app_code)
            if permission_codename not in perms:
                if raise_exception:
                    raise PermissionDenied(
                        f"Você não tem permissão '{permission_codename}' no {app_code}."
                    )
                messages.error(
                    request,
                    f"Você não tem permissão para realizar esta ação."
                )
                return redirect('portal:dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_any_permission(*permission_codenames, app_code='ACOES_PNGI', raise_exception=True):
    """
    Decorator que requer QUALQUER uma das permissões listadas.
    
    Uso:
        @require_any_permission('add_eixo', 'change_eixo', 'delete_eixo')
        def manage_eixo(request):
            # ...
    
    Args:
        *permission_codenames: Lista de codenames de permissões
        app_code: Código da aplicação
        raise_exception: Se True, lança PermissionDenied. Se False, redireciona.
    
    Returns:
        function: Decorator
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if raise_exception:
                    raise PermissionDenied("Você precisa estar autenticado.")
                messages.error(request, "Você precisa estar autenticado.")
                return redirect('login')
            
            perms = get_user_app_permissions(request.user, app_code)
            has_permission = any(perm in perms for perm in permission_codenames)
            
            if not has_permission:
                if raise_exception:
                    raise PermissionDenied(
                        f"Você precisa de pelo menos uma destas permissões: {', '.join(permission_codenames)}"
                    )
                messages.error(
                    request,
                    "Você não tem permissão para realizar esta ação."
                )
                return redirect('portal:dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_all_permissions(*permission_codenames, app_code='ACOES_PNGI', raise_exception=True):
    """
    Decorator que requer TODAS as permissões listadas.
    
    Uso:
        @require_all_permissions('view_eixo', 'change_eixo')
        def edit_eixo(request, pk):
            # ...
    
    Args:
        *permission_codenames: Lista de codenames de permissões
        app_code: Código da aplicação
        raise_exception: Se True, lança PermissionDenied. Se False, redireciona.
    
    Returns:
        function: Decorator
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if raise_exception:
                    raise PermissionDenied("Você precisa estar autenticado.")
                messages.error(request, "Você precisa estar autenticado.")
                return redirect('login')
            
            perms = get_user_app_permissions(request.user, app_code)
            missing_perms = [
                perm for perm in permission_codenames
                if perm not in perms
            ]
            
            if missing_perms:
                if raise_exception:
                    raise PermissionDenied(
                        f"Faltam permissões: {', '.join(missing_perms)}"
                    )
                messages.error(
                    request,
                    "Você não tem todas as permissões necessárias."
                )
                return redirect('portal:dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def user_can_manage_model(user, model_name, app_code='ACOES_PNGI'):
    """
    Verifica se usuário pode gerenciar um modelo (add OU change).
    
    Uso em views:
        if user_can_manage_model(request.user, 'eixo'):
            # Permitir acesso
        else:
            # Negar acesso
    
    Args:
        user: Instância do usuário
        model_name: Nome do modelo
        app_code: Código da aplicação
    
    Returns:
        bool: True se pode adicionar OU editar
    """
    perms = get_user_app_permissions(user, app_code)
    return (
        f'add_{model_name}' in perms or
        f'change_{model_name}' in perms
    )


def get_model_permissions(user, model_name, app_code='ACOES_PNGI'):
    """
    Obtém todas as permissões de um modelo para um usuário.
    
    Uso:
        perms = get_model_permissions(request.user, 'eixo')
        if perms['can_add']:
            # ...
    
    Args:
        user: Instância do usuário
        model_name: Nome do modelo
        app_code: Código da aplicação
    
    Returns:
        dict: Dicionário com flags de permissão
    """
    perms = get_user_app_permissions(user, app_code)
    return {
        'can_add': f'add_{model_name}' in perms,
        'can_change': f'change_{model_name}' in perms,
        'can_delete': f'delete_{model_name}' in perms,
        'can_view': f'view_{model_name}' in perms,
        'can_manage': user_can_manage_model(user, model_name, app_code),
    }
