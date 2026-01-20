from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.portal_login, name='home'),  # Redireciona raiz para login
    path('login/', views.portal_login, name='login'),
    path('dashboard/', views.portal_dashboard, name='dashboard'),
    path('logout/', views.portal_logout, name='logout'),
]