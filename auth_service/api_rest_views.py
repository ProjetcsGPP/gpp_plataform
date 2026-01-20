# auth_service/api_rest_views.py
"""
APIs REST explícitas para consumo do frontend Next.js.
Separadas completamente das views tradicionais em auth_service/views.py.

Prefixo: /api/auth-rest/
Razão: evitar conflito com qualquer rota existente.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_POST
def rest_login(request):
    """
    POST /api/auth-rest/login/
    
    Body: { "username": "...", "password": "..." }
    Response: { "detail": "...", "user": {...}, "csrfToken": "..." }
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'detail': 'JSON inválido.'}, status=400)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse(
            {'detail': 'username e password são obrigatórios.'},
            status=400
        )

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'detail': 'Credenciais inválidas.'}, status=401)

    login(request, user)
    csrf_token = get_token(request)

    return JsonResponse({
        'detail': 'Login realizado com sucesso.',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'csrfToken': csrf_token,
    })


@login_required
@require_GET
def rest_me(request):
    """
    GET /api/auth-rest/me/
    
    Retorna os dados do usuário logado.
    Response: { "id": ..., "username": "...", "email": "..." }
    """
    user = request.user
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })


@login_required
@require_POST
def rest_logout(request):
    """
    POST /api/auth-rest/logout/
    
    Response: { "detail": "..." }
    """
    logout(request)
    return JsonResponse({'detail': 'Logout realizado com sucesso.'})


@login_required
@require_GET
def rest_csrf_token(request):
    """
    GET /api/auth-rest/csrf-token/
    
    Retorna o CSRF token para o frontend usar em futuras requisições.
    Útil se usar abordagem de requisições SPA sem cookies.
    """
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})