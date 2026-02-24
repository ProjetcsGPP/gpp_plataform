# accounts/urls/api_urls.py
from django.urls import path
from ..views.api_views import (
    UserManagementView,
    LoginView,
    RefreshTokenView,
    LogoutView,
    ValidateTokenView,
    ChangeRoleView
)

app_name = 'accounts'

urlpatterns = [
    # ✅ MANTER: Gestão de usuários (original)
    path('gestao/usuarios/', UserManagementView.as_view(), name='user_management'),
    
    # ✨ NOVO: Endpoints de autenticação JWT
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='refresh_token'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/validate/', ValidateTokenView.as_view(), name='validate_token'),
    path('auth/change-role/', ChangeRoleView.as_view(), name='change_role'),
]
