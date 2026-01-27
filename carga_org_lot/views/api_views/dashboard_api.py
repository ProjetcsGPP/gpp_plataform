"""
API de Dashboard e Utilitários
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q, Count

from accounts.models import UserRole
from ...models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblLotacao,
    TblCargaPatriarca,
    TblOrgaoUnidade,
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    GET /api/carga_org_lot/dashboard/
    
    Retorna estatísticas gerais do sistema de carga.
    """
    app_code = request.app_context.get('code', 'CARGA_ORG_LOT')
    
    # Verifica acesso
    has_access = UserRole.objects.filter(
        user=request.user,
        aplicacao__codigointerno=app_code
    ).exists()
    
    if not has_access:
        return Response(
            {'detail': 'Acesso negado'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Estatísticas gerais
    stats = {
        'patriarcas': {
            'total': TblPatriarca.objects.count(),
            'por_status': list(
                TblPatriarca.objects.values('id_status_progresso__str_descricao')
                .annotate(count=Count('id_patriarca'))
            )
        },
        'organogramas': {
            'total': TblOrganogramaVersao.objects.count(),
            'ativos': TblOrganogramaVersao.objects.filter(flg_ativo=True).count(),
            'processados': TblOrganogramaVersao.objects.filter(
                str_status_processamento='PROCESSADO'
            ).count(),
        },
        'lotacoes': {
            'total': TblLotacao.objects.count(),
            'validas': TblLotacao.objects.filter(flg_valido=True).count(),
            'invalidas': TblLotacao.objects.filter(flg_valido=False).count(),
        },
        'cargas': {
            'total': TblCargaPatriarca.objects.count(),
            'por_status': list(
                TblCargaPatriarca.objects.values('id_status_carga__str_descricao')
                .annotate(count=Count('id_carga_patriarca'))
            ),
            'por_tipo': list(
                TblCargaPatriarca.objects.values('id_tipo_carga__str_descricao')
                .annotate(count=Count('id_carga_patriarca'))
            )
        }
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_orgao(request):
    """
    GET /api/carga_org_lot/search/orgao/?q=termo&patriarca_id=1
    
    Busca órgãos por sigla ou nome.
    """
    query = request.query_params.get('q', '')
    patriarca_id = request.query_params.get('patriarca_id', None)
    
    if len(query) < 2:
        return Response({'results': []})
    
    orgaos = TblOrgaoUnidade.objects.filter(
        Q(str_sigla__icontains=query) | Q(str_nome__icontains=query),
        flg_ativo=True
    )
    
    if patriarca_id:
        orgaos = orgaos.filter(id_patriarca_id=patriarca_id)
    
    orgaos = orgaos.select_related('id_patriarca')[:20]
    
    results = [
        {
            'id': o.id_orgao_unidade,
            'sigla': o.str_sigla,
            'nome': o.str_nome,
            'patriarca': o.id_patriarca.str_sigla_patriarca,
            'nivel': o.int_nivel_hierarquia
        }
        for o in orgaos
    ]
    
    return Response({'results': results})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_organograma(request):
    """
    POST /api/carga_org_lot/upload/organograma/
    
    Faz upload de arquivo de organograma (Excel/CSV).
    
    Body (multipart/form-data):
        - file: arquivo
        - patriarca_id: ID do patriarca
    """
    # TODO: Implementar lógica de upload e processamento
    
    return Response({
        'message': 'Upload de organograma em desenvolvimento'
    }, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_lotacao(request):
    """
    POST /api/carga_org_lot/upload/lotacao/
    
    Faz upload de arquivo de lotação (Excel/CSV).
    
    Body (multipart/form-data):
        - file: arquivo
        - patriarca_id: ID do patriarca
        - organograma_versao_id: ID da versão do organograma
    """
    # TODO: Implementar lógica de upload e processamento
    
    return Response({
        'message': 'Upload de lotação em desenvolvimento'
    }, status=status.HTTP_501_NOT_IMPLEMENTED)
