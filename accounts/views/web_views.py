# accounts/views/web_views.py
from django.http import HttpResponseRedirect
from django.conf import settings

def set_jwt_cookies(response, access_token, refresh_token):
    """
    Define JWT tokens em cookies HttpOnly/Secure para web tradicional
    """
    # Access token (curto)
    response.set_cookie(
        'access_token',
        access_token,
        max_age=600,  # 10 min
        httponly=True,
        secure=settings.DEBUG == False,  # HTTPS em produção
        samesite='lax',
        path='/'
    )
    
    # Refresh token (longo)
    response.set_cookie(
        'refresh_token',
        refresh_token,
        max_age=1800,  # 30 min
        httponly=True,
        secure=settings.DEBUG == False,
        samesite='lax',
        path='/'
    )
    return response
