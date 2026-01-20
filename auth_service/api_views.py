from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from accounts.models import User, UserRole
import json


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """
    POST /api/auth/login
    Autentica usuário e cria sessão
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
                'applications': list(apps_dict.values())
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
def api_logout(request):
    """
    POST /api/auth/logout
    Encerra sessão do usuário
    """
    logout(request)
    return JsonResponse({'ok': True, 'message': 'Logout realizado com sucesso.'})


@require_http_methods(["GET"])
def api_me(request):
    """
    GET /api/auth/me
    Retorna dados do usuário autenticado
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