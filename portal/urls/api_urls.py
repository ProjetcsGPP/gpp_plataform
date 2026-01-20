# portal/api_urls.py
"""
URLs das APIs REST do portal (prefixo /api/portal-rest/)
Importadas em gpp_platform/urls.py
"""
from django.urls import path
from ..views.api_views import api_views

urlpatterns = [
    path('api/portal-rest/applications/', api_views.rest_list_applications, name='rest_portal_apps'),
    path('api/portal-rest/applications/<slug:slug>/', api_views.rest_get_application, name='rest_portal_app_detail'),
    path('api/portal-rest/applications/<slug:slug>/access/', api_views.rest_check_app_access, name='rest_portal_app_access'),
]