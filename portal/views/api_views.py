"""
APIs REST para o Portal
Prefixo: /api/v1/portal/
"""


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response  # ← ADICIONADO
from accounts.models import Aplicacao, UserRole


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rest_list_applications(request):
    """
    GET /api/v1/portal/applications/
    
    Lista todas as aplicações que o usuário logado pode acessar.
    Response: [{ "id": ..., "codigo": "...", "nome": "...", "url": "...", "showInPortal": bool }, ...]
    """
    user = request.user  # ← DRF já garante que é autenticado
    
    # Busca aplicações através dos UserRoles
    user_roles = UserRole.objects.filter(user=user).select_related('aplicacao')
    
    # Remove duplicatas de aplicações
    apps_dict = {}
    for ur in user_roles:
        app = ur.aplicacao
        if app.idaplicacao not in apps_dict:
            apps_dict[app.idaplicacao] = {
                'id': app.idaplicacao,
                'codigo': app.codigointerno,
                'nome': app.nomeaplicacao,
                'url': app.base_url or '',
                'showInPortal': app.isshowinportal,
            }
    
    # Retorna apenas apps que devem aparecer no portal
    data = [app for app in apps_dict.values() if app['showInPortal']]
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rest_check_app_access(request, codigo):
    """
    GET /api/v1/portal/applications/<codigo>/access/
    
    Verifica se o usuário tem acesso à aplicação específica.
    Response: { "application": {...}, "hasAccess": bool }
    """
    user = request.user
    
    try:
        app = Aplicacao.objects.get(codigointerno=codigo)
    except Aplicacao.DoesNotExist:
        return Response(
            {'detail': 'Aplicação não encontrada.'},
            status=404
        )
    
    # Verifica se usuário tem role nessa aplicação
    has_access = UserRole.objects.filter(user=user, aplicacao=app).exists()
    
    return Response({
        'application': {
            'id': app.idaplicacao,
            'codigo': app.codigointerno,
            'nome': app.nomeaplicacao,
            'url': app.base_url or '',
            'showInPortal': app.isshowinportal,
        },
        'hasAccess': has_access,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rest_get_application(request, codigo):
    """
    GET /api/v1/portal/applications/<codigo>/
    
    Retorna detalhes de uma aplicação específica (sem verificar acesso).
    Response: { "id": ..., "codigo": "...", "nome": "...", "url": "...", "showInPortal": bool }
    """
    try:
        app = Aplicacao.objects.get(codigointerno=codigo)
    except Aplicacao.DoesNotExist:
        return Response(
            {'detail': 'Aplicação não encontrada.'},
            status=404
        )
    
    return Response({
        'id': app.idaplicacao,
        'codigo': app.codigointerno,
        'nome': app.nomeaplicacao,
        'url': app.base_url or '',
        'showInPortal': app.isshowinportal,
    })
