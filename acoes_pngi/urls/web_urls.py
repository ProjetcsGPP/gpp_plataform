"""
URLs Web (Django templates) para a aplicação Ações PNGI.
Prefixo aplicado em gpp_platform/urls.py: /acoes-pngi/
"""

from django.urls import path
from ..views.web_views import (
    acoes_pngi_login,
    acoes_pngi_dashboard,
    acoes_pngi_logout,
    eixos_list,
    eixo_create,
    eixo_update,
    eixo_delete,
    vigencia_create,
    vigencia_update,
    vigencia_delete,
    vigencias_list
)

app_name = 'acoes_pngi_web'

urlpatterns = [
    # =========================================================================
    # AUTENTICAÇÃO
    # =========================================================================
    path('', acoes_pngi_login, name='home'),
    path('login/', acoes_pngi_login, name='login'),
    path('logout/', acoes_pngi_logout, name='logout'),
    
    # =========================================================================
    # DASHBOARD
    # =========================================================================
    path('dashboard/', acoes_pngi_dashboard, name='dashboard'),
    
    # =========================================================================
    # EIXOS
    # =========================================================================
    path('eixos/', eixos_list, name='eixos_list'),
    path('eixos/criar/', eixo_create, name='eixo_create'),
    path('eixos/<int:pk>/editar/', eixo_update, name='eixo_update'),
    path('eixos/<int:pk>/deletar/', eixo_delete, name='eixo_delete'),
    
    # =========================================================================
    # SITUAÇÕES (TODO: implementar)
    # =========================================================================
    # path('situacoes/', situacoes_list, name='situacoes_list'),
    # path('situacoes/criar/', situacao_create, name='situacao_create'),
    # path('situacoes/<int:pk>/editar/', situacao_update, name='situacao_update'),
    # path('situacoes/<int:pk>/deletar/', situacao_delete, name='situacao_delete'),
    
    # =========================================================================
    # VIGÊNCIAS 
    # =========================================================================
    path('vigencias/', vigencias_list, name='vigencias_list'),
    path('vigencias/criar/', vigencia_create, name='vigencia_create'),
    path('vigencias/<int:pk>/editar/', vigencia_update, name='vigencia_update'),
    path('vigencias/<int:pk>/deletar/', vigencia_delete, name='vigencia_delete'),
]
