"""
Views de Carga para Carga Org/Lot
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from ...models import (
    TblPatriarca,
    TblCargaPatriarca,
    TblDetalheStatusCarga,
    TblTipoCarga,
    TblStatusCarga,
)
from .auth_views import carga_org_lot_required


@carga_org_lot_required
def carga_list(request):
    """
    GET /carga_org_lot/cargas/
    
    Lista todas as cargas com filtros.
    """
    patriarca_id = request.GET.get('patriarca', '')
    tipo_id = request.GET.get('tipo', '')
    status_id = request.GET.get('status', '')
    
    cargas = TblCargaPatriarca.objects.select_related(
        'id_patriarca',
        'id_tipo_carga',
        'id_status_carga',
        'id_token_envio_carga'
    ).all()
    
    if patriarca_id:
        cargas = cargas.filter(id_patriarca_id=patriarca_id)
    
    if tipo_id:
        cargas = cargas.filter(id_tipo_carga_id=tipo_id)
    
    if status_id:
        cargas = cargas.filter(id_status_carga_id=status_id)
    
    cargas = cargas.order_by('-dat_data_hora_inicio')
    
    # Paginação
    paginator = Paginator(cargas, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Listas para filtros
    patriarcas = TblPatriarca.objects.all()
    tipos_carga = TblTipoCarga.objects.all()
    status_carga = TblStatusCarga.objects.all()
    
    context = {
        'page_obj': page_obj,
        'patriarcas': patriarcas,
        'tipos_carga': tipos_carga,
        'status_carga': status_carga,
        'patriarca_id': patriarca_id,
        'tipo_id': tipo_id,
        'status_id': status_id,
    }
    
    return render(request, 'carga_org_lot/carga_list.html', context)


@carga_org_lot_required
def carga_detail(request, carga_id):
    """
    GET /carga_org_lot/cargas/{id}/
    
    Detalhes de uma carga específica com timeline.
    """
    carga = get_object_or_404(
        TblCargaPatriarca.objects.select_related(
            'id_patriarca',
            'id_tipo_carga',
            'id_status_carga',
            'id_token_envio_carga',
            'id_token_envio_carga__id_status_token_envio_carga'
        ),
        id_carga_patriarca=carga_id
    )
    
    # Timeline de status
    timeline = TblDetalheStatusCarga.objects.filter(
        id_carga_patriarca=carga
    ).select_related('id_status_carga').order_by('dat_registro')
    
    context = {
        'carga': carga,
        'timeline': timeline,
    }
    
    return render(request, 'carga_org_lot/carga_detail.html', context)
