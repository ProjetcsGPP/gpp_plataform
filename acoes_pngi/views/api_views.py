from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.db import connection
import json
import requests
from accounts.models import UserRole
from ..models import Eixo, SituacaoAcao, VigenciaPNGI
from rest_framework_simplejwt.authentication import JWTAuthentication


User = get_user_model()


def check_acoes_pngi_access(user):
    """Verifica se usuário tem acesso ao Ações PNGI via UserRole"""
    if not user.is_authenticated:
        return False
    return UserRole.objects.filter(
        user=user,
        aplicacao__codigointerno='ACOES_PNGI'
    ).exists()


def criar_usuario_pngi(cpf, nome_completo):
    """
    Cria usuário PNGI via API Portal (padrão existente)
    Retorna token PNGI para uso local
    """
    try:
        # Chama API Portal para criar usuário + atribuir role PNGI
        portal_url = "http://localhost:8000/accounts/api/gestao/usuarios/"  # Ajustar URL
        admin_token = "SEU_TOKEN_ADMIN_PORTAL"  # Token admin portal
        
        response = requests.post(
            portal_url,
            json={
                'cpf': cpf,
                'nome': nome_completo,
                'role_codigo_aplicacao': 'GESTORPNGI',  # Role PNGI
                'aplicacao_destino': 'ACOES_PNGI'
            },
            headers={
                'Authorization': f'Bearer {admin_token}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            return {
                'success': True,
                'user_id': data['userid'],
                'access_token_pngi': data['access_token'],
                'message': 'Usuário PNGI criado com sucesso'
            }
        else:
            return {
                'success': False,
                'message': f'Erro portal: {response.status_code} - {response.text}'
            }
            
    except requests.RequestException as e:
        return {
            'success': False,
            'message': f'Erro conexão portal: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Erro inesperado: {str(e)}'
        }


@csrf_exempt
@require_http_methods(["POST"])
def api_acoes_pngi_criar_usuario(request):
    """
    POST /api/acoes_pngi/usuario/
    Cria usuário PNGI via API Portal (padrão)
    """
    try:
        data = json.loads(request.body)
        cpf = data.get('cpf', '').strip()
        nome = data.get('nome', '').strip()
        
        if not cpf or not nome:
            return JsonResponse({
                'ok': False,
                'message': 'CPF e nome são obrigatórios.'
            }, status=400)
        
        # ✅ Chama função padrão
        result = criar_usuario_pngi(cpf, nome)
        
        return JsonResponse(result, status=201 if result['success'] else 400)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'ok': False,
            'message': 'JSON inválido.'
        }, status=400)


@require_http_methods(["GET"])
def api_acoes_pngi_dashboard(request):
    """
    GET /api/acoes_pngi/
    Dashboard (token acoespngiapp)
    """
    if not check_acoes_pngi_access(request.user):
        return JsonResponse({
            'ok': False,
            'message': 'Você não tem permissão para Ações PNGI.'
        }, status=403)
    
    user = request.user
    user_role = UserRole.objects.filter(
        user=user, aplicacao__codigointerno='ACOES_PNGI'
    ).select_related('role', 'aplicacao').first()
    
    total_eixos = Eixo.objects.count()
    total_situacoes = SituacaoAcao.objects.count()
    total_vigencias = VigenciaPNGI.objects.count()
    vigencias_ativas = VigenciaPNGI.objects.filter(isvigenciaativa=True).count()
    
    eixos = Eixo.objects.all()[:10]
    eixos_list = [{
        'id': e.ideixo,
        'alias': e.stralias,
        'descricao': e.strdescricaoeixo
    } for e in eixos]
    
    vigencia_atual = VigenciaPNGI.objects.filter(isvigenciaativa=True).first()
    vigencia_data = None
    if vigencia_atual:
        vigencia_data = {
            'id': vigencia_atual.idvigenciapngi,
            'descricao': vigencia_atual.strdescricaovigenciapngi,
            'dataInicio': vigencia_atual.datiniciovigencia.isoformat(),
            'dataFim': vigencia_atual.datfinalvigencia.isoformat(),
            'duracaoDias': getattr(vigencia_atual, 'duracao_dias', 0)
        }
    
    return JsonResponse({
        'ok': True,
        'user': {
            'id': user.id,
            'name': user.name or f"{user.first_name} {user.last_name}".strip(),
            'email': user.email
        },
        'role': {
            'codigo': getattr(user_role, 'role', {}).codigoperfil if user_role else None,
            'nome': getattr(user_role, 'role', {}).nomeperfil if user_role else None
        },
        'aplicacao': {
            'codigo': 'ACOES_PNGI',
            'nome': getattr(user_role, 'aplicacao', {}).nomeaplicacao if user_role else 'Ações PNGI'
        },
        'stats': {
            'totalEixos': total_eixos,
            'totalSituacoes': total_situacoes,
            'totalVigencias': total_vigencias,
            'vigenciasAtivas': vigencias_ativas
        },
        'eixos': eixos_list,
        'vigenciaAtual': vigencia_data
    })


