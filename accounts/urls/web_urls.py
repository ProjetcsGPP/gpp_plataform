'''
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Include app URLs
    path('api/accounts/', include('accounts.urls')),
    path('api/auth_service/', include('auth_service.urls')),
    path('api/portal/', include('portal.urls')),
    path('api/carga_org_lot/', include('carga_org_lot.urls')),
    path('api/db_service/', include('db_service.urls')),
]
'''