from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.api_acoes_pngi_dashboard, name='api_acoes_pngi_dashboard'),
    path('eixos', api_views.api_acoes_pngi_eixos, name='api_acoes_pngi_eixos'),
    path('eixos/create', api_views.api_acoes_pngi_eixos_create, name='api_acoes_pngi_eixos_create'),
    path('vigencias', api_views.api_acoes_pngi_vigencias, name='api_acoes_pngi_vigencias'),
]