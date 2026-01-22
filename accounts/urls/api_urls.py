from django.urls import path
from ..views.api_views import UserManagementView

urlpatterns = [
    path('api/gestao/usuarios/', UserManagementView.as_view()),
]


from django.urls import path
from .views import api_views

app_name = 'acoes_pngi'
urlpatterns = [
    path('api/acoes_pngi/', api_views.api_acoes_pngi_dashboard, name='dashboard'),
    path('api/acoes_pngi/usuario/', api_views.api_acoes_pngi_criar_usuario, name='criar_usuario'),
    path('api/acoes_pngi/eixos/', api_views.api_acoes_pngi_eixos, name='eixos'),
    path('api/acoes_pngi/eixos/', api_views.api_acoes_pngi_eixos_create, name='eixos_create'),
    path('api/acoes_pngi/vigencias/', api_views.api_acoes_pngi_vigencias, name='vigencias'),
]
