from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.api_carga_org_lot_dashboard, name='api_carga_org_lot_dashboard'),
    path('upload', api_views.api_carga_org_lot_upload, name='api_carga_org_lot_upload'),
]