from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('select-role/<str:app_code>/', views.select_role, name='select_role'),
    path('set-role/<int:role_id>/', views.set_active_role, name='set_active_role'),
    path('switch-role/<str:app_code>/', views.switch_role, name='switch_role'),
]
