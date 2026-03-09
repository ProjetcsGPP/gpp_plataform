# portal/views/web_views.py
"""
Views Web do Portal - REFATORADO com PortalAuthorizationService
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import User

from ..services.portal_authorization import get_portal_authorization_service


def portal_login(request):
    """
    Login do Portal - valida usuário e senha
    
    ✅ MANTIDO: Lógica de login permanece inalterada
    ✅ REFATORADO: Usa PortalAuthorizationService para validar acesso
    """
    if request.user.is_authenticated:
        return redirect("portal:dashboard")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validação de campos vazios
        if not email or not password:
            messages.error(request, "Por favor, preencha todos os campos.")
            return render(request, "portal/login.html")

        # Verifica se usuário existe
        try:
            user_exists = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(
                request, "Usuário não encontrado. Verifique o email informado."
            )
            return render(request, "portal/login.html")

        # Verifica se usuário está ativo
        if not user_exists.is_active:
            messages.error(
                request, "Usuário inativo. Entre em contato com o administrador."
            )
            return render(request, "portal/login.html")

        # Autentica usuário
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # ✅ REFATORADO: Usa PortalAuthorizationService
            # ✅ CORRIGIDO: Type hint adequado para user.id
            portal_service = get_portal_authorization_service()
            applications = portal_service.get_user_applications(user.id)  # type: ignore

            if not applications:
                messages.error(
                    request, "Usuário sem permissão de acesso a nenhuma aplicação."
                )
                return render(request, "portal/login.html")

            # Login bem-sucedido
            login(request, user)
            # ✅ CORRIGIDO: Type hint adequado para user.name
            messages.success(request, f"Bem-vindo(a), {user.name}!")  # type: ignore
            return redirect("portal:dashboard")
        else:
            messages.error(request, "Senha incorreta. Tente novamente.")
            return render(request, "portal/login.html")

    return render(request, "portal/login.html")


@login_required(login_url="/login/")
def portal_dashboard(request):
    """
    Dashboard do Portal - exibe aplicações disponíveis para o usuário

    ✅ REFATORADO: Usa PortalAuthorizationService
    ✅ PROTEGIDO: @login_required mantido
    """
    portal_service = get_portal_authorization_service()
    # ✅ CORRIGIDO: Type hint adequado para request.user.id
    portal_service = get_portal_authorization_service()
    applications = portal_service.get_user_applications(request.user.id)  # type: ignore

    return render(
        request,
        "portal/dashboard.html",
        {
            "user": request.user,
            "applications": applications,
        },
    )


def portal_logout(request):
    """
    Logout do Portal
    
    ✅ MANTIDO: Lógica inalterada
    """
    logout(request)
    messages.success(request, "Logout realizado com sucesso.")
    return redirect("portal:login")
