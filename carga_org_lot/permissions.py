"""
Classes de permissão DRF para carga_org_lot.
Verificação automática baseada em Django permissions.
"""

import logging
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .utils.permissions import has_permission, is_coordenador_or_above, APP_CODE


logger = logging.getLogger(__name__)


class HasCargaOrgLotPermission(BasePermission):
    """
    Classe de permissão que verifica automaticamente Django permissions
    baseada na action do ViewSet.
    
    Mapeia actions do ViewSet para permissões Django:
    - list, retrieve: view_<model>
    - create: add_<model>
    - update, partial_update: change_<model>
    - destroy: delete_<model>
    
    Uso:
        class PatriarcaViewSet(viewsets.ModelViewSet):
            permission_classes = [HasCargaOrgLotPermission]
    
    ✨ Usa helpers com cache para performance otimizada.
    """
    
    def has_permission(self, request, view):
        """
        Verifica permissão no nível de view.
        """
        # Não autenticado = sem permissão
        if not request.user or not request.user.is_authenticated:
            logger.warning("Usuário não autenticado tentou acessar API")
            return False
        
        # Superusuário = sempre permitido
        if request.user.is_superuser:
            return True
        
        # Determina permissão requerida baseada na action
        required_perm = self._get_required_permission(view)
        
        if not required_perm:
            # Se não conseguir determinar, nega acesso
            logger.warning(
                f"Não foi possível determinar permissão para action '{view.action}' "
                f"no model '{view.queryset.model.__name__}'"
            )
            return False
        
        # Verifica permissão usando helper com cache
        has_perm = has_permission(request.user, required_perm, APP_CODE)
        
        if not has_perm:
            logger.warning(
                f"Usuário {request.user.email} sem permissão '{required_perm}' "
                f"para action '{view.action}'"
            )
        
        return has_perm
    
    def _get_required_permission(self, view):
        """
        Determina permissão requerida baseada na action do ViewSet.
        
        Args:
            view: ViewSet instance
        
        Returns:
            str: Codename da permissão (ex: 'view_patriarca')
        """
        # Obtém nome do modelo em lowercase
        try:
            model_name = view.queryset.model._meta.model_name
        except:
            return None
        
        # Mapeia action para operação
        action = getattr(view, 'action', None)
        
        if not action:
            return None
        
        # Mapeamento de actions para permissões
        action_permission_map = {
            'list': 'view',
            'retrieve': 'view',
            'create': 'add',
            'update': 'change',
            'partial_update': 'change',
            'destroy': 'delete',
        }
        
        # Actions customizadas geralmente são de leitura (view)
        operation = action_permission_map.get(action, 'view')
        
        # Formato: {operation}_{model_name}
        return f"{operation}_{model_name}"


class IsCoordenadorOrAbove(BasePermission):
    """
    Permite acesso apenas para Coordenadores e Gestores.
    
    Uso:
        @action(detail=True, methods=['post'], permission_classes=[IsCoordenadorOrAbove])
        def ativar_organograma(self, request, pk=None):
            ...
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return is_coordenador_or_above(request.user, APP_CODE)


class IsGestor(BasePermission):
    """
    Permite acesso apenas para Gestores.
    
    Uso:
        @action(detail=True, methods=['delete'], permission_classes=[IsGestor])
        def delete_all_data(self, request, pk=None):
            ...
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        from .utils.permissions import is_gestor
        return is_gestor(request.user, APP_CODE)


class ReadOnly(BasePermission):
    """
    Permite apenas operações de leitura (GET, HEAD, OPTIONS).
    
    Uso:
        permission_classes = [IsAuthenticated, ReadOnly]
    """
    
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


# ============================================
# COMPAT: Mantendo classes antigas para compatibilidade
# ============================================

class CanManageCarga(HasCargaOrgLotPermission):
    """
    Alias para compatibilidade com código antigo.
    Usa a mesma lógica de HasCargaOrgLotPermission.
    """
    pass


class IsCargaOrgLotUser(HasCargaOrgLotPermission):
    """
    Alias para compatibilidade com testes antigos.
    Usa a mesma lógica de HasCargaOrgLotPermission.
    """
    pass
