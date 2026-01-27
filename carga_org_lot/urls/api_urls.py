from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import correto das views do dashboard_api.py
from ..views.api_views import (
    dashboard_stats,
    upload_organograma,
    upload_lotacao,
    search_orgao,
)

# Import dos ViewSets
from ..views.api_views import (
    PatriarcaViewSet,
    OrganogramaVersaoViewSet,
    LotacaoVersaoViewSet,
    CargaPatriarcaViewSet,
    LotacaoJsonOrgaoViewSet,
    TokenEnvioCargaViewSet,
    StatusProgressoViewSet,
    StatusCargaViewSet,
    TipoCargaViewSet,
    StatusTokenEnvioCargaViewSet,
)

app_name = 'carga_org_lot_api'

# Router para ViewSets
router = DefaultRouter()
router.register(r'patriarca', PatriarcaViewSet, basename='patriarca')
router.register(r'organograma', OrganogramaVersaoViewSet, basename='organograma')
router.register(r'lotacao', LotacaoVersaoViewSet, basename='lotacao')
router.register(r'carga', CargaPatriarcaViewSet, basename='carga')
router.register(r'lotacao-json', LotacaoJsonOrgaoViewSet, basename='lotacao-json')
router.register(r'token', TokenEnvioCargaViewSet, basename='token')

# ViewSets auxiliares (read-only)
router.register(r'status-progresso', StatusProgressoViewSet, basename='status-progresso')
router.register(r'status-carga', StatusCargaViewSet, basename='status-carga')
router.register(r'tipo-carga', TipoCargaViewSet, basename='tipo-carga')
router.register(r'status-token', StatusTokenEnvioCargaViewSet, basename='status-token')

urlpatterns = [
    # Dashboard e utilitários
    path('dashboard/', dashboard_stats, name='dashboard'),
    path('search/orgao/', search_orgao, name='search-orgao'),
    
    # Uploads
    path('upload/organograma/', upload_organograma, name='upload-organograma'),
    path('upload/lotacao/', upload_lotacao, name='upload-lotacao'),
    
    # ViewSets (REST)
    path('', include(router.urls)),
]
