"""
URLs consolidadas das APIs REST de autenticação
Prefixo recomendado: /api/v1/auth/
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from ..views.api_views import api_views

urlpatterns = [
    # JWT Authentication (stateless - recomendado para Next.js)
    path('token/', api_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Session Authentication (stateful - compatibilidade)
    path('session/login/', api_views.session_login, name='session_login'),
    path('session/logout/', api_views.session_logout, name='session_logout'),
    path('session/me/', api_views.session_me, name='session_me'),
    
    # CSRF Token
    path('csrf/', api_views.get_csrf_token, name='csrf_token'),
]