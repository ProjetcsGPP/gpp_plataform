from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import UserRole, Aplicacao, User
from ..models import Eixo, SituacaoAcao, VigenciaPNGI


def acoes_pngi_login(request):
    """
    Login do Ações PNGI - valida usuário, senha e permissão para esta aplicação
    """
    if request.user.is_authenticated:
        # Verifica se já tem acesso ao acoes_pngi
        has_access = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).exists()
        
        if has_access:
            return redirect('acoes_pngi:dashboard')
        else:
            messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
            logout(request)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validação de campos vazios
        if not email or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'acoes_pngi/login.html')
        
        # Verifica se usuário existe
        try:
            user_exists = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado. Verifique o email informado.')
            return render(request, 'acoes_pngi/login.html')
        
        # Verifica se usuário está ativo
        if not user_exists.is_active:
            messages.error(request, 'Usuário inativo. Entre em contato com o administrador.')
            return render(request, 'acoes_pngi/login.html')
        
        # Autentica usuário
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Verifica se usuário tem acesso à aplicação ACOES_PNGI
            try:
                app_acoes = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
                user_role = UserRole.objects.filter(
                    user=user,
                    aplicacao=app_acoes
                ).select_related('role').first()
                
                if not user_role:
                    messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
                    return render(request, 'acoes_pngi/login.html')
                
                # Login bem-sucedido
                login(request, user)
                messages.success(request, f'Bem-vindo(a) ao Ações PNGI, {user.name}!')
                return redirect('acoes_pngi:dashboard')
                
            except Aplicacao.DoesNotExist:
                messages.error(request, 'Aplicação não encontrada no sistema.')
                return render(request, 'acoes_pngi/login.html')
        else:
            messages.error(request, 'Senha incorreta. Tente novamente.')
            return render(request, 'acoes_pngi/login.html')
    
    return render(request, 'acoes_pngi/login.html')


@login_required(login_url='/acoes-pngi/login/')
def acoes_pngi_dashboard(request):
    """
    Dashboard do Ações PNGI - verifica permissões específicas e exibe estatísticas
    """
    user = request.user
    
    # Verifica se usuário tem acesso à aplicação
    try:
        app_acoes = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
        user_role = UserRole.objects.filter(
            user=user,
            aplicacao=app_acoes
        ).select_related('role').first()
        
        if not user_role:
            messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
            return redirect('acoes_pngi:login')
        
        # Busca estatísticas
        total_eixos = Eixo.objects.count()
        total_situacoes = SituacaoAcao.objects.count()
        total_vigencias = VigenciaPNGI.objects.count()
        vigencias_ativas = VigenciaPNGI.objects.filter(isvigenciaativa=True).count()
        
        # Busca últimos registros
        ultimos_eixos = Eixo.objects.all()[:5]
        vigencia_atual = VigenciaPNGI.objects.filter(isvigenciaativa=True).first()
        
        return render(request, 'acoes_pngi/dashboard.html', {
            'user': user,
            'role': user_role.role,
            'aplicacao': app_acoes,
            'stats': {
                'total_eixos': total_eixos,
                'total_situacoes': total_situacoes,
                'total_vigencias': total_vigencias,
                'vigencias_ativas': vigencias_ativas,
            },
            'ultimos_eixos': ultimos_eixos,
            'vigencia_atual': vigencia_atual,
        })
        
    except Aplicacao.DoesNotExist:
        messages.error(request, 'Aplicação não encontrada no sistema.')
        return redirect('acoes_pngi:login')


def acoes_pngi_logout(request):
    """
    Logout do Ações PNGI
    """
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('acoes_pngi:login')