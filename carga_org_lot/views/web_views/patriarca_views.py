"""
Views de Patriarca para Carga Org/Lot
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from ...models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblLotacaoVersao,
    TblCargaPatriarca,
    TblStatusProgresso,
)
from .auth_views import carga_org_lot_required


@carga_org_lot_required
def patriarca_list(request):
    """
    GET /carga_org_lot/patriarcas/
    
    Lista todos os patriarcas com filtros e paginação.
    """
    # Filtros
    search = request.GET.get('search', '')
    status_id = request.GET.get('status', '')
    
    patriarcas = TblPatriarca.objects.select_related(
        'id_status_progresso',
        'id_usuario_criacao'
    ).all()
    
    # Aplicar filtros
    if search:
        patriarcas = patriarcas.filter(
            Q(str_sigla_patriarca__icontains=search) |
            Q(str_nome__icontains=search)
        )
    
    if status_id:
        patriarcas = patriarcas.filter(id_status_progresso_id=status_id)
    
    # Ordenação
    patriarcas = patriarcas.order_by('-dat_criacao')
    
    # Paginação
    paginator = Paginator(patriarcas, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Lista de status para filtro
    status_list = TblStatusProgresso.objects.all()
    
    context = {
        'page_obj': page_obj,
        'status_list': status_list,
        'search': search,
        'status_id': status_id,
    }
    
    return render(request, 'carga_org_lot/patriarca_list.html', context)


@carga_org_lot_required
def patriarca_detail(request, patriarca_id):
    """
    GET /carga_org_lot/patriarcas/{id}/
    
    Detalhes de um patriarca específico.
    """
    patriarca = get_object_or_404(
        TblPatriarca.objects.select_related(
            'id_status_progresso',
            'id_usuario_criacao'
        ),
        id_patriarca=patriarca_id
    )
    
    # Organogramas do patriarca
    organogramas = TblOrganogramaVersao.objects.filter(
        id_patriarca=patriarca
    ).order_by('-dat_processamento')[:5]
    
    # Versões de lotação
    lotacoes = TblLotacaoVersao.objects.filter(
        id_patriarca=patriarca
    ).order_by('-dat_processamento')[:5]
    
    # Cargas recentes
    cargas = TblCargaPatriarca.objects.filter(
        id_patriarca=patriarca
    ).select_related(
        'id_tipo_carga',
        'id_status_carga'
    ).order_by('-dat_data_hora_inicio')[:10]
    
    context = {
        'patriarca': patriarca,
        'organogramas': organogramas,
        'lotacoes': lotacoes,
        'cargas': cargas,
    }
    
    return render(request, 'carga_org_lot/patriarca_detail.html', context)
