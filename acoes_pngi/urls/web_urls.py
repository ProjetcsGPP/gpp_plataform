from django.urls import path
from ..views.web_views import acoes_pngi_login, acoes_pngi_dashboard, acoes_pngi_logout

app_name = 'acoes_pngi_web'  # ← MUDOU: namespace específico para Web

urlpatterns = [
    path('', acoes_pngi_login, name='home'),
    path('login/', acoes_pngi_login, name='login'),
    path('dashboard/', acoes_pngi_dashboard, name='dashboard'),
    path('logout/', acoes_pngi_logout, name='logout'),
]
