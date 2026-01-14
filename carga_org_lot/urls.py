from django.urls import path
from . import views

app_name = 'carga_org_lot'

urlpatterns = [
    # Views de Interface Web
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    
    # APIs REST (já existentes)
    path('api/home/', views.carga_home, name='api_home'),
    path('api/upload-organograma/', views.UploadOrganogramaView.as_view(), name='upload_organograma'),
]