"""
Authorization Service para carga_org_lot - RBAC Django
Perfis: GESTOR_CARGA (id=2), COORDENADOR_CARGA (id=20)
"""

from collections.abc import Callable
from functools import wraps

from django.contrib.auth import get_user_model
from django.http import JsonResponse

from accounts.models import Aplicacao, UserRole

User = get_user_model()
APPLICACAO_CODIGO = "CARGA_ORG_LOT"


def get_user_permissions(user) -> dict:
    """Retorna roles do usuário para CARGA_ORG_LOT"""
    try:
        aplicacao = Aplicacao.objects.get(codigointerno=APPLICACAO_CODIGO)
        roles = UserRole.objects.filter(user=user, aplicacao=aplicacao).values_list(
            "role__codigoperfil", flat=True
        )

        return {
            "roles": list(roles),
            "is_gestor": "GESTOR_CARGA" in roles,
            "is_coordenador": "COORDENADOR_CARGA" in roles,
            "is_operacional": "GESTOR_CARGA" in roles or "COORDENADOR_CARGA" in roles,
        }
    except Aplicacao.DoesNotExist:
        return {
            "roles": [],
            "is_gestor": False,
            "is_coordenador": False,
            "is_operacional": False,
        }


def gestor_required(view_func: Callable) -> Callable:
    """Requer GESTOR_CARGA - Lookup Tables (W/D)"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        permissoes = get_user_permissions(request.user)
        if not permissoes["is_gestor"]:
            return JsonResponse(
                {
                    "erro": "Permissão GESTOR_CARGA requerida",
                    "roles_usuario": permissoes["roles"],
                    "tabelas_afetadas": [
                        "tblstatusprogresso",
                        "tbltipocarga",
                        "tblstatustokenenviocarga",
                        "tblstatuscarga",
                    ],
                },
                status=403,
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def operacional_required(view_func: Callable) -> Callable:
    """Requer GESTOR_CARGA ou COORDENADOR_CARGA - Operações Principais"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        permissoes = get_user_permissions(request.user)
        if not permissoes["is_operacional"]:
            return JsonResponse(
                {
                    "erro": "Permissão GESTOR_CARGA ou COORDENADOR_CARGA requerida",
                    "roles_usuario": permissoes["roles"],
                    "tabelas_afetadas": [
                        "tblpatriarca",
                        "tblorganogram*",
                        "tbllotacao*",
                        "tblcargapatriarca*",
                    ],
                },
                status=403,
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def consulta_required(view_func: Callable) -> Callable:
    """Requer qualquer role da aplicação - Somente Leitura"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        permissoes = get_user_permissions(request.user)
        if not permissoes["roles"]:
            return JsonResponse(
                {
                    "erro": "Acesso à aplicação CARGA_ORG_LOT requerido",
                    "roles_usuario": [],
                },
                status=403,
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view
