# accounts/views/role_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from accounts.models import UserRole, Aplicacao

@login_required
def select_role(request, app_code):
    """
    View para seleção de papel/perfil para uma aplicação
    """
    # Busca a aplicação
    aplicacao = get_object_or_404(Aplicacao, codigointerno=app_code)
    
    # Busca todos os papéis do usuário para esta aplicação
    user_roles = UserRole.objects.filter(
        user=request.user,
        aplicacao=aplicacao
    ).select_related('role')
    
    # Se não tem nenhum papel, erro
    if not user_roles.exists():
        messages.error(request, f'Você não possui acesso à aplicação {aplicacao.nomeaplicacao}')
        return redirect('portal:dashboard')  # Redireciona para o portal
    
    # Se tem apenas 1 papel, seleciona automaticamente
    if user_roles.count() == 1:
        return set_active_role(request, user_roles.first().id, app_code)
    
    # Se é POST, processa seleção
    if request.method == 'POST':
        role_id = request.POST.get('role_id')
        if role_id:
            return set_active_role(request, role_id, app_code)
    
    # Renderiza tela de seleção
    context = {
        'aplicacao': aplicacao,
        'user_roles': user_roles,
        'app_code': app_code,
    }
    return render(request, 'accounts/select_role.html', context)


@login_required
def set_active_role(request, role_id, app_code=None):
    """
    Define o papel ativo na sessão e redireciona para a aplicação
    """
    # Valida que o papel pertence ao usuário
    user_role = get_object_or_404(
        UserRole.objects.select_related('role', 'aplicacao'),
        id=role_id,
        user=request.user
    )
    
    app_code = app_code or user_role.aplicacao.codigointerno
    
    # Salva na sessão
    session_key = f'active_role_{app_code}'
    request.session[session_key] = user_role.id
    request.session.modified = True
    
    messages.success(
        request, 
        f'Papel {user_role.role.nomeperfil} ativado para {user_role.aplicacao.nomeaplicacao}'
    )
    
    # Redireciona para dashboard da aplicação
    if app_code == 'ACOES_PNGI':
        return redirect('acoes_pngi:dashboard')
    elif app_code == 'CARGA_ORG_LOT':
        return redirect('carga_org_lot:dashboard')
    elif app_code == 'PORTAL':
        return redirect('portal:dashboard')
    else:
        return redirect('/')


@login_required
def switch_role(request, app_code):
    """
    Permite trocar de papel sem fazer novo login
    """
    # Limpa papel atual da sessão
    session_key = f'active_role_{app_code}'
    if session_key in request.session:
        del request.session[session_key]
    
    # Redireciona para seleção
    return redirect('accounts:select_role', app_code=app_code)
