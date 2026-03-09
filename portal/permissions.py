# portal/permissions.py
"""
Portal DRF Permissions - Integração com AuthorizationService

Define permissões específicas para endpoints REST do Portal.
"""

import logging

from rest_framework.permissions import BasePermission

from .services.portal_authorization import get_portal_authorization_service

logger = logging.getLogger(__name__)


class CanAccessPortal(BasePermission):
    """
    Permissão básica: usuário autenticado com pelo menos uma aplicação.
    
    Uso:
        permission_classes = [CanAccessPortal]
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superusuários sempre passam
        if request.user.is_superuser:
            return True

        # Verifica se usuário tem acesso a pelo menos uma aplicação
        portal_service = get_portal_authorization_service()
        applications = portal_service.get_user_applications(request.user.id)
        
        has_access = len(applications) > 0
        
        if not has_access:
            logger.warning(
                f"⛔ User {request.user.id} has no applications in portal"
            )
        
        return has_access


class CanViewApplication(BasePermission):
    """
    Permissão: usuário pode visualizar uma aplicação específica.
    
    Requer que a view forneça 'codigo' via kwargs ou query params.
    
    Uso:
        permission_classes = [CanViewApplication]
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superusuários sempre passam
        if request.user.is_superuser:
            return True

        # Extrai código da aplicação
        app_code = view.kwargs.get('codigo') or request.GET.get('codigo')
        
        if not app_code:
            logger.error("❌ Application code not provided in request")
            return False

        # Valida acesso à aplicação
        portal_service = get_portal_authorization_service()
        has_access = portal_service.user_can_access_application(
            request.user.id, 
            app_code
        )
        
        if not has_access:
            logger.warning(
                f"⛔ User {request.user.id} cannot access application "
                f"{app_code}"
            )
        
        return has_access
