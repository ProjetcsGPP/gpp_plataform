# accounts/services/authorization_service.py

from django.core.cache import cache
from django.contrib.auth.models import Permission
from typing import Optional, Set, Dict
import logging

from accounts.models import User, Role, UserRole, RolePermission, Aplicacao
from acoes_pngi.permissions import IsAnyPNGIRole

logger = logging.getLogger(__name__)


class AuthorizationService:
    """
    Serviço central de autorização RBAC/ABAC.
    
    Valida permissões sem depender de request/sessão.
    Compatível com Web Views e DRF APIViews.
    """
    
    # Cache TTL: 5 minutos
    CACHE_TTL = 300
    
    # Role máxima com todas as permissões
    PORTAL_ADMIN_CODE = 'PORTAL_ADMIN'
    
    def __init__(self):
        self.cache_prefix = 'authz'
    
    def can(
        self,
        user_id: int,
        app_code: str,
        active_role_id: int,
        action: str,
        model_name: str
    ) -> bool:
        """
        Verifica se usuário tem permissão para executar ação em modelo.
        
        Args:
            user_id: ID do usuário
            app_code: Código da aplicação (ex: 'ACOES_PNGI')
            active_role_id: ID da role ativa
            action: Ação desejada ('view', 'add', 'change', 'delete')
            model_name: Nome do modelo (ex: 'eixo', 'acoes')
        
        Returns:
            bool: True se autorizado, False caso contrário
        
        Exemplo:
            >>> auth = AuthorizationService()
            >>> auth.can(5, 'ACOES_PNGI', 3, 'change', 'eixo')
            True
        """
        try:
            # 1. Validar se role pertence ao usuário e à aplicação
            if not self._validate_user_role(user_id, app_code, active_role_id):
                logger.warning(
                    f"Role {active_role_id} inválida para user={user_id}, app={app_code}"
                )
                return False
            
            # 2. Verificar se é PORTAL_ADMIN
            if self._is_portal_admin(active_role_id):
                logger.debug(f"User {user_id} é PORTAL_ADMIN - autorizado")
                return True
            
            # 3. Buscar permissões da role (com cache)
            permissions = self._get_role_permissions(active_role_id)
            
            # 4. Montar codename da permissão Django
            permission_codename = f"{action}_{model_name.lower()}"
            
            # 5. Verificar se permissão existe
            has_permission = permission_codename in permissions
            
            logger.info(
                f"Authorization check: user={user_id}, role={active_role_id}, "
                f"permission={permission_codename}, result={has_permission}"
            )
            
            return has_permission
        
        except Exception as e:
            logger.error(f"Erro na verificação de autorização: {str(e)}", exc_info=True)
            return False
    
    def _validate_user_role(
        self,
        user_id: int,
        app_code: str,
        role_id: int
    ) -> bool:
        """Valida se role pertence ao usuário na aplicação."""
        cache_key = f"{self.cache_prefix}:user_role:{user_id}:{app_code}:{role_id}"
        
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        
        exists = UserRole.objects.filter(
            user_id=user_id,
            role_id=role_id,
            aplicacao__codigointerno=app_code
        ).exists()
        
        cache.set(cache_key, exists, self.CACHE_TTL)
        return exists
    
    def _is_portal_admin(self, role_id: int) -> bool:
        """Verifica se role é PORTAL_ADMIN."""
        cache_key = f"{self.cache_prefix}:is_admin:{role_id}"
        
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        
        is_admin = Role.objects.filter(
            id=role_id,
            codigoperfil=self.PORTAL_ADMIN_CODE
        ).exists()
        
        cache.set(cache_key, is_admin, self.CACHE_TTL)
        return is_admin
    
    def _get_role_permissions(self, role_id: int) -> Set[str]:
        """
        Busca todas as permissões da role (com cache).
        
        Returns:
            Set com codenames das permissões
        """
        cache_key = f"{self.cache_prefix}:perms:{role_id}"
        
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        
        permission_ids = RolePermission.objects.filter(
            role_id=role_id
        ).values_list('permission_id', flat=True)
        
        codenames = set(
            Permission.objects.filter(
                id__in=permission_ids
            ).values_list('codename', flat=True)
        )
        
        cache.set(cache_key, codenames, self.CACHE_TTL)
        return codenames
    
    def get_user_permissions_in_app(
        self,
        user_id: int,
        app_code: str,
        role_id: int
    ) -> Dict[str, Set[str]]:
        """
        Retorna todas as permissões do usuário agrupadas por modelo.
        
        Returns:
            Dict[modelo, Set[ações]]
            
        Exemplo:
            {
                'eixo': {'view', 'add', 'change'},
                'acoes': {'view'},
                'situacaoacao': {'view'}
            }
        """
        if not self._validate_user_role(user_id, app_code, role_id):
            return {}
        
        if self._is_portal_admin(role_id):
            # Retornar todas as permissões
            return self._get_all_permissions()
        
        permissions = self._get_role_permissions(role_id)
        
        # Agrupar por modelo
        grouped = {}
        for perm in permissions:
            parts = perm.split('_', 1)
            if len(parts) == 2:
                action, model = parts
                if model not in grouped:
                    grouped[model] = set()
                grouped[model].add(action)
        
        return grouped
    
    def _get_all_permissions(self) -> Dict[str, Set[str]]:
        """Retorna todas as permissões do sistema (para PORTAL_ADMIN)."""
        cache_key = f"{self.cache_prefix}:all_perms"
        
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        
        all_perms = Permission.objects.all().values_list('codename', flat=True)
        
        grouped = {}
        for perm in all_perms:
            parts = perm.split('_', 1)
            if len(parts) == 2:
                action, model = parts
                if model not in grouped:
                    grouped[model] = set()
                grouped[model].add(action)
        
        cache.set(cache_key, grouped, self.CACHE_TTL * 2)  # 10 min
        return grouped
    
    def invalidate_cache(self, user_id: Optional[int] = None, role_id: Optional[int] = None):
        """
        Invalida cache de permissões.
        
        Args:
            user_id: Limpar cache específico do usuário
            role_id: Limpar cache específico da role
        """
        if user_id:
            # Limpar cache do usuário
            pattern = f"{self.cache_prefix}:user_role:{user_id}:*"
            # LocMemCache não suporta wildcard delete, mas Redis sim
            logger.info(f"Cache invalidation requested for user {user_id}")
        
        if role_id:
            cache.delete(f"{self.cache_prefix}:perms:{role_id}")
            cache.delete(f"{self.cache_prefix}:is_admin:{role_id}")
            logger.info(f"Cache invalidated for role {role_id}")


