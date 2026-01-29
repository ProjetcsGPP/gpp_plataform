# accounts/urls/__init__.py
from django.urls import path
from accounts.views import role_views

app_name = 'accounts'

urlpatterns = [
    # ... URLs existentes de login/logout
    path('select-role/<str:app_code>/', role_views.select_role, name='select_role'),
    path('set-role/<int:role_id>/', role_views.set_active_role, name='set_active_role'),
    path('switch-role/<str:app_code>/', role_views.switch_role, name='switch_role'),
]
