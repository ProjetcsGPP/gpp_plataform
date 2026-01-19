from django.urls import path
from . import views

app_name = 'acoes_pngi'

urlpatterns = [
    path('', views.acoes_pngi_login, name='home'),
    path('login/', views.acoes_pngi_login, name='login'),
    path('dashboard/', views.acoes_pngi_dashboard, name='dashboard'),
    path('logout/', views.acoes_pngi_logout, name='logout'),
]