@require_http_methods(["GET"])
def api_acoes_pngi_eixos(request):
    """GET /api/acoes_pngi/eixos"""
    if not check_acoes_pngi_access(request.user):
        return JsonResponse({'ok': False, 'message': 'Sem permissão.'}, status=403)
    
    eixos = Eixo.objects.all()
    eixos_list = [{
        'id': e.ideixo,
        'alias': e.stralias,
        'descricao': e.strdescricaoeixo,
        'createdAt': getattr(e, 'created_at', None) and e.created_at.isoformat(),
        'updatedAt': getattr(e, 'updated_at', None) and e.updated_at.isoformat()
    } for e in eixos]
    
    return JsonResponse({'ok': True, 'eixos': eixos_list})


@csrf_exempt
@require_http_methods(["POST"])
def api_acoes_pngi_eixos_create(request):
    """
    POST /api/acoes_pngi/eixos
    Cria eixo via PROCEDURE (acoespngiapp EXECUTE)
    """
    if not check_acoes_pngi_access(request.user):
        return JsonResponse({'ok': False, 'message': 'Sem permissão.'}, status=403)
    
    try:
        data = json.loads(request.body)
        alias = data.get('alias', '').strip().upper()
        descricao = data.get('descricao', '').strip()
        
        if not alias or not descricao:
            return JsonResponse({'ok': False, 'message': 'Alias e descrição obrigatórios.'}, status=400)
        
        if Eixo.objects.filter(stralias=alias).exists():
            return JsonResponse({'ok': False, 'message': f'Alias "{alias}" existe.'}, status=400)
        
        # ✅ Usa PROCEDURE (GRANT EXECUTE acoespngiapp)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT acoes_pngi_create_eixo(%s, %s)",
                [alias, descricao]
            )
            eixo_id = cursor.fetchone()[0]
        
        eixo = Eixo.objects.get(ideixo=eixo_id)
        
        return JsonResponse({
            'ok': True,
            'eixo': {
                'id': eixo.ideixo,
                'alias': eixo.stralias,
                'descricao': eixo.strdescricaoeixo
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'ok': False, 'message': f'Erro: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def api_acoes_pngi_vigencias(request):
    """GET /api/acoes_pngi/vigencias"""
    if not check_acoes_pngi_access(request.user):
        return JsonResponse({'ok': False, 'message': 'Sem permissão.'}, status=403)
    
    vigencias = VigenciaPNGI.objects.all()
    vigencias_list = [{
        'id': v.idvigenciapngi,
        'descricao': v.strdescricaovigenciapngi,
        'dataInicio': v.datiniciovigencia.isoformat(),
        'dataFim': v.datfinalvigencia.isoformat(),
        'ativa': v.isvigenciaativa,
        'vigente': getattr(v, 'esta_vigente', False),
        'duracaoDias': getattr(v, 'duracao_dias', 0)
    } for v in vigencias]
    
    return JsonResponse({'ok': True, 'vigencias': vigencias_list})
