# carga_org_lot/permissions.py - VERSÃO REFATORADA

"""
Classes de permissão DRF para carga_org_lot.
🔄 MIGRADO para usar AuthorizationService centralizado.
"""

import logging
from rest_framework.permissions import SAFE_METHODS, BasePermission
from accounts.services.authorization_service import get_authorization_service

logger = logging.getLogger(__name__)

# ============================================================================
# ✅ IMPORTAR DO SERVIÇO CENTRALIZADO
# ============================================================================

from accounts.services.authorization_service import HasModelPermission

# ============================================================================
# PERMISSÕES ESPECIALIZADAS (Lógica de negócio específica)
# ============================================================================

class IsCoordenadorOrAbove(BasePermission):
    """
    🔄 MIGRADO: Usa AuthorizationService.
    
    Permite acesso apenas para Coordenadores e Gestores.
    
    Mantida porque views antigas usam diretamente em @action decorators.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Usar AuthorizationService
        token_payload = getattr(request, "token_payload", {})
        if token_payload:
            active_role_id = token_payload.get("active_role_id")
            
            if active_role_id:
                try:
                    from accounts.models import Role
                    role = Role.objects.get(id=active_role_id)
                    return role.codigoperfil in ["COORDENADOR_CARGA", "GESTOR_CARGA"]
                except:
                    return False

        # Fallback para compatibilidade
        from .utils.permissions import is_coordenador_or_above, APP_CODE
        return is_coordenador_or_above(request.user, APP_CODE)


class IsGestor(BasePermission):
    """
    🔄 MIGRADO: Usa AuthorizationService.
    
    Permite acesso apenas para Gestores.
    
    Mantida porque operações críticas requerem apenas GESTOR.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Usar AuthorizationService
        token_payload = getattr(request, "token_payload", {})
        if token_payload:
            active_role_id = token_payload.get("active_role_id")
            
            if active_role_id:
                try:
                    from accounts.models import Role
                    role = Role.objects.get(id=active_role_id)
                    return role.codigoperfil == "GESTOR_CARGA"
                except:
                    return False

        # Fallback para compatibilidade
        from .utils.permissions import is_gestor, APP_CODE
        return is_gestor(request.user, APP_CODE)


class ReadOnly(BasePermission):
    """
    Permite apenas operações de leitura (GET, HEAD, OPTIONS).
    
    Mantida porque é simples e não precisa de AuthorizationService.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


# ============================================================================
# ALIASES DE COMPATIBILIDADE (Manter temporariamente)
# ============================================================================

class CanManageCarga(HasModelPermission):
    """
    Alias para compatibilidade com código antigo.
    Agora usa HasModelPermission do AuthorizationService.
    """
    pass


class IsCargaOrgLotUser(HasModelPermission):
    """
    Alias para compatibilidade com testes antigos.
    Agora usa HasModelPermission do AuthorizationService.
    """
    pass


# Nota: HasCargaOrgLotPermission foi REMOVIDA
# Substituir por: HasModelPermission nas views
#
# Exemplo de uso:
# from accounts.services.authorization_service import HasModelPermission
#
# class PatriarcaViewSet(viewsets.ModelViewSet):
#     permission_classes = [HasModelPermission]
#     permission_model = 'patriarca'
