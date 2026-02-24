from django.urls import path

from accounts.views.web_views import (
    WebLoginView, WebValidateTokenView, WebUserManagementView
)

from accounts.views.api_views import (  # ✅ IMPORTS DIRETOS
    LoginView, ValidateTokenView, UserManagementView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', WebLoginView.as_view(), name='login'),
    path('validate/', WebValidateTokenView.as_view(), name='validate'),
    path('gestao/usuarios/', WebUserManagementView.as_view(), name='usuarios'),
]

api_urlpatterns = [
    path('api/auth/login/', LoginView.as_view()),           # ✅ .as_view()
    path('api/auth/validate/', ValidateTokenView.as_view()),
    path('api/gestao/usuarios/', UserManagementView.as_view()),
]