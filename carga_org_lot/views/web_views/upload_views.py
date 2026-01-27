"""
Views de Upload para Carga Org/Lot
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from ...models import TblPatriarca
from .auth_views import carga_org_lot_required


@carga_org_lot_required
def upload_page(request):
    """
    GET /carga_org_lot/upload/
    
    Página de upload de arquivos (organograma e lotação).
    """
    patriarcas = TblPatriarca.objects.filter(
        id_status_progresso__in=[1, 2, 3]  # Apenas patriarcas ativos
    ).order_by('str_sigla_patriarca')
    
    context = {
        'patriarcas': patriarcas,
    }
    
    return render(request, 'carga_org_lot/upload.html', context)


@carga_org_lot_required
@require_http_methods(["POST"])
def upload_organograma_handler(request):
    """
    POST /carga_org_lot/upload/organograma/
    
    Processa upload de arquivo de organograma.
    """
    # TODO: Implementar lógica de processamento
    messages.info(request, 'Processamento de organograma em desenvolvimento.')
    return redirect('carga_org_lot_web:upload')


@carga_org_lot_required
@require_http_methods(["POST"])
def upload_lotacao_handler(request):
    """
    POST /carga_org_lot/upload/lotacao/
    
    Processa upload de arquivo de lotação.
    """
    # TODO: Implementar lógica de processamento
    messages.info(request, 'Processamento de lotação em desenvolvimento.')
    return redirect('carga_org_lot_web:upload')
