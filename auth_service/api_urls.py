# auth_service/api_urls.py
"""
URLs das APIs REST (prefixo /api/auth-rest/)
Importadas em gpp_platform/urls.py
"""
from django.urls import path
from . import api_rest_views

urlpatterns = [
    path('api/auth-rest/login/', api_rest_views.rest_login, name='rest_auth_login'),
    path('api/auth-rest/me/', api_rest_views.rest_me, name='rest_auth_me'),
    path('api/auth-rest/logout/', api_rest_views.rest_logout, name='rest_auth_logout'),
    path('api/auth-rest/csrf-token/', api_rest_views.rest_csrf_token, name='rest_csrf_token'),
]