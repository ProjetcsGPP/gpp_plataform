"""
GPP Platform - URLs principais
Organização:
- /admin/ -> Django Admin
- /api/v1/auth/ -> APIs de autenticação (JWT + Session)
- /api/v1/<app>/ -> APIs REST para consumo do Next.js
- /<app>/ -> Views tradicionais Django (templates HTML)
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # =========================================================================
    # DJANGO ADMIN
    # =========================================================================
    path('admin/', admin.site.urls),
    
    
    # =========================================================================
    # APIs REST - Autenticação (para Next.js)
    # Prefixo: /api/v1/auth/
    # =========================================================================
    path('api/v1/auth/', include('auth_service.api_urls')),
    
    
    # =========================================================================
    # APIs REST - Aplicações (para Next.js)
    # Prefixo: /api/v1/<app>/
    # =========================================================================
    path('api/v1/portal/', include('portal.api_urls')),
    path('api/v1/acoes/', include('acoes_pngi.api_urls')),
    path('api/v1/carga/', include('carga_org_lot.api_urls')),
    # path('api/v1/accounts/', include('accounts.api_urls')),  # TODO: criar accounts/api_urls.py
    # path('api/v1/db/', include('db_service.api_urls')),      # TODO: criar db_service/api_urls.py
    
    
    # =========================================================================
    # VIEWS TRADICIONAIS - Django Templates (páginas web internas)
    # Prefixo: /<app>/
    # =========================================================================
    path('', include('portal.urls')),                    # Portal (index, etc)
    path('acoes-pngi/', include('acoes_pngi.urls')),     # Ações PNGI
    path('carga/', include('carga_org_lot.urls')),       # Carga de Organogramas
    path('accounts/', include('accounts.urls')),         # Gestão de contas
    # path('db/', include('db_service.urls')),           # TODO: criar db_service/urls.py
]