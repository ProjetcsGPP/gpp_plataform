# accounts/views/role_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import UserRole, Aplicacao


@login_required
def select_role(request, app_code):
    """View para seleção de papel/perfil para uma aplicação"""
    aplicacao = get_object_or_404(Aplicacao, codigointerno=app_code)
    
    user_roles = UserRole.objects.filter(
        user=request.user,
        aplicacao=aplicacao
    ).select_related('role')
    
    if not user_roles.exists():
        messages.error(request, f'Você não possui acesso à aplicação {aplicacao.nomeaplicacao}')
        return redirect('portal:dashboard')
    
    if user_roles.count() == 1:
        return set_active_role(request, user_roles.first().id, app_code)
    
    if request.method == 'POST':
        role_id = request.POST.get('role_id')
        if role_id:
            return set_active_role(request, role_id, app_code)
    
    context = {
        'aplicacao': aplicacao,
        'user_roles': user_roles,
        'app_code': app_code,
    }
    return render(request, 'accounts/select_role.html', context)


@login_required
def set_active_role(request, role_id, app_code=None):
    """Define o papel ativo na sessão e redireciona para a aplicação"""
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
    
    # Redireciona para dashboard da aplicação usando os namespaces WEB corretos
    if app_code == 'ACOES_PNGI':
        return redirect('acoes_pngi_web:dashboard')  # ← CORRIGIDO
    elif app_code == 'CARGA_ORG_LOT':
        return redirect('carga_org_lot_web:dashboard')  # ← CORRIGIDO
    elif app_code == 'PORTAL':
        return redirect('portal:dashboard')  # ← Este já estava correto
    else:
        return redirect('/')


@login_required
def switch_role(request, app_code):
    """Permite trocar de papel sem fazer novo login"""
    session_key = f'active_role_{app_code}'
    if session_key in request.session:
        del request.session[session_key]
    
    return redirect('accounts:select_role', app_code=app_code)
