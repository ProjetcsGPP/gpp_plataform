"""
API de Dashboard e Utilitários

REFATORADO: Implementa require_api_permission do AuthorizationService
"""

from django.db.models import Count, Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.services.authorization_service import require_api_permission

from ...models import (
    TblCargaPatriarca,
    TblLotacao,
    TblOrganogramaVersao,
    TblOrgaoUnidade,
    TblPatriarca,
)


@api_view(["GET"])
@require_api_permission("view_tblpatriarca", "CARGA_ORG_LOT")
def dashboard_stats(request):
    """
    GET /api/carga_org_lot/dashboard/

    Retorna estatísticas gerais do sistema de carga.

    ✅ PERMISSÃO: view_tblpatriarca
    """
    # Estatísticas gerais
    stats = {
        "patriarcas": {
            "total": TblPatriarca.objects.count(),
            "por_status": list(
                TblPatriarca.objects.values(
                    "id_status_progresso__str_descricao"
                ).annotate(count=Count("id_patriarca"))
            ),
        },
        "organogramas": {
            "total": TblOrganogramaVersao.objects.count(),
            "ativos": TblOrganogramaVersao.objects.filter(flg_ativo=True).count(),
            "processados": TblOrganogramaVersao.objects.filter(
                str_status_processamento="PROCESSADO"
            ).count(),
        },
        "lotacoes": {
            "total": TblLotacao.objects.count(),
            "validas": TblLotacao.objects.filter(flg_valido=True).count(),
            "invalidas": TblLotacao.objects.filter(flg_valido=False).count(),
        },
        "cargas": {
            "total": TblCargaPatriarca.objects.count(),
            "por_status": list(
                TblCargaPatriarca.objects.values(
                    "id_status_carga__str_descricao"
                ).annotate(count=Count("id_carga_patriarca"))
            ),
            "por_tipo": list(
                TblCargaPatriarca.objects.values(
                    "id_tipo_carga__str_descricao"
                ).annotate(count=Count("id_carga_patriarca"))
            ),
        },
    }

    return Response(stats)


@api_view(["GET"])
@require_api_permission("view_tblorgaounidade", "CARGA_ORG_LOT")
def search_orgao(request):
    """
    GET /api/carga_org_lot/search/orgao/?q=termo&patriarca_id=1

    Busca órgãos por sigla ou nome.

    ✅ PERMISSÃO: view_tblorgaounidade
    """
    query = request.query_params.get("q", "")
    patriarca_id = request.query_params.get("patriarca_id", None)

    if len(query) < 2:
        return Response({"results": []})

    orgaos = TblOrgaoUnidade.objects.filter(
        Q(str_sigla__icontains=query) | Q(str_nome__icontains=query), flg_ativo=True
    )

    if patriarca_id:
        orgaos = orgaos.filter(id_patriarca_id=patriarca_id)

    orgaos = orgaos.select_related("id_patriarca")[:20]

    results = [
        {
            "id": o.id_orgao_unidade,
            "sigla": o.str_sigla,
            "nome": o.str_nome,
            "patriarca": o.id_patriarca.str_sigla_patriarca,
            "nivel": o.int_nivel_hierarquia,
        }
        for o in orgaos
    ]

    return Response({"results": results})


@api_view(["POST"])
@require_api_permission("add_tblorganogramaversao", "CARGA_ORG_LOT")
def upload_organograma(request):
    """
    POST /api/carga_org_lot/upload/organograma/

    Faz upload de arquivo de organograma (Excel/CSV).

    Body (multipart/form-data):
        - file: arquivo
        - patriarca_id: ID do patriarca

    ✅ PERMISSÃO: add_tblorganogramaversao
    """
    # TODO: Implementar lógica de upload e processamento

    return Response(
        {"message": "Upload de organograma em desenvolvimento"},
        status=status.HTTP_501_NOT_IMPLEMENTED,
    )


@api_view(["POST"])
@require_api_permission("add_tbllotacaoversao", "CARGA_ORG_LOT")
def upload_lotacao(request):
    """
    POST /api/carga_org_lot/upload/lotacao/

    Faz upload de arquivo de lotação (Excel/CSV).

    Body (multipart/form-data):
        - file: arquivo
        - patriarca_id: ID do patriarca
        - organograma_versao_id: ID da versão do organograma

    ✅ PERMISSÃO: add_tbllotacaoversao
    """
    # TODO: Implementar lógica de upload e processamento

    return Response(
        {"message": "Upload de lotação em desenvolvimento"},
        status=status.HTTP_501_NOT_IMPLEMENTED,
    )
