from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import UserRole, Aplicacao


@login_required
def portal_home(request):
    user = request.user

    # Todas as aplicações em que o usuário tem algum role
    roles = (
        UserRole.objects
        .filter(user=user)
        .select_related('aplicacao')
    )

    apps = {ur.aplicacao.codigointerno: ur.aplicacao for ur in roles}

    return render(request, 'portal/home.html', {
        'applications': apps.values(),
    })