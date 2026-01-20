from django.urls import path
from django.views.generic import RedirectView
from ..views.web_views import views

app_name = 'carga_org_lot'

urlpatterns = [
    # Views de Interface Web
    path('',RedirectView.as_view(pattern_name='carga_org_lot:login'), name='login'),
    path('login/', views.carga_login, name='login'),
    path('dashboard/', views.carga_dashboard, name='dashboard'),
    path('logout/', views.carga_logout, name='logout'),
    
    # APIs REST (já existentes)
    #path('api/home/', views.carga_home, name='api_home'),
    #path('api/upload-organograma/', views.UploadOrganogramaView.as_view(), name='upload_organograma'),
]
