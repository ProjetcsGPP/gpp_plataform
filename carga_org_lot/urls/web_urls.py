from django.urls import path
from django.views.generic import RedirectView
from ..views.web_views import carga_login, carga_dashboard, carga_logout

app_name = 'carga_org_lot'

urlpatterns = [
    # Views de Interface Web
    path('',RedirectView.as_view(pattern_name='carga_org_lot:login'), name='login'),
    path('login/', carga_login, name='login'),
    path('dashboard/', carga_dashboard, name='dashboard'),
    path('logout/', carga_logout, name='logout'),
    
    # APIs REST (já existentes)
    #path('api/home/', views.carga_home, name='api_home'),
    #path('api/upload-organograma/', views.UploadOrganogramaView.as_view(), name='upload_organograma'),
]
