from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User, UserRole
from .permissions import CanManageCarga


# ============================================
# Views de API (já existentes)
# ============================================

class UploadOrganogramaView(APIView):
    permission_classes = [CanManageCarga]

    def post(self, request):
        # receber arquivo, criar OrganogramaVersao, etc.
        return Response({'status': 'ok'})


@api_view(['GET'])
@permission_classes([CanManageCarga])
def carga_home(request):
    """
    Entrada da aplicação de carga de organograma/lotação.
    Só deixa entrar se o JWT tiver role/atributo corretos.
    """
    user = request.user
    return Response({
        'message': 'Bem-vindo à Carga de Organograma/Lotação',
        'user': user.email,
    })


# ============================================
# Views de Interface Web (novas)
# ============================================

def login_view(request):
    """Página de login do Carga Org Lot"""
    # Se já está logado, redireciona para o dashboard
    if 'user_id' in request.session:
        return redirect('carga_org_lot:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Por favor, preencha email e senha.')
            return render(request, 'carga_org_lot/login.html')
        
        # Autentica o usuário
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Verifica se o usuário está ativo
            if not user.is_active:
                messages.error(request, 'Sua conta está inativa. Entre em contato com o administrador.')
                return render(request, 'carga_org_lot/login.html')
            
            # Verifica se o usuário tem permissão para acessar carga_org_lot
            has_permission = UserRole.objects.filter(
                user=user,
                aplicacao__codigointerno='CARGA_ORG_LOT'
            ).exists()
            
            if has_permission:
                # Gera token JWT
                refresh = RefreshToken.for_user(user)
                
                # Salva informações na sessão
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                request.session['user_name'] = user.name
                request.session['access_token'] = str(refresh.access_token)
                request.session['refresh_token'] = str(refresh)
                
                messages.success(request, f'Bem-vindo, {user.name}!')
                return redirect('carga_org_lot:dashboard')
            else:
                messages.error(request, 'Você não tem permissão para acessar este sistema. Entre em contato com o administrador para solicitar acesso.')
        else:
            messages.error(request, 'Email ou senha incorretos. Verifique suas credenciais e tente novamente.')
    
    return render(request, 'carga_org_lot/login.html')


def dashboard_view(request):
    """Dashboard principal do Carga Org Lot"""
    # Verifica se o usuário está autenticado
    if 'user_id' not in request.session:
        messages.warning(request, 'Por favor, faça login para acessar o sistema.')
        return redirect('carga_org_lot:login')
    
    try:
        # Busca informações do usuário
        user = User.objects.get(id=request.session['user_id'])
        
        # Verifica se ainda tem permissão
        has_permission = UserRole.objects.filter(
            user=user,
            aplicacao__codigointerno='CARGA_ORG_LOT'
        ).exists()
        
        if not has_permission:
            request.session.flush()
            messages.error(request, 'Sua permissão foi revogada. Entre em contato com o administrador.')
            return redirect('carga_org_lot:login')
        
        # Busca roles do usuário para esta aplicação
        user_roles = UserRole.objects.filter(
            user=user,
            aplicacao__codigointerno='CARGA_ORG_LOT'
        ).select_related('role', 'aplicacao')
        
        context = {
            'user_name': request.session.get('user_name'),
            'user_email': request.session.get('user_email'),
            'user_roles': user_roles,
            'access_token': request.session.get('access_token'),
        }
        
        return render(request, 'carga_org_lot/dashboard.html', context)
        
    except User.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Usuário não encontrado. Faça login novamente.')
        return redirect('carga_org_lot:login')


def logout_view(request):
    """Logout do usuário"""
    user_name = request.session.get('user_name', 'Usuário')
    request.session.flush()
    messages.success(request, f'Até logo, {user_name}! Logout realizado com sucesso.')
    return redirect('carga_org_lot:login')
    