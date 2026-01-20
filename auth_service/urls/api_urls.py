"""
URLs consolidadas das APIs REST de autenticação
Prefixo aplicado em gpp_platform/urls.py: /api/v1/auth/
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from ..views.api_views import (
    CustomTokenObtainPairView,
    session_login,
    session_logout,
    session_me,
    get_csrf_token
)

urlpatterns = [
    # JWT Authentication (stateless - recomendado para Next.js)
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Session Authentication (stateful - compatibilidade)
    path('session/login/', session_login, name='session_login'),
    path('session/logout/', session_logout, name='session_logout'),
    path('session/me/', session_me, name='session_me'),
    
    # CSRF Token
    path('csrf/', get_csrf_token, name='csrf_token'),
]