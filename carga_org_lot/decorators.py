"""
decorators.py - carga_org_lot
Replicação exata do padrão acoes_pngi/decorators.py
Perfis: GESTOR_CARGA (id=2), COORDENADOR_CARGA (id=20)
"""

from functools import wraps

from django.contrib.auth import get_user_model
from django.http import JsonResponse

from accounts.models import Aplicacao, UserRole

User = get_user_model()


def get_aplicacao_carga_org_lot():
    """Retorna Aplicacao CARGA_ORG_LOT"""
    return Aplicacao.objects.get(codigointerno="CARGA_ORG_LOT")


def user_has_gestor_carga(user):
    """Verifica GESTOR_CARGA ativo"""
    aplicacao = get_aplicacao_carga_org_lot()
    return UserRole.objects.filter(
        user=user, aplicacao=aplicacao, role__codigoperfil="GESTOR_CARGA"
    ).exists()


def user_has_coordenador_carga(user):
    """Verifica GESTOR ou COORDENADOR"""
    aplicacao = get_aplicacao_carga_org_lot()
    return UserRole.objects.filter(
        user=user,
        aplicacao=aplicacao,
        role__codigoperfil__in=["GESTOR_CARGA", "COORDENADOR_CARGA"],
    ).exists()


def gestor_carga_required(view_func):
    """
    Decorator: LOOKUP TABLES (W/D) - APENAS GESTOR_CARGA
    tblstatusprogresso, tbltipocarga, tblstatustokenenviocarga, tblstatuscarga
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not user_has_gestor_carga(request.user):
            return JsonResponse(
                {
                    "success": False,
                    "message": "Acesso negado. Perfil GESTOR_CARGA requerido.",
                    "permissao_requerida": "GESTOR_CARGA",
                    "tabelas": [
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


def operacional_carga_required(view_func):
    """
    Decorator: OPERAÇÕES - GESTOR_CARGA + COORDENADOR_CARGA
    tblpatriarca, tblorganograma*, tbllotacao*, tblcargapatriarca*, etc.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not user_has_coordenador_carga(request.user):
            return JsonResponse(
                {
                    "success": False,
                    "message": "Acesso negado. Perfil GESTOR_CARGA ou COORDENADOR_CARGA requerido.",
                    "permissao_requerida": "GESTOR_CARGA|COORDENADOR_CARGA",
                    "tabelas": [
                        "tblpatriarca",
                        "tblorganogram*",
                        "tbllotacao*",
                        "tbltokenenviocarga",
                        "tblcargapatriarca*",
                    ],
                },
                status=403,
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def consulta_carga_required(view_func):
    """
    Decorator: CONSULTA - Qualquer role CARGA_ORG_LOT
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        aplicacao = get_aplicacao_carga_org_lot()
        if not UserRole.objects.filter(user=request.user, aplicacao=aplicacao).exists():
            return JsonResponse(
                {
                    "success": False,
                    "message": "Acesso negado. Usuário sem permissão na aplicação CARGA_ORG_LOT.",
                    "aplicacao_requerida": "CARGA_ORG_LOT",
                },
                status=403,
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view
