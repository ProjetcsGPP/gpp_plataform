"""
API Views do Carga Org/Lot.
Usa AppContextMiddleware para detecção automática da aplicação.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def api_carga_org_lot_dashboard(request):
    """
    Dashboard API com estatísticas.
    
    ✨ Usa request.app_context automaticamente.
    
    GET /api/v1/carga/
    """
    from ..models import Patriarca
    from accounts.models import UserRole
    
    # ✨ Verifica acesso usando app_context
    app_code = request.app_context.get('code')
    
    if not app_code:
        return Response(
            {'detail': 'Aplicação não identificada'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Verifica se usuário tem acesso
    has_access = UserRole.objects.filter(
        user=request.user,
        aplicacao__codigointerno=app_code
    ).exists()
    
    if not has_access:
        return Response(
            {'detail': 'Acesso negado'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Estatísticas
    stats = {
        'total_patriarcas': Patriarca.objects.count(),
        'patriarcas_ativos': Patriarca.objects.filter(
            idstatusprogresso__in=[1, 2, 3, 4, 5]
        ).count(),
        'cargas_finalizadas': Patriarca.objects.filter(
            idstatusprogresso=6
        ).count(),
        'app': {
            'code': request.app_context['code'],
            'name': request.app_context['name']
        }
    }
    
    return Response(stats)


@api_view(['POST'])
def api_carga_org_lot_upload(request):
    """
    Upload de arquivo de organograma ou lotação.
    
    POST /api/v1/carga/upload/
    """
    from accounts.models import Attribute
    
    # ✨ Verifica atributo usando app_context
    app_code = request.app_context.get('code')
    
    # Verifica se pode fazer upload
    can_upload = Attribute.objects.filter(
        user=request.user,
        aplicacao__codigointerno=app_code,
        key='can_upload',
        value='true'
    ).exists()
    
    if not can_upload:
        return Response(
            {'detail': 'Você não tem permissão para fazer upload'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Processar upload...
    # TODO: Implementar lógica de upload
    
    return Response({
        'message': 'Upload em desenvolvimento',
        'app': request.app_context['code']
    })
