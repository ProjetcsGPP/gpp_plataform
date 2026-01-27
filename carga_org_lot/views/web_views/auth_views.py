"""
Views de Autenticação para Carga Org/Lot
"""

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import UserRole, Aplicacao, User


def carga_login(request):
    """
    GET/POST /carga_org_lot/login/
    
    Página de login do Carga Org/Lot.
    Valida usuário, senha e permissão para esta aplicação.
    """
    if request.user.is_authenticated:
        # Verifica se já tem acesso ao carga_org_lot
        has_access = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='CARGA_ORG_LOT'
        ).exists()
        
        if has_access:
            return redirect('carga_org_lot_web:dashboard')
        else:
            messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
            logout(request)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validação de campos vazios
        if not email or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'carga_org_lot/login.html')
        
        # Verifica se usuário existe
        try:
            user_exists = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado. Verifique o email informado.')
            return render(request, 'carga_org_lot/login.html')
        
        # Verifica se usuário está ativo
        if not user_exists.is_active:
            messages.error(request, 'Usuário inativo. Entre em contato com o administrador.')
            return render(request, 'carga_org_lot/login.html')
        
        # Autentica usuário
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Verifica se usuário tem acesso à aplicação CARGA_ORG_LOT
            try:
                app_carga = Aplicacao.objects.get(codigointerno='CARGA_ORG_LOT')
                user_role = UserRole.objects.filter(
                    user=user,
                    aplicacao=app_carga
                ).select_related('role').first()
                
                if not user_role:
                    messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
                    return render(request, 'carga_org_lot/login.html')
                
                # Login bem-sucedido
                login(request, user)
                messages.success(request, f'Bem-vindo(a) ao Carga Org/Lot, {user.name}!')
                return redirect('carga_org_lot_web:dashboard')
                
            except Aplicacao.DoesNotExist:
                messages.error(request, 'Aplicação não encontrada no sistema.')
                return render(request, 'carga_org_lot/login.html')
        else:
            messages.error(request, 'Senha incorreta. Tente novamente.')
            return render(request, 'carga_org_lot/login.html')
    
    return render(request, 'carga_org_lot/login.html')


def carga_logout(request):
    """
    GET /carga_org_lot/logout/
    
    Logout do Carga Org/Lot.
    """
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('carga_org_lot_web:login')


def carga_org_lot_required(view_func):
    """
    Decorador que verifica se usuário tem acesso ao Carga Org/Lot.
    Combina @login_required + verificação de role.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('carga_org_lot_web:login')
        
        # Verifica se usuário tem acesso à aplicação
        has_access = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='CARGA_ORG_LOT'
        ).exists()
        
        if not has_access:
            messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
            return redirect('carga_org_lot_web:login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
