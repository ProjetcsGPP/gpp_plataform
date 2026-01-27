"""
Views AJAX para Carga Org/Lot
"""

from django.http import JsonResponse
from django.db.models import Q

from ...models import TblOrgaoUnidade
from .auth_views import carga_org_lot_required


@carga_org_lot_required
def search_orgao_ajax(request):
    """
    GET /carga_org_lot/ajax/search/orgao/?q=termo&patriarca_id=1
    
    Busca órgãos por sigla ou nome (para autocomplete).
    """
    query = request.GET.get('q', '')
    patriarca_id = request.GET.get('patriarca_id', None)
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
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
    
    return JsonResponse({'results': results})
