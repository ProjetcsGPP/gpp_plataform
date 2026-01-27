"""
Views de Dashboard para Carga Org/Lot
"""

from django.shortcuts import render
from django.db.models import Count

from accounts.models import UserRole, Aplicacao
from ...models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblLotacao,
    TblCargaPatriarca,
)
from .auth_views import carga_org_lot_required


@carga_org_lot_required
def carga_dashboard(request):
    """
    GET /carga_org_lot/
    
    Dashboard principal com estatísticas gerais.
    """
    user = request.user
    
    # Buscar role do usuário
    app_carga = Aplicacao.objects.get(codigointerno='CARGA_ORG_LOT')
    user_role = UserRole.objects.filter(
        user=user,
        aplicacao=app_carga
    ).select_related('role').first()
    
    # Estatísticas gerais
    stats = {
        'patriarcas': {
            'total': TblPatriarca.objects.count(),
            'por_status': TblPatriarca.objects.values(
                'id_status_progresso__str_descricao'
            ).annotate(count=Count('id_patriarca'))
        },
        'organogramas': {
            'total': TblOrganogramaVersao.objects.count(),
            'ativos': TblOrganogramaVersao.objects.filter(flg_ativo=True).count(),
        },
        'lotacoes': {
            'total': TblLotacao.objects.count(),
            'validas': TblLotacao.objects.filter(flg_valido=True).count(),
            'invalidas': TblLotacao.objects.filter(flg_valido=False).count(),
        },
        'cargas_recentes': TblCargaPatriarca.objects.select_related(
            'id_patriarca',
            'id_tipo_carga',
            'id_status_carga'
        ).order_by('-dat_data_hora_inicio')[:10]
    }
    
    context = {
        'user': user,
        'role': user_role.role,
        'aplicacao': app_carga,
        'stats': stats,
    }
    
    return render(request, 'carga_org_lot/dashboard.html', context)
