# portal/api_rest_views.py
"""
APIs REST explícitas para consumo do frontend Next.js.
Separadas das views tradicionais em portal/views.py.

Prefixo: /api/portal-rest/
"""

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from .models import Application


@login_required
@require_GET
def rest_list_applications(request):
    """
    GET /api/portal-rest/applications/
    
    Lista todas as aplicações que o usuário logado pode acessar.
    Response: [{ "id": ..., "name": "...", "slug": "...", "url": "...", "description": "..." }, ...]
    """
    user = request.user
    apps = Application.objects.filter(users=user).order_by('name')

    data = [
        {
            'id': app.id,
            'name': app.name,
            'slug': app.slug,
            'url': app.url,
            'description': app.description,
        }
        for app in apps
    ]

    return JsonResponse(data, safe=False)


@login_required
@require_GET
def rest_check_app_access(request, slug):
    """
    GET /api/portal-rest/applications/<slug>/access/
    
    Verifica se o usuário tem acesso à aplicação específica.
    Response: { "application": {...}, "hasAccess": bool }
    """
    user = request.user
    try:
        app = Application.objects.get(slug=slug)
    except Application.DoesNotExist:
        return JsonResponse(
            {'detail': 'Aplicação não encontrada.'},
            status=404
        )

    has_access = app.users.filter(id=user.id).exists()

    return JsonResponse({
        'application': {
            'id': app.id,
            'name': app.name,
            'slug': app.slug,
            'url': app.url,
            'description': app.description,
        },
        'hasAccess': has_access,
    })


@login_required
@require_GET
def rest_get_application(request, slug):
    """
    GET /api/portal-rest/applications/<slug>/
    
    Retorna detalhes de uma aplicação específica (sem verificar acesso).
    Útil para o frontend exibir dados da app mesmo sem acesso (para mensagem de alerta).
    Response: { "id": ..., "name": "...", "slug": "...", "url": "...", "description": "..." }
    """
    try:
        app = Application.objects.get(slug=slug)
    except Application.DoesNotExist:
        return JsonResponse(
            {'detail': 'Aplicação não encontrada.'},
            status=404
        )

    return JsonResponse({
        'id': app.id,
        'name': app.name,
        'slug': app.slug,
        'url': app.url,
        'description': app.description,
    })