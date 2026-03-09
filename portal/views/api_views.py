# portal/views/api_views.py
"""
APIs REST para o Portal - REFATORADO com AuthorizationService
Prefixo: /api/v1/portal/
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..permissions import CanAccessPortal, CanViewApplication
from ..services.portal_authorization import get_portal_authorization_service


@api_view(["GET"])
@permission_classes([CanAccessPortal])
def rest_list_applications(request):
    """
    GET /api/v1/portal/applications/

    Lista todas as aplicações que o usuário logado pode acessar.
    
    ✅ REFATORADO: Usa PortalAuthorizationService
    ✅ PROTEGIDO: CanAccessPortal valida que usuário tem acesso ao portal
    
    Response: 
        [
            {
                "id": ..., 
                "codigo": "...", 
                "nome": "...", 
                "url": "...", 
                "showInPortal": bool
            }, 
            ...
        ]
    """
    portal_service = get_portal_authorization_service()
    applications = portal_service.get_user_applications(request.user.id)
    
    return Response(applications)


@api_view(["GET"])
@permission_classes([CanViewApplication])
def rest_check_app_access(request, codigo):
    """
    GET /api/v1/portal/applications/<codigo>/access/

    Verifica se o usuário tem acesso à aplicação específica.
    
    ✅ REFATORADO: Usa PortalAuthorizationService
    ✅ PROTEGIDO: CanViewApplication valida acesso à aplicação
    
    Response: 
        {
            "application": {...}, 
            "hasAccess": bool
        }
    """
    portal_service = get_portal_authorization_service()
    
    # Buscar aplicação
    application = portal_service.get_application_by_code(codigo)
    if not application:
        return Response(
            {"detail": "Aplicação não encontrada."}, 
            status=404
        )

    # Validar acesso
    has_access = portal_service.user_can_access_application(
        request.user.id, 
        codigo
    )

    return Response(
        {
            "application": application,
            "hasAccess": has_access,
        }
    )


@api_view(["GET"])
@permission_classes([CanViewApplication])
def rest_get_application(request, codigo):
    """
    GET /api/v1/portal/applications/<codigo>/

    Retorna detalhes de uma aplicação específica.
    
    ✅ REFATORADO: Usa PortalAuthorizationService
    ✅ PROTEGIDO: CanViewApplication valida que usuário pode ver esta aplicação
    🔒 CORRIGIDO: Agora valida permissão antes de retornar dados
    
    Response: 
        {
            "id": ..., 
            "codigo": "...", 
            "nome": "...", 
            "url": "...", 
            "showInPortal": bool
        }
    """
    portal_service = get_portal_authorization_service()
    
    application = portal_service.get_application_by_code(codigo)
    if not application:
        return Response(
            {"detail": "Aplicação não encontrada."}, 
            status=404
        )

    return Response(application)
