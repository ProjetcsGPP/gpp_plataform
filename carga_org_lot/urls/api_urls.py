from django.urls import path
from ..views.api_views import api_carga_org_lot_dashboard, api_carga_org_lot_upload

urlpatterns = [
    path('', api_carga_org_lot_dashboard, name='api_carga_org_lot_dashboard'),
    path('upload', api_carga_org_lot_dashboard, name='api_carga_org_lot_upload'),
]