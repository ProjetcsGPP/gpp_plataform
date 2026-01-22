from django.urls import path
from ..views.api_views import api_carga_org_lot_dashboard, api_carga_org_lot_upload

app_name = 'carga_org_lot_api'  # ← ADICIONE esta linha

urlpatterns = [
    path('', api_carga_org_lot_dashboard, name='dashboard'),
    path('upload/', api_carga_org_lot_upload, name='upload'),  # ← Corrigi também o nome
]
