from django.contrib import admin
from django.urls import path, include
from auth_service.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from auth_service import api_views as auth_api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication (para APIs REST)
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Session Authentication (para Next.js)
    path('api/auth/login', auth_api_views.api_login, name='api_login'),
    path('api/auth/logout', auth_api_views.api_logout, name='api_logout'),
    path('api/auth/me', auth_api_views.api_me, name='api_me'),
    
    # Apps tradicionais (Django templates)
    path('portal/', include('portal.urls')),  # rotas das views tradicionais
    path('carga_org_lot/', include('carga_org_lot.urls')),  # rotas das views tradicionais
    path('acoes-pngi/', include('acoes_pngi.urls')),  # rotas das views tradicionais
    
    
    # APIs REST explícitas para o frontend Next.js
    path('', include('auth_service.api_urls')), # /api/auth-rest/*
    path('', include('portal.api_urls')),       # /api/portal-rest/*
]