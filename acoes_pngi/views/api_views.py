from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from accounts.models import UserRole
from ..models import Eixo, SituacaoAcao, VigenciaPNGI
import json


def check_acoes_pngi_access(user):
    """Verifica se usuário tem acesso ao Ações PNGI"""
    if not user.is_authenticated:
        return False
    return UserRole.objects.filter(
        user=user,
        aplicacao__codigointerno='ACOES_PNGI'
    ).exists()


@require_http_methods(["GET"])
def api_acoes_pngi_dashboard(request):
    """
    GET /api/acoes_pngi
    Retorna dados do dashboard Ações PNGI
    """
    if not check_acoes_pngi_access(request.user):
        return JsonResponse({
            'ok': False,
            'message': 'Você não tem permissão para acessar esta aplicação.'
        }, status=403)
    
    user = request.user
    user_role = UserRole.objects.filter(
        user=user,
        aplicacao__codigointerno='ACOES_PNGI'
    ).select_related('role', 'aplicacao').first()
    
    # Busca estatísticas
    total_eixos = Eixo.objects.count()
    total_situacoes = SituacaoAcao.objects.count()
    total_vigencias = VigenciaPNGI.objects.count()
    vigencias_ativas = VigenciaPNGI.objects.filter(isvigenciaativa=True).count()
    
    # Busca eixos
    eixos = Eixo.objects.all()[:10]
    eixos_list = [{
        'id': e.ideixo,
        'alias': e.stralias,
        'descricao': e.strdescricaoeixo
    } for e in eixos]
    
    # Vigência atual
    vigencia_atual = VigenciaPNGI.objects.filter(isvigenciaativa=True).first()
    vigencia_data = None
    if vigencia_atual:
        vigencia_data = {
            'id': vigencia_atual.idvigenciapngi,
            'descricao': vigencia_atual.strdescricaovigenciapngi,
            'dataInicio': vigencia_atual.datiniciovigencia.isoformat(),
            'dataFim': vigencia_atual.datfinalvigencia.isoformat(),
            'duracaoDias': vigencia_atual.duracao_dias
        }
    
    return JsonResponse({
        'ok': True,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        },
        'role': {
            'codigo': user_role.role.codigoperfil,
            'nome': user_role.role.nomeperfil
        },
        'aplicacao': {
            'codigo': user_role.aplicacao.codigointerno,
            'nome': user_role.aplicacao.nomeaplicacao
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
    """
    GET /api/acoes_pngi/eixos
    Lista todos os eixos
    """
    if not check_acoes_pngi_access(request.user):
        return JsonResponse({
            'ok': False,
            'message': 'Você não tem permissão para acessar esta aplicação.'
        }, status=403)
    
    eixos = Eixo.objects.all()
    eixos_list = [{
        'id': e.ideixo,
        'alias': e.stralias,
        'descricao': e.strdescricaoeixo,
        'createdAt': e.created_at.isoformat(),
        'updatedAt': e.updated_at.isoformat()
    } for e in eixos]
    
    return JsonResponse({
        'ok': True,
        'eixos': eixos_list
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_acoes_pngi_eixos_create(request):
    """
    POST /api/acoes_pngi/eixos
    Cria novo eixo
    """
    if not check_acoes_pngi_access(request.user):
        return JsonResponse({
            'ok': False,
            'message': 'Você não tem permissão para acessar esta aplicação.'
        }, status=403)
    
    try:
        data = json.loads(request.body)
        alias = data.get('alias', '').strip().upper()
        descricao = data.get('descricao', '').strip()
        
        if not alias or not descricao:
            return JsonResponse({
                'ok': False,
                'message': 'Alias e descrição são obrigatórios.'
            }, status=400)
        
        # Verifica se alias já existe
        if Eixo.objects.filter(stralias=alias).exists():
            return JsonResponse({
                'ok': False,
                'message': f'Eixo com alias "{alias}" já existe.'
            }, status=400)
        
        # Cria eixo
        eixo = Eixo.objects.create(
            stralias=alias,
            strdescricaoeixo=descricao
        )
        
        return JsonResponse({
            'ok': True,
            'eixo': {
                'id': eixo.ideixo,
                'alias': eixo.stralias,
                'descricao': eixo.strdescricaoeixo
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'ok': False,
            'message': 'JSON inválido.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'ok': False,
            'message': f'Erro ao criar eixo: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def api_acoes_pngi_vigencias(request):
    """
    GET /api/acoes_pngi/vigencias
    Lista todas as vigências
    """
    if not check_acoes_pngi_access(request.user):
        return JsonResponse({
            'ok': False,
            'message': 'Você não tem permissão para acessar esta aplicação.'
        }, status=403)
    
    vigencias = VigenciaPNGI.objects.all()
    vigencias_list = [{
        'id': v.idvigenciapngi,
        'descricao': v.strdescricaovigenciapngi,
        'dataInicio': v.datiniciovigencia.isoformat(),
        'dataFim': v.datfinalvigencia.isoformat(),
        'ativa': v.isvigenciaativa,
        'vigente': v.esta_vigente,
        'duracaoDias': v.duracao_dias
    } for v in vigencias]
    
    return JsonResponse({
        'ok': True,
        'vigencias': vigencias_list
    })