"""
URLs principais da aplicação Ações PNGI
Inclui API + Web views
"""

from django.urls import path, include

app_name = 'acoes_pngi'  # Namespace principal

urlpatterns = [
    # APIs REST
    path('api/', include('acoes_pngi.urls.api_urls', namespace='acoes_pngi_api')),
    
    # Web Views (Django templates)
    path('', include('acoes_pngi.urls.web_urls', namespace='acoes_pngi_web')),
]
