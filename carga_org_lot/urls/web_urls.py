from django.urls import path
from django.views.generic import RedirectView
from ..views.web_views import carga_login, carga_dashboard, carga_logout

app_name = 'carga_org_lot_web'

urlpatterns = [
    # Views de Interface Web
    path('', RedirectView.as_view(pattern_name='carga_org_lot_web:login'), name='home'),  # ← CORRIGIDO
    path('login/', carga_login, name='login'),
    path('dashboard/', carga_dashboard, name='dashboard'),
    path('logout/', carga_logout, name='logout'),
]
