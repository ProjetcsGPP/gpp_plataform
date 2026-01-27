"""
Views de Organograma para Carga Org/Lot
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse

from ...models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblOrgaoUnidade,
)
from .auth_views import carga_org_lot_required


@carga_org_lot_required
def organograma_list(request):
    """
    GET /carga_org_lot/organogramas/
    
    Lista versões de organogramas.
    """
    patriarca_id = request.GET.get('patriarca', '')
    apenas_ativos = request.GET.get('ativos', '')
    
    organogramas = TblOrganogramaVersao.objects.select_related('id_patriarca').all()
    
    if patriarca_id:
        organogramas = organogramas.filter(id_patriarca_id=patriarca_id)
    
    if apenas_ativos == 'true':
        organogramas = organogramas.filter(flg_ativo=True)
    
    organogramas = organogramas.order_by('-dat_processamento')
    
    # Paginação
    paginator = Paginator(organogramas, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Lista de patriarcas para filtro
    patriarcas = TblPatriarca.objects.all()
    
    context = {
        'page_obj': page_obj,
        'patriarcas': patriarcas,
        'patriarca_id': patriarca_id,
        'apenas_ativos': apenas_ativos,
    }
    
    return render(request, 'carga_org_lot/organograma_list.html', context)


@carga_org_lot_required
def organograma_detail(request, organograma_id):
    """
    GET /carga_org_lot/organogramas/{id}/
    
    Detalhes de uma versão de organograma.
    """
    organograma = get_object_or_404(
        TblOrganogramaVersao.objects.select_related('id_patriarca'),
        id_organograma_versao=organograma_id
    )
    
    # Órgãos raiz (sem pai) para construir hierarquia
    orgaos_raiz = TblOrgaoUnidade.objects.filter(
        id_organograma_versao=organograma,
        id_orgao_unidade_pai__isnull=True
    ).prefetch_related('tblorgaounidade_set')
    
    # Estatísticas
    total_orgaos = TblOrgaoUnidade.objects.filter(
        id_organograma_versao=organograma
    ).count()
    
    context = {
        'organograma': organograma,
        'orgaos_raiz': orgaos_raiz,
        'total_orgaos': total_orgaos,
    }
    
    return render(request, 'carga_org_lot/organograma_detail.html', context)


@carga_org_lot_required
def organograma_hierarquia_json(request, organograma_id):
    """
    GET /carga_org_lot/organogramas/{id}/hierarquia/json/
    
    Retorna hierarquia em formato JSON para visualização em árvore.
    """
    organograma = get_object_or_404(TblOrganogramaVersao, id_organograma_versao=organograma_id)
    
    def build_tree(orgao):
        """Constrói árvore recursivamente"""
        children = TblOrgaoUnidade.objects.filter(id_orgao_unidade_pai=orgao)
        return {
            'id': orgao.id_orgao_unidade,
            'sigla': orgao.str_sigla,
            'nome': orgao.str_nome,
            'nivel': orgao.int_nivel_hierarquia,
            'children': [build_tree(child) for child in children]
        }
    
    # Buscar órgãos raiz
    orgaos_raiz = TblOrgaoUnidade.objects.filter(
        id_organograma_versao=organograma,
        id_orgao_unidade_pai__isnull=True
    )
    
    hierarquia = [build_tree(orgao) for orgao in orgaos_raiz]
    
    return JsonResponse({
        'organograma_id': organograma.id_organograma_versao,
        'patriarca': {
            'id': organograma.id_patriarca.id_patriarca,
            'sigla': organograma.id_patriarca.str_sigla_patriarca,
            'nome': organograma.id_patriarca.str_nome,
        },
        'hierarquia': hierarquia
    })
