from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from accounts.models import UserRole, Aplicacao
import json


def check_carga_org_lot_access(user):
    """Verifica se usuário tem acesso ao Carga Org Lot"""
    if not user.is_authenticated:
        return False
    return UserRole.objects.filter(
        user=user,
        aplicacao__codigointerno='CARGA_ORG_LOT'
    ).exists()


@require_http_methods(["GET"])
def api_carga_org_lot_dashboard(request):
    """
    GET /api/carga_org_lot
    Retorna dados do dashboard Carga Org Lot
    """
    if not check_carga_org_lot_access(request.user):
        return JsonResponse({
            'ok': False,
            'message': 'Você não tem permissão para acessar esta aplicação.'
        }, status=403)
    
    user = request.user
    user_role = UserRole.objects.filter(
        user=user,
        aplicacao__codigointerno='CARGA_ORG_LOT'
    ).select_related('role', 'aplicacao').first()
    
    return JsonResponse({
        'ok': True,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        },
        'role': {
            'codigo': user_role.role.codigoperfil,
            'nome': user_role.role.nomeperfil
        },
        'aplicacao': {
            'codigo': user_role.aplicacao.codigointerno,
            'nome': user_role.aplicacao.nomeaplicacao
        },
        'stats': {
            'organogramas_total': 0,  # Implementar quando tiver models
            'lotacoes_total': 0,
            'ultimo_upload': None
        }
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_carga_org_lot_upload(request):
    """
    POST /api/carga_org_lot/upload
    Upload de organograma
    """
    if not check_carga_org_lot_access(request.user):
        return JsonResponse({
            'ok': False,
            'message': 'Você não tem permissão para acessar esta aplicação.'
        }, status=403)
    
    # TODO: Implementar lógica de upload
    return JsonResponse({
        'ok': True,
        'message': 'Upload não implementado ainda.'
    })