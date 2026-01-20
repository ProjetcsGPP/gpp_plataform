"""
URLs das APIs REST do Portal
Prefixo aplicado em gpp_platform/urls.py: /api/v1/portal/
"""

from django.urls import path
from ..views.api_views import rest_list_applications, rest_check_app_access, rest_get_application

urlpatterns = [
    path('applications/', rest_list_applications, name='rest_portal_apps'),
    path('applications/<str:codigo>/', rest_get_application, name='rest_portal_app_detail'),
    path('applications/<str:codigo>/access/', rest_check_app_access, name='rest_portal_app_access'),
]