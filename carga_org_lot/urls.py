from django.urls import path
from .views import carga_home

app_name = 'carga_org_lot'

urlpatterns = [
    path('', carga_home, name='home'),
]