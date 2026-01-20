from django.urls import path
from ..views.api_views import api_acoes_pngi_dashboard, api_acoes_pngi_eixos, api_acoes_pngi_eixos_create, api_acoes_pngi_vigencias

urlpatterns = [
    path('', api_acoes_pngi_dashboard, name='api_acoes_pngi_dashboard'),
    path('eixos', api_acoes_pngi_eixos, name='api_acoes_pngi_eixos'),
    path('eixos/create', api_acoes_pngi_eixos_create, name='api_acoes_pngi_eixos_create'),
    path('vigencias', api_acoes_pngi_vigencias, name='api_acoes_pngi_vigencias'),
]