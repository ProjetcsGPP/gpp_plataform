from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import UserRole, Aplicacao, User

def portal_login(request):
    """
    Login do Portal - valida usuário e senha
    """
    if request.user.is_authenticated:
        return redirect('portal:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validação de campos vazios
        if not email or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'portal/login.html')
        
        # Verifica se usuário existe
        try:
            user_exists = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado. Verifique o email informado.')
            return render(request, 'portal/login.html')
        
        # Verifica se usuário está ativo
        if not user_exists.is_active:
            messages.error(request, 'Usuário inativo. Entre em contato com o administrador.')
            return render(request, 'portal/login.html')
        
        # Autentica usuário
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Verifica se usuário tem acesso a pelo menos uma aplicação
            user_roles = UserRole.objects.filter(user=user).select_related('aplicacao')
            
            if not user_roles.exists():
                messages.error(request, 'Usuário sem permissão de acesso a nenhuma aplicação.')
                return render(request, 'portal/login.html')
            
            # Login bem-sucedido
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.name}!')
            return redirect('portal:dashboard')
        else:
            messages.error(request, 'Senha incorreta. Tente novamente.')
            return render(request, 'portal/login.html')
    
    return render(request, 'portal/login.html')


@login_required(login_url='/login/')  # ✅ Corrigido: usa /login/ em vez de /portal/login/
def portal_dashboard(request):
    """
    Dashboard do Portal - exibe aplicações disponíveis para o usuário
    
    Protegido por @login_required com redirecionamento para /login/
    (consistênte com settings.LOGIN_URL = '/login/')
    """
    user = request.user
    
    # Busca todas as aplicações que o usuário tem acesso
    roles = (
        UserRole.objects
        .filter(user=user)
        .select_related('aplicacao', 'role')
    )
    
    # Organiza aplicações por código interno (evita duplicatas)
    apps_dict = {}
    for ur in roles:
        app_code = ur.aplicacao.codigointerno
        if app_code not in apps_dict:
            if not ur.aplicacao.isshowinportal:
                continue
            
            apps_dict[app_code] = {
                'aplicacao': ur.aplicacao,
                'roles': []
            }
        apps_dict[app_code]['roles'].append(ur.role)
    
    return render(request, 'portal/dashboard.html', {
        'user': user,
        'applications': apps_dict.values(),
    })


def portal_logout(request):
    """
    Logout do Portal
    """
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('portal:login')