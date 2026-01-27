"""
Views de Lotação para Carga Org/Lot
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from ...models import (
    TblPatriarca,
    TblLotacaoVersao,
    TblLotacao,
    TblLotacaoInconsistencia,
)
from .auth_views import carga_org_lot_required


@carga_org_lot_required
def lotacao_list(request):
    """
    GET /carga_org_lot/lotacoes/
    
    Lista versões de lotações.
    """
    patriarca_id = request.GET.get('patriarca', '')
    
    lotacoes = TblLotacaoVersao.objects.select_related(
        'id_patriarca',
        'id_organograma_versao'
    ).all()
    
    if patriarca_id:
        lotacoes = lotacoes.filter(id_patriarca_id=patriarca_id)
    
    lotacoes = lotacoes.order_by('-dat_processamento')
    
    # Paginação
    paginator = Paginator(lotacoes, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Lista de patriarcas para filtro
    patriarcas = TblPatriarca.objects.all()
    
    context = {
        'page_obj': page_obj,
        'patriarcas': patriarcas,
        'patriarca_id': patriarca_id,
    }
    
    return render(request, 'carga_org_lot/lotacao_list.html', context)


@carga_org_lot_required
def lotacao_detail(request, lotacao_versao_id):
    """
    GET /carga_org_lot/lotacoes/{id}/
    
    Detalhes de uma versão de lotação.
    """
    lotacao_versao = get_object_or_404(
        TblLotacaoVersao.objects.select_related(
            'id_patriarca',
            'id_organograma_versao'
        ),
        id_lotacao_versao=lotacao_versao_id
    )
    
    # Filtros para registros de lotação
    cpf_search = request.GET.get('cpf', '')
    valido_filter = request.GET.get('valido', '')
    
    # Registros de lotação
    lotacoes = TblLotacao.objects.filter(
        id_lotacao_versao=lotacao_versao
    ).select_related('id_orgao_lotacao', 'id_unidade_lotacao')
    
    if cpf_search:
        lotacoes = lotacoes.filter(str_cpf__icontains=cpf_search)
    
    if valido_filter == 'true':
        lotacoes = lotacoes.filter(flg_valido=True)
    elif valido_filter == 'false':
        lotacoes = lotacoes.filter(flg_valido=False)
    
    # Paginação de lotações
    paginator = Paginator(lotacoes, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    stats = {
        'total': TblLotacao.objects.filter(id_lotacao_versao=lotacao_versao).count(),
        'validos': TblLotacao.objects.filter(
            id_lotacao_versao=lotacao_versao,
            flg_valido=True
        ).count(),
        'invalidos': TblLotacao.objects.filter(
            id_lotacao_versao=lotacao_versao,
            flg_valido=False
        ).count(),
        'inconsistencias': TblLotacaoInconsistencia.objects.filter(
            id_lotacao__id_lotacao_versao=lotacao_versao
        ).count()
    }
    
    context = {
        'lotacao_versao': lotacao_versao,
        'page_obj': page_obj,
        'stats': stats,
        'cpf_search': cpf_search,
        'valido_filter': valido_filter,
    }
    
    return render(request, 'carga_org_lot/lotacao_detail.html', context)


@carga_org_lot_required
def lotacao_inconsistencias(request, lotacao_versao_id):
    """
    GET /carga_org_lot/lotacoes/{id}/inconsistencias/
    
    Lista inconsistências de uma versão de lotação.
    """
    lotacao_versao = get_object_or_404(TblLotacaoVersao, id_lotacao_versao=lotacao_versao_id)
    
    inconsistencias = TblLotacaoInconsistencia.objects.filter(
        id_lotacao__id_lotacao_versao=lotacao_versao
    ).select_related('id_lotacao', 'id_lotacao__id_orgao_lotacao').order_by('-dat_registro')
    
    # Paginação
    paginator = Paginator(inconsistencias, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'lotacao_versao': lotacao_versao,
        'page_obj': page_obj,
    }
    
    return render(request, 'carga_org_lot/lotacao_inconsistencias.html', context)
