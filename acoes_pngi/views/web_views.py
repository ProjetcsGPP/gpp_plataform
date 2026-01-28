"""
Views web (Django templates) para a aplicação Ações PNGI.
Usa autenticação por sessão e verifica permissões através do sistema RBAC.
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

from accounts.models import UserRole, Aplicacao, User
from ..models import Eixo, SituacaoAcao, VigenciaPNGI


def require_acoes_access(view_func):
    """
    Decorator que verifica se o usuário tem acesso à aplicação Ações PNGI.
    Deve ser usado após @login_required.
    """
    def wrapper(request, *args, **kwargs):
        # Verifica se usuário tem acesso à aplicação
        has_access = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).exists()
        
        if not has_access:
            messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
            return redirect('acoes_pngi_web:login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def require_acoes_permission(permission_codename):
    """
    Decorator que verifica se o usuário tem uma permissão específica do Ações PNGI.
    
    Uso:
        @require_acoes_permission('add_eixo')
        def criar_eixo_view(request):
            ...
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.has_app_perm('ACOES_PNGI', permission_codename):
                messages.error(
                    request, 
                    f'Você não tem permissão para realizar esta ação. '
                    f'Permissão necessária: {permission_codename}'
                )
                return redirect('acoes_pngi_web:dashboard')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def acoes_pngi_login(request):
    """
    Login do Ações PNGI - valida usuário, senha e permissão para esta aplicação.
    """
    if request.user.is_authenticated:
        # Verifica se já tem acesso ao acoes_pngi
        has_access = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).exists()
        
        if has_access:
            return redirect('acoes_pngi_web:dashboard')
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
            user_exists = User.objects.get(stremail=email)
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
                messages.success(request, f'Bem-vindo(a) ao Ações PNGI, {user.strnome}!')
                return redirect('acoes_pngi_web:dashboard')
                
            except Aplicacao.DoesNotExist:
                messages.error(request, 'Aplicação não encontrada no sistema.')
                return render(request, 'acoes_pngi/login.html')
        else:
            messages.error(request, 'Senha incorreta. Tente novamente.')
            return render(request, 'acoes_pngi/login.html')
    
    return render(request, 'acoes_pngi/login.html')


@login_required(login_url='/acoes-pngi/login/')
@require_acoes_access
def acoes_pngi_dashboard(request):
    """
    Dashboard do Ações PNGI - exibe estatísticas e informações do sistema.
    Usa o sistema de permissões para controlar o que o usuário pode ver e fazer.
    """
    user = request.user
    
    # Busca informações do usuário e role
    app_acoes = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
    user_role = UserRole.objects.filter(
        user=user,
        aplicacao=app_acoes
    ).select_related('role').first()
    
    # Busca permissões do usuário usando o sistema RBAC
    permissions = user.get_app_permissions('ACOES_PNGI')
    
    # Busca estatísticas (apenas se tiver permissão de view)
    stats = {}
    ultimos_eixos = []
    vigencia_atual = None
    
    if user.has_app_perm('ACOES_PNGI', 'view_eixo'):
        stats['total_eixos'] = Eixo.objects.count()
        ultimos_eixos = Eixo.objects.order_by('-created_at')[:5]
    
    if user.has_app_perm('ACOES_PNGI', 'view_situacaoacao'):
        stats['total_situacoes'] = SituacaoAcao.objects.count()
    
    if user.has_app_perm('ACOES_PNGI', 'view_vigenciapngi'):
        stats['total_vigencias'] = VigenciaPNGI.objects.count()
        stats['vigencias_ativas'] = VigenciaPNGI.objects.filter(isvigenciaativa=True).count()
        vigencia_atual = VigenciaPNGI.objects.filter(isvigenciaativa=True).first()
    
    # Determinar capacidades do usuário baseado nas permissões
    can_manage_config = (
        user.has_app_perm('ACOES_PNGI', 'add_eixo') or
        user.has_app_perm('ACOES_PNGI', 'add_situacaoacao') or
        user.has_app_perm('ACOES_PNGI', 'add_vigenciapngi')
    )
    
    can_delete = (
        user.has_app_perm('ACOES_PNGI', 'delete_eixo') or
        user.has_app_perm('ACOES_PNGI', 'delete_situacaoacao') or
        user.has_app_perm('ACOES_PNGI', 'delete_vigenciapngi')
    )
    
    return render(request, 'acoes_pngi/dashboard.html', {
        'user': user,
        'role': user_role.role if user_role else None,
        'role_display': user_role.role.strnomerole if user_role else 'Sem Role',
        'aplicacao': app_acoes,
        'stats': stats,
        'ultimos_eixos': ultimos_eixos,
        'vigencia_atual': vigencia_atual,
        'permissions': permissions,
        'can_manage_config': can_manage_config,
        'can_delete': can_delete,
        # Permissões específicas para usar nos templates
        'can_add_eixo': user.has_app_perm('ACOES_PNGI', 'add_eixo'),
        'can_change_eixo': user.has_app_perm('ACOES_PNGI', 'change_eixo'),
        'can_delete_eixo': user.has_app_perm('ACOES_PNGI', 'delete_eixo'),
        'can_view_eixo': user.has_app_perm('ACOES_PNGI', 'view_eixo'),
        'can_add_situacao': user.has_app_perm('ACOES_PNGI', 'add_situacaoacao'),
        'can_change_situacao': user.has_app_perm('ACOES_PNGI', 'change_situacaoacao'),
        'can_delete_situacao': user.has_app_perm('ACOES_PNGI', 'delete_situacaoacao'),
        'can_view_situacao': user.has_app_perm('ACOES_PNGI', 'view_situacaoacao'),
        'can_add_vigencia': user.has_app_perm('ACOES_PNGI', 'add_vigenciapngi'),
        'can_change_vigencia': user.has_app_perm('ACOES_PNGI', 'change_vigenciapngi'),
        'can_delete_vigencia': user.has_app_perm('ACOES_PNGI', 'delete_vigenciapngi'),
        'can_view_vigencia': user.has_app_perm('ACOES_PNGI', 'view_vigenciapngi'),
    })


