"""
Helpers de permissões para carga_org_lot.
Inclui cache automático para otimização de performance.
"""

import logging
import functools
from django.core.cache import cache
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import status
from accounts.models import UserRole
from django.contrib.auth.models import Group
from accounts.services.authorization_service import get_authorization_service



logger = logging.getLogger(__name__)

# Constantes
APP_CODE = 'CARGA_ORG_LOT'
CACHE_TIMEOUT = 900  # 15 minutos


def get_user_app_permissions(user, app_code=APP_CODE):
    """
    Retorna conjunto de permissões do usuário para a aplicação.
    
    ✨ Usa cache automático (15 minutos) para performance.
    
    Args:
        user: User object
        app_code: Código da aplicação (default: CARGA_ORG_LOT)
    
    Returns:
        set: Conjunto de codenames de permissões (ex: {'add_patriarca', 'view_patriarca'})
    
    Example:
        >>> perms = get_user_app_permissions(request.user)
        >>> if 'add_patriarca' in perms:
        >>>     # Usuário pode criar patriarcas
    """
    if not user or not user.is_authenticated:
        return set()
    
    # Superusuário tem todas as permissões
    if user.is_superuser:
        # Retorna todas as permissões da app
        content_types = ContentType.objects.filter(app_label='carga_org_lot')
        all_perms = Permission.objects.filter(content_type__in=content_types)
        return set(all_perms.values_list('codename', flat=True))
    
    # Chave de cache
    cache_key = f'user_perms_{user.id}_{app_code}'
    
    # Tenta buscar do cache
    cached_perms = cache.get(cache_key)
    if cached_perms is not None:
        logger.debug(f"Permissões carregadas do cache para {user.email}")
        return cached_perms
    
    # Busca do banco de dados
    try:
        # Busca roles do usuário na aplicação
        user_roles = UserRole.objects.filter(
            user=user,
            aplicacao__codigointerno=app_code
        ).values_list('role_id', flat=True)
        
        if not user_roles:
            logger.warning(f"Usuário {user.email} sem roles em {app_code}")
            cache.set(cache_key, set(), CACHE_TIMEOUT)
            return set()
        
        # Busca permissões das roles
        auth = get_authorization_service()
        permissions = auth.get_user_permissions(user.id, {app_code})
        
        perms_set = set(permissions)
        
        # Salva no cache
        cache.set(cache_key, perms_set, CACHE_TIMEOUT)
        logger.debug(f"Permissões carregadas do BD para {user.email}: {len(perms_set)} permissões")
        
        return perms_set
    
    except Exception as e:
        logger.error(f"Erro ao buscar permissões de {user.email}: {str(e)}")
        return set()


def get_model_permissions(user, model_name, app_code=APP_CODE):
    """
    Retorna permissões do usuário para um modelo específico.
    
    Args:
        user: User object
        model_name: Nome do modelo em lowercase (ex: 'patriarca')
        app_code: Código da aplicação
    
    Returns:
        dict: Dicionário com permissões por operação
    
    Example:
        >>> perms = get_model_permissions(request.user, 'patriarca')
        >>> perms
        {'can_add': True, 'can_change': True, 'can_delete': False, 'can_view': True}
    """
    all_perms = get_user_app_permissions(user, app_code)
    
    return {
        'can_add': f'add_{model_name}' in all_perms,
        'can_change': f'change_{model_name}' in all_perms,
        'can_delete': f'delete_{model_name}' in all_perms,
        'can_view': f'view_{model_name}' in all_perms,
    }


def has_permission(user, permission_codename, app_code=APP_CODE):
    """
    Verifica se usuário tem uma permissão específica.
    
    Args:
        user: User object
        permission_codename: Codename da permissão (ex: 'add_patriarca')
        app_code: Código da aplicação
    
    Returns:
        bool: True se tem permissão, False caso contrário
    
    Example:
        >>> if has_permission(request.user, 'add_patriarca'):
        >>>     # Usuário pode criar patriarcas
    """
    perms = get_user_app_permissions(user, app_code)
    return permission_codename in perms


def require_api_permission(permission_codename):
    """
    Decorator para endpoints de API que requerem permissão específica.
    
    Args:
        permission_codename: Codename da permissão (ex: 'add_patriarca')
    
    Example:
        >>> @action(detail=False, methods=['post'])
        >>> @require_api_permission('add_patriarca')
        >>> def criar_patriarca(self, request):
        >>>     # Lógica aqui
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if not has_permission(request.user, permission_codename):
                return Response(
                    {
                        'detail': f'Você não tem permissão para esta operação',
                        'required_permission': permission_codename
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def clear_user_permissions_cache(user, app_code=APP_CODE):
    """
    Limpa cache de permissões do usuário.
    
    Use quando permissões do usuário forem alteradas.
    
    Args:
        user: User object
        app_code: Código da aplicação
    """
    cache_key = f'user_perms_{user.id}_{app_code}'
    cache.delete(cache_key)
    logger.info(f"Cache de permissões limpo para {user.email}")


def get_user_role(user, app_code=APP_CODE):
    """
    Retorna role do usuário na aplicação.
    
    Args:
        user: User object
        app_code: Código da aplicação
    
    Returns:
        str or None: Código do perfil (ex: 'GESTOR_CARGA') ou None
    """
    try:
        user_role = UserRole.objects.filter(
            user=user,
            aplicacao__codigointerno=app_code
        ).select_related('role').first()
        
        if user_role:
            return user_role.role.codigoperfil
        return None
    
    except Exception as e:
        logger.error(f"Erro ao buscar role de {user.email}: {str(e)}")
        return None


def is_gestor(user, app_code=APP_CODE):
    """
    Verifica se usuário é Gestor.
    
    Args:
        user: User object
        app_code: Código da aplicação
    
    Returns:
        bool: True se é gestor
    """
    role = get_user_role(user, app_code)
    return role == 'GESTOR_CARGA'


def is_coordenador_or_above(user, app_code=APP_CODE):
    """
    Verifica se usuário é Coordenador ou Gestor.
    
    Args:
        user: User object
        app_code: Código da aplicação
    
    Returns:
        bool: True se é coordenador ou gestor
    """
    role = get_user_role(user, app_code)
    return role in ['GESTOR_CARGA', 'COORDENADOR_CARGA']


def is_analista_or_above(user, app_code=APP_CODE):
    """
    Verifica se usuário é Analista, Coordenador ou Gestor.
    
    Args:
        user: User object
        app_code: Código da aplicação
    
    Returns:
        bool: True se tem permissão de analista ou superior
    """
    role = get_user_role(user, app_code)
    return role in ['GESTOR_CARGA', 'COORDENADOR_CARGA', 'ANALISTA_CARGA']
