from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import UserRole, Aplicacao, User

def carga_login(request):
    """
    Login do Carga Org Lot - valida usuário, senha e permissão para esta aplicação
    """
    if request.user.is_authenticated:
        # Verifica se já tem acesso ao carga_org_lot
        has_access = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='CARGA_ORG_LOT'
        ).exists()
        
        if has_access:
            return redirect('carga_org_lot_web:dashboard')  # ← MUDOU
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
            user_exists = User.objects.get(stremail=email)  # ← CORRIGIDO: use stremail
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
                messages.success(request, f'Bem-vindo(a) ao Carga Org Lot, {user.strnome}!')  # ← CORRIGIDO: use strnome
                return redirect('carga_org_lot_web:dashboard')  # ← MUDOU
                
            except Aplicacao.DoesNotExist:
                messages.error(request, 'Aplicação não encontrada no sistema.')
                return render(request, 'carga_org_lot/login.html')
        else:
            messages.error(request, 'Senha incorreta. Tente novamente.')
            return render(request, 'carga_org_lot/login.html')
    
    return render(request, 'carga_org_lot/login.html')


@login_required(login_url='/carga_org_lot/login/')
def carga_dashboard(request):
    """
    Dashboard do Carga Org Lot - verifica permissões específicas
    """
    user = request.user
    
    # Verifica se usuário tem acesso à aplicação
    try:
        app_carga = Aplicacao.objects.get(codigointerno='CARGA_ORG_LOT')
        user_role = UserRole.objects.filter(
            user=user,
            aplicacao=app_carga
        ).select_related('role').first()
        
        if not user_role:
            messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
            return redirect('carga_org_lot_web:login')  # ← MUDOU
        
        return render(request, 'carga_org_lot/dashboard.html', {
            'user': user,
            'role': user_role.role,
            'aplicacao': app_carga,
        })
        
    except Aplicacao.DoesNotExist:
        messages.error(request, 'Aplicação não encontrada no sistema.')
        return redirect('carga_org_lot_web:login')  # ← MUDOU


def carga_logout(request):
    """
    Logout do Carga Org Lot
    """
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('carga_org_lot_web:login')  # ← MUDOU
