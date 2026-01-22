from django.urls import path
from ..views.api_views import api_acoes_pngi_dashboard, api_acoes_pngi_eixos, api_acoes_pngi_eixos_create, api_acoes_pngi_vigencias, api_acoes_pngi_criar_usuario

#urlpatterns = [
#    path('', api_acoes_pngi_dashboard, name='api_acoes_pngi_dashboard'),
#    path('eixos', api_acoes_pngi_eixos, name='api_acoes_pngi_eixos'),
#    path('eixos/create', api_acoes_pngi_eixos_create, name='api_acoes_pngi_eixos_create'),
#    path('vigencias', api_acoes_pngi_vigencias, name='api_acoes_pngi_vigencias'),
#]


app_name = 'acoes_pngi'

urlpatterns = [
    path('', api_acoes_pngi_dashboard, name='dashboard'),
    path('usuario/', api_acoes_pngi_criar_usuario, name='criar_usuario'),
    path('eixos/', api_acoes_pngi_eixos, name='eixos_list'),
    path('eixos/', api_acoes_pngi_eixos_create, name='eixos_create'),
    path('vigencias/', api_acoes_pngi_vigencias, name='vigencias'),
]