# Singleton
_authorization_service = None

def get_authorization_service() -> AuthorizationService:
    """Factory para AuthorizationService (singleton)."""
    global _authorization_service
    if _authorization_service is None:
        _authorization_service = AuthorizationService()
    return _authorization_service

# ============================================================================
# 🆕 INTEGRAÇÃO COM AuthorizationService (NOVO - 2026-02-25)
# ============================================================================

from rest_framework.permissions import BasePermission
from accounts.services import get_authorization_service  # ← Novo import
import logging

logger = logging.getLogger(__name__)


class HasModelPermission(BasePermission):
    """
    🔑 NOVA: Integra com AuthorizationService (cache + performance).
    
    MANTÉM compatibilidade com classes existentes.
    
    Uso nas views:
        permission_classes = [IsAnyPNGIRole, HasModelPermission]
        permission_model = 'eixo'  # ← Defina na view
        
    Vantagens vs classes atuais:
    - ✅ Cache 5min (sem SQL em cada request)
    - ✅ Suporte PORTAL_ADMIN automático
    - ✅ Reutilizável em qualquer app (ACOES_PNGI, CARGA_ORG_LOT)
    - ✅ 100% compatível com token_payload do middleware
    """
    
    def has_permission(self, request, view):
        # Superusuários sempre autorizados
        if request.user and request.user.is_superuser:
            return True
        
        # Usuário deve estar autenticado com role PNGI (classes existentes)
        if not hasattr(request.user, 'is_authenticated') or not request.user.is_authenticated:
            return False
        
        # Verificar se tem role PNGI (usar classe existente)
        pngi_perm = IsAnyPNGIRole()
        if not pngi_perm.has_permission(request, view):
            return False
        
        # Mapa HTTP → ação Django
        action_map = {
            'GET': 'view', 'HEAD': 'view', 'OPTIONS': 'view',
            'POST': 'add', 'PUT': 'change', 'PATCH': 'change', 'DELETE': 'delete'
        }
        action = action_map.get(request.method, 'view')
        
        # Modelo da view
        model_name = getattr(view, 'permission_model', None)
        if not model_name:
            logger.error(f"View {view.__class__.__name__} sem 'permission_model'")
            return False
        
        # Token payload (middleware JWT)
        token_payload = getattr(request, 'token_payload', {})
        user_id = getattr(request.user, 'id', None)
        app_code = token_payload.get('app_code', 'ACOES_PNGI')
        active_role_id = token_payload.get('active_role_id')
        
        if not all([user_id, active_role_id]):
            logger.warning(f"Dados insuficientes: user_id={user_id}, role_id={active_role_id}")
            return False
        
        # 🆕 AuthorizationService (cache + validações)
        auth_service = get_authorization_service()
        has_perm = auth_service.can(
            user_id=user_id,
            app_code=app_code,
            active_role_id=active_role_id,
            action=action,
            model_name=model_name
        )
        
        if not has_perm:
            logger.info(
                f"Permissão negada [AuthorizationService]: user={user_id}, "
                f"role={active_role_id}, action={action}, model={model_name}"
            )
        
        return has_perm


class ReadOnlyOrHasPermission(BasePermission):
    """
    🆕 Leitura para todas as roles PNGI, escrita via AuthorizationService.
    
    Uso: permission_classes = [ReadOnlyOrHasPermission]
         permission_model = 'acoes'
    """
    
    def has_permission(self, request, view):
        # Leitura: usa classes existentes (rápido)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            pngi_perm = IsAnyPNGIRole()
            return pngi_perm.has_permission(request, view)
        
        # Escrita: AuthorizationService + cache
        model_perm = HasModelPermission()
        return model_perm.has_permission(request, view)


# ============================================================================
# ALIAS PARA FACILITAR MIGRAÇÃO GRADUAL
# ============================================================================

class HasAcoesPermissionV2(HasModelPermission):
    """Alias para migração das views existentes."""
    pass

class IsGestorOrCoordenadorV2(HasModelPermission):
    """Alias para classes antigas."""
    pass