@login_required(login_url='/acoes-pngi/login/')
@require_acoes_access
@require_acoes_permission('view_eixo')
def eixos_list(request):
    """
    Lista todos os eixos cadastrados.
    Requer permissão: view_eixo
    """
    eixos = Eixo.objects.all().order_by('stralias')
    
    return render(request, 'acoes_pngi/eixos/list.html', {
        'eixos': eixos,
        'can_add': request.user.has_app_perm('ACOES_PNGI', 'add_eixo'),
        'can_edit': request.user.has_app_perm('ACOES_PNGI', 'change_eixo'),
        'can_delete': request.user.has_app_perm('ACOES_PNGI', 'delete_eixo'),
    })


@login_required(login_url='/acoes-pngi/login/')
@require_acoes_access
@require_acoes_permission('add_eixo')
def eixo_create(request):
    """
    Cria um novo eixo.
    Requer permissão: add_eixo
    """
    if request.method == 'POST':
        strdescricaoeixo = request.POST.get('strdescricaoeixo')
        stralias = request.POST.get('stralias', '').upper()
        
        if not strdescricaoeixo or not stralias:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'acoes_pngi/eixos/form.html')
        
        if len(stralias) > 5:
            messages.error(request, 'O alias deve ter no máximo 5 caracteres.')
            return render(request, 'acoes_pngi/eixos/form.html', {
                'strdescricaoeixo': strdescricaoeixo,
                'stralias': stralias,
            })
        
        try:
            eixo = Eixo.objects.create(
                strdescricaoeixo=strdescricaoeixo,
                stralias=stralias
            )
            messages.success(request, f'Eixo "{eixo.strdescricaoeixo}" criado com sucesso!')
            return redirect('acoes_pngi_web:eixos_list')
        except Exception as e:
            messages.error(request, f'Erro ao criar eixo: {str(e)}')
            return render(request, 'acoes_pngi/eixos/form.html', {
                'strdescricaoeixo': strdescricaoeixo,
                'stralias': stralias,
            })
    
    return render(request, 'acoes_pngi/eixos/form.html')


@login_required(login_url='/acoes-pngi/login/')
@require_acoes_access
@require_acoes_permission('change_eixo')
def eixo_update(request, pk):
    """
    Atualiza um eixo existente.
    Requer permissão: change_eixo
    """
    try:
        eixo = Eixo.objects.get(pk=pk)
    except Eixo.DoesNotExist:
        messages.error(request, 'Eixo não encontrado.')
        return redirect('acoes_pngi_web:eixos_list')
    
    if request.method == 'POST':
        strdescricaoeixo = request.POST.get('strdescricaoeixo')
        stralias = request.POST.get('stralias', '').upper()
        
        if not strdescricaoeixo or not stralias:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'acoes_pngi/eixos/form.html', {'eixo': eixo})
        
        if len(stralias) > 5:
            messages.error(request, 'O alias deve ter no máximo 5 caracteres.')
            return render(request, 'acoes_pngi/eixos/form.html', {'eixo': eixo})
        
        try:
            eixo.strdescricaoeixo = strdescricaoeixo
            eixo.stralias = stralias
            eixo.save()
            messages.success(request, f'Eixo "{eixo.strdescricaoeixo}" atualizado com sucesso!')
            return redirect('acoes_pngi_web:eixos_list')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar eixo: {str(e)}')
            return render(request, 'acoes_pngi/eixos/form.html', {'eixo': eixo})
    
    return render(request, 'acoes_pngi/eixos/form.html', {'eixo': eixo})


@login_required(login_url='/acoes-pngi/login/')
@require_acoes_access
@require_acoes_permission('delete_eixo')
def eixo_delete(request, pk):
    """
    Deleta um eixo.
    Requer permissão: delete_eixo
    """
    try:
        eixo = Eixo.objects.get(pk=pk)
        nome = eixo.strdescricaoeixo
        eixo.delete()
        messages.success(request, f'Eixo "{nome}" deletado com sucesso!')
    except Eixo.DoesNotExist:
        messages.error(request, 'Eixo não encontrado.')
    except Exception as e:
        messages.error(request, f'Erro ao deletar eixo: {str(e)}')
    
    return redirect('acoes_pngi_web:eixos_list')


def acoes_pngi_logout(request):
    """
    Logout do Ações PNGI.
    """
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('acoes_pngi_web:login')
