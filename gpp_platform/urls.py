from django.contrib import admin
from django.urls import path, include
from auth_service.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Endpoints de autenticação JWT
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('portal/', include('portal.urls')),
    path('carga_org_lot/', include('carga_org_lot.urls')),
    path('acoes-pngi/', include('acoes_pngi.urls')), 
]