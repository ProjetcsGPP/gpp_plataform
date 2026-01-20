"""
URLs das views web do Portal
Prefixo aplicado em gpp_platform/urls.py: /
"""

from django.urls import path
from ..views.web_views import portal_login, portal_dashboard, portal_logout

app_name = 'portal'

urlpatterns = [
    path('', portal_login, name='home'),
    path('login/', portal_login, name='login'),
    path('dashboard/', portal_dashboard, name='dashboard'),
    path('logout/', portal_logout, name='logout'),
]