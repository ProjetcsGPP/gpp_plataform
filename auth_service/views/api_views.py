"""
APIs REST consolidadas para autenticação
Suporta tanto JWT (stateless para Next.js) quanto Session (stateful para Django)
"""

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User, UserRole, Attribute
import json


# =============================================================================
# JWT TOKEN AUTHENTICATION (para Next.js - Stateless)
# =============================================================================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer customizado que adiciona permissions, roles e attributes ao JWT
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Busca todas as permissões do usuário
        permissions = User.get_all_permissions(user)
        
        # Claims básicos
        token['useremail'] = user.email
        token['username'] = user.name
        token['permissions'] = list(permissions)
        
        # Roles RBAC por aplicação
        roles = list(
            UserRole.objects.filter(user=user).values(
                'aplicacao__codigointerno', 
                'role__codigoperfil',
                'role__nomeperfil'
            )
        )
        token['roles'] = roles
        
        # Atributos ABAC
        attrs = list(
            Attribute.objects.filter(user=user).values(
                'aplicacao__codigointerno', 
                'key', 
                'value'
            )
        )
        token['attrs'] = attrs
        
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/v1/auth/token/
    
    Body: { "username": "email@example.com", "password": "senha" }
    Response: { "access": "...", "refresh": "..." }
    
    Usa JWT para autenticação stateless (recomendado para Next.js)
    """
    serializer_class = CustomTokenObtainPairSerializer


# =============================================================================
# SESSION AUTHENTICATION (para compatibilidade - Stateful)
# =============================================================================

@csrf_exempt
@require_http_methods(["POST"])
def session_login(request):
    """
    POST /api/v1/auth/session/login/
    
    Body: { "email": "...", "password": "..." }
    Response: { "ok": true, "user": {...}, "applications": [...], "csrfToken": "..." }
    
    Autentica usuário e cria sessão Django (stateful)
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return JsonResponse({
                'ok': False,
                'message': 'Email e senha são obrigatórios.'
            }, status=400)
        
        # Verifica se usuário existe
        try:
            user_exists = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({
                'ok': False,
                'message': 'Usuário não encontrado. Verifique o email informado.'
            }, status=404)
        
        # Verifica se usuário está ativo
        if not user_exists.is_active:
            return JsonResponse({
                'ok': False,
                'message': 'Usuário inativo. Entre em contato com o administrador.'
            }, status=403)
        
        # Autentica
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Verifica se tem acesso a pelo menos uma aplicação
            user_roles = UserRole.objects.filter(user=user).select_related('aplicacao', 'role')
            
            if not user_roles.exists():
                return JsonResponse({
                    'ok': False,
                    'message': 'Usuário sem permissão de acesso a nenhuma aplicação.'
                }, status=403)
            
            # Faz login (cria sessão)
            login(request, user)
            
            # Gera CSRF token
            csrf_token = get_token(request)
            
            # Retorna dados do usuário e aplicações
            apps_dict = {}
            for ur in user_roles:
                app_code = ur.aplicacao.codigointerno
                if app_code not in apps_dict:
                    apps_dict[app_code] = {
                        'codigo': ur.aplicacao.codigointerno,
                        'nome': ur.aplicacao.nomeaplicacao,
                        'url': ur.aplicacao.base_url,
                        'roles': []
                    }
                apps_dict[app_code]['roles'].append({
                    'codigo': ur.role.codigoperfil,
                    'nome': ur.role.nomeperfil
                })
            
            return JsonResponse({
                'ok': True,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                },
                'applications': list(apps_dict.values()),
                'csrfToken': csrf_token
            })
        else:
            return JsonResponse({
                'ok': False,
                'message': 'Senha incorreta. Tente novamente.'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'ok': False,
            'message': 'JSON inválido.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'ok': False,
            'message': f'Erro no servidor: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
def session_logout(request):
    """
    POST /api/v1/auth/session/logout/
    
    Response: { "ok": true, "message": "..." }
    
    Encerra sessão do usuário
    """
    logout(request)
    return JsonResponse({
        'ok': True, 
        'message': 'Logout realizado com sucesso.'
    })


@require_http_methods(["GET"])
def session_me(request):
    """
    GET /api/v1/auth/session/me/
    
    Response: { "ok": true, "user": {...}, "applications": [...] }
    
    Retorna dados do usuário autenticado via sessão
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            'ok': False,
            'message': 'Não autenticado.'
        }, status=401)
    
    user = request.user
    user_roles = UserRole.objects.filter(user=user).select_related('aplicacao', 'role')
    
    apps_dict = {}
    for ur in user_roles:
        app_code = ur.aplicacao.codigointerno
        if app_code not in apps_dict:
            apps_dict[app_code] = {
                'codigo': ur.aplicacao.codigointerno,
                'nome': ur.aplicacao.nomeaplicacao,
                'url': ur.aplicacao.base_url,
                'roles': []
            }
        apps_dict[app_code]['roles'].append({
            'codigo': ur.role.codigoperfil,
            'nome': ur.role.nomeperfil
        })
    
    return JsonResponse({
        'ok': True,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        },
        'applications': list(apps_dict.values())
    })


@require_http_methods(["GET"])
def get_csrf_token(request):
    """
    GET /api/v1/auth/csrf/
    
    Response: { "csrfToken": "..." }
    
    Retorna CSRF token para uso em requisições subsequentes
    """
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})