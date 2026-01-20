from django.urls import path
from ..views.web_views import web_views

app_name = 'acoes_pngi'

urlpatterns = [
    path('', web_views.acoes_pngi_login, name='home'),
    path('login/', web_views.acoes_pngi_login, name='login'),
    path('dashboard/', web_views.acoes_pngi_dashboard, name='dashboard'),
    path('logout/', web_views.acoes_pngi_logout, name='logout'),
]