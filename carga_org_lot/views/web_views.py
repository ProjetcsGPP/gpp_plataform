# carga_org_lot/views/web_views.py
"""
Web Views para Carga Org/Lot.
Views tradicionais Django para renderizar páginas HTML.
"""

from functools import wraps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json

from accounts.models import UserRole, Aplicacao, User
from ..models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblOrgaoUnidade,
    TblOrganogramaJson,
    TblLotacaoVersao,
    TblLotacao,
    TblLotacaoJsonOrgao,
    TblLotacaoInconsistencia,
    TblTokenEnvioCarga,
    TblCargaPatriarca,
    TblDetalheStatusCarga,
    TblStatusProgresso,
    TblStatusTokenEnvioCarga,
    TblStatusCarga,
    TblTipoCarga,
)


# ============================================
# AUTENTICAÇÃO
# ============================================

def carga_login(request):
    """
    GET/POST /carga_org_lot/login/
    
    Página de login do Carga Org/Lot.
    Valida usuário, senha e permissão para esta aplicação.
    """
    if request.user.is_authenticated:
        # Verifica se já tem acesso ao carga_org_lot
        has_access = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='CARGA_ORG_LOT'
        ).exists()
        
        if has_access:
            return redirect('carga_org_lot_web:dashboard')
        else:
            messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
            logout(request)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validação de campos vazios
        if not email or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'carga_org_lot/login.html')
        
        # Verifica se usuário existe
        try:
            user_exists = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado. Verifique o email informado.')
            return render(request, 'carga_org_lot/login.html')
        
        # Verifica se usuário está ativo
        if not user_exists.is_active:
            messages.error(request, 'Usuário inativo. Entre em contato com o administrador.')
            return render(request, 'carga_org_lot/login.html')
        
        # Autentica usuário
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Verifica se usuário tem acesso à aplicação CARGA_ORG_LOT
            try:
                app_carga = Aplicacao.objects.get(codigointerno='CARGA_ORG_LOT')
                user_role = UserRole.objects.filter(
                    user=user,
                    aplicacao=app_carga
                ).select_related('role').first()
                
                if not user_role:
                    messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
                    return render(request, 'carga_org_lot/login.html')
                
                # Login bem-sucedido
                login(request, user)
                messages.success(request, f'Bem-vindo(a) ao Carga Org/Lot, {user.name}!')
                return redirect('carga_org_lot_web:dashboard')
                
            except Aplicacao.DoesNotExist:
                messages.error(request, 'Aplicação não encontrada no sistema.')
                return render(request, 'carga_org_lot/login.html')
        else:
            messages.error(request, 'Senha incorreta. Tente novamente.')
            return render(request, 'carga_org_lot/login.html')
    
    return render(request, 'carga_org_lot/login.html')


def carga_logout(request):
    """
    GET /carga_org_lot/logout/
    
    Logout do Carga Org/Lot.
    """
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('carga_org_lot_web:login')


# ============================================
# DECORADOR DE VERIFICAÇÃO DE ACESSO
# ============================================

def carga_org_lot_required(view_func):
    """
    Decorador que verifica se usuário tem acesso ao Carga Org/Lot.
    Combina @login_required + verificação de role.
    
    CORREÇÃO: Usa @wraps para preservar metadados da view original.
    Usa @login_required nativo do Django para garantir compatibilidade.
    """
    @wraps(view_func)
    @login_required(login_url='/carga_org_lot/login/')
    def wrapper(request, *args, **kwargs):
        # Verifica se usuário tem acesso à aplicação
        has_access = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='CARGA_ORG_LOT'
        ).exists()
        
        if not has_access:
            messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
            logout(request)
            return redirect('carga_org_lot_web:login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


# ============================================
# DASHBOARD
# ============================================

@carga_org_lot_required
def carga_dashboard(request):
    """
    GET /carga_org_lot/
    
    Dashboard principal com estatísticas gerais.
    """
    user = request.user
    
    # Buscar role do usuário
    app_carga = Aplicacao.objects.get(codigointerno='CARGA_ORG_LOT')
    user_role = UserRole.objects.filter(
        user=user,
        aplicacao=app_carga
    ).select_related('role').first()
    
    # Estatísticas gerais
    stats = {
        'patriarcas': {
            'total': TblPatriarca.objects.count(),
            'por_status': TblPatriarca.objects.values(
                'id_status_progresso__str_descricao'
            ).annotate(count=Count('id_patriarca'))
        },
        'organogramas': {
            'total': TblOrganogramaVersao.objects.count(),
            'ativos': TblOrganogramaVersao.objects.filter(flg_ativo=True).count(),
        },
        'lotacoes': {
            'total': TblLotacao.objects.count(),
            'validas': TblLotacao.objects.filter(flg_valido=True).count(),
            'invalidas': TblLotacao.objects.filter(flg_valido=False).count(),
        },
        'cargas_recentes': TblCargaPatriarca.objects.select_related(
            'id_patriarca',
            'id_tipo_carga',
            'id_status_carga'
        ).order_by('-dat_data_hora_inicio')[:10]
    }
    
    context = {
        'user': user,
        'role': user_role.role,
        'aplicacao': app_carga,
        'stats': stats,
    }
    
    return render(request, 'carga_org_lot/dashboard.html', context)


# ============================================
# PATRIARCAS
# ============================================

@carga_org_lot_required
def patriarca_list(request):
    """
    GET /carga_org_lot/patriarcas/
    
    Lista todos os patriarcas com filtros e paginação.
    """
    # Filtros
    search = request.GET.get('search', '')
    status_id = request.GET.get('status', '')
    
    patriarcas = TblPatriarca.objects.select_related(
        'id_status_progresso',
        'id_usuario_criacao'
    ).all()
    
    # Aplicar filtros
    if search:
        patriarcas = patriarcas.filter(
            Q(str_sigla_patriarca__icontains=search) |
            Q(str_nome__icontains=search)
        )
    
    if status_id:
        patriarcas = patriarcas.filter(id_status_progresso_id=status_id)
    
    # Ordenação
    patriarcas = patriarcas.order_by('-dat_criacao')
    
    # Paginação
    paginator = Paginator(patriarcas, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Lista de status para filtro
    status_list = TblStatusProgresso.objects.all()
    
    context = {
        'page_obj': page_obj,
        'status_list': status_list,
        'search': search,
        'status_id': status_id,
    }
    
    return render(request, 'carga_org_lot/patriarca_list.html', context)


@carga_org_lot_required
def patriarca_detail(request, patriarca_id):
    """
    GET /carga_org_lot/patriarcas/{id}/
    
    Detalhes de um patriarca específico.
    """
    patriarca = get_object_or_404(
        TblPatriarca.objects.select_related(
            'id_status_progresso',
            'id_usuario_criacao'
        ),
        id_patriarca=patriarca_id
    )
    
    # Organogramas do patriarca
    organogramas = TblOrganogramaVersao.objects.filter(
        id_patriarca=patriarca
    ).order_by('-dat_processamento')[:5]
    
    # Versões de lotação
    lotacoes = TblLotacaoVersao.objects.filter(
        id_patriarca=patriarca
    ).order_by('-dat_processamento')[:5]
    
    # Cargas recentes
    cargas = TblCargaPatriarca.objects.filter(
        id_patriarca=patriarca
    ).select_related(
        'id_tipo_carga',
        'id_status_carga'
    ).order_by('-dat_data_hora_inicio')[:10]
    
    context = {
        'patriarca': patriarca,
        'organogramas': organogramas,
        'lotacoes': lotacoes,
        'cargas': cargas,
    }
    
    return render(request, 'carga_org_lot/patriarca_detail.html', context)


# ============================================
# ORGANOGRAMAS
# ============================================

@carga_org_lot_required
def organograma_list(request):
    """
    GET /carga_org_lot/organogramas/
    
    Lista versões de organogramas.
    """
    patriarca_id = request.GET.get('patriarca', '')
    apenas_ativos = request.GET.get('ativos', '')
    
    organogramas = TblOrganogramaVersao.objects.select_related('id_patriarca').all()
    
    if patriarca_id:
        organogramas = organogramas.filter(id_patriarca_id=patriarca_id)
    
    if apenas_ativos == 'true':
        organogramas = organogramas.filter(flg_ativo=True)
    
    organogramas = organogramas.order_by('-dat_processamento')
    
    # Paginação
    paginator = Paginator(organogramas, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Lista de patriarcas para filtro
    patriarcas = TblPatriarca.objects.all()
    
    context = {
        'page_obj': page_obj,
        'patriarcas': patriarcas,
        'patriarca_id': patriarca_id,
        'apenas_ativos': apenas_ativos,
    }
    
    return render(request, 'carga_org_lot/organograma_list.html', context)


@carga_org_lot_required
def organograma_detail(request, organograma_id):
    """
    GET /carga_org_lot/organogramas/{id}/
    
    Detalhes de uma versão de organograma.
    """
    organograma = get_object_or_404(
        TblOrganogramaVersao.objects.select_related('id_patriarca'),
        id_organograma_versao=organograma_id
    )
    
    # Órgãos raiz (sem pai) para construir hierarquia
    orgaos_raiz = TblOrgaoUnidade.objects.filter(
        id_organograma_versao=organograma,
        id_orgao_unidade_pai__isnull=True
    ).prefetch_related('tblorgaounidade_set')
    
    # Estatísticas
    total_orgaos = TblOrgaoUnidade.objects.filter(
        id_organograma_versao=organograma
    ).count()
    
    context = {
        'organograma': organograma,
        'orgaos_raiz': orgaos_raiz,
        'total_orgaos': total_orgaos,
    }
    
    return render(request, 'carga_org_lot/organograma_detail.html', context)


@carga_org_lot_required
def organograma_hierarquia_json(request, organograma_id):
    """
    GET /carga_org_lot/organogramas/{id}/hierarquia/json/
    
    Retorna hierarquia em formato JSON para visualização em árvore.
    """
    organograma = get_object_or_404(TblOrganogramaVersao, id_organograma_versao=organograma_id)
    
    def build_tree(orgao):
        """Constrói árvore recursivamente"""
        children = TblOrgaoUnidade.objects.filter(id_orgao_unidade_pai=orgao)
        return {
            'id': orgao.id_orgao_unidade,
            'sigla': orgao.str_sigla,
            'nome': orgao.str_nome,
            'nivel': orgao.int_nivel_hierarquia,
            'children': [build_tree(child) for child in children]
        }
    
    # Buscar órgãos raiz
    orgaos_raiz = TblOrgaoUnidade.objects.filter(
        id_organograma_versao=organograma,
        id_orgao_unidade_pai__isnull=True
    )
    
    hierarquia = [build_tree(orgao) for orgao in orgaos_raiz]
    
    return JsonResponse({
        'organograma_id': organograma.id_organograma_versao,
        'patriarca': {
            'id': organograma.id_patriarca.id_patriarca,
            'sigla': organograma.id_patriarca.str_sigla_patriarca,
            'nome': organograma.id_patriarca.str_nome,
        },
        'hierarquia': hierarquia
    })


# ============================================
# LOTAÇÕES
# ============================================

@carga_org_lot_required
def lotacao_list(request):
    """
    GET /carga_org_lot/lotacoes/
    
    Lista versões de lotações.
    """
    patriarca_id = request.GET.get('patriarca', '')
    
    lotacoes = TblLotacaoVersao.objects.select_related(
        'id_patriarca',
        'id_organograma_versao'
    ).all()
    
    if patriarca_id:
        lotacoes = lotacoes.filter(id_patriarca_id=patriarca_id)
    
    lotacoes = lotacoes.order_by('-dat_processamento')
    
    # Paginação
    paginator = Paginator(lotacoes, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Lista de patriarcas para filtro
    patriarcas = TblPatriarca.objects.all()
    
    context = {
        'page_obj': page_obj,
        'patriarcas': patriarcas,
        'patriarca_id': patriarca_id,
    }
    
    return render(request, 'carga_org_lot/lotacao_list.html', context)


@carga_org_lot_required
def lotacao_detail(request, lotacao_versao_id):
    """
    GET /carga_org_lot/lotacoes/{id}/
    
    Detalhes de uma versão de lotação.
    """
    lotacao_versao = get_object_or_404(
        TblLotacaoVersao.objects.select_related(
            'id_patriarca',
            'id_organograma_versao'
        ),
        id_lotacao_versao=lotacao_versao_id
    )
    
    # Filtros para registros de lotação
    cpf_search = request.GET.get('cpf', '')
    valido_filter = request.GET.get('valido', '')
    
    # Registros de lotação
    lotacoes = TblLotacao.objects.filter(
        id_lotacao_versao=lotacao_versao
    ).select_related('id_orgao_lotacao', 'id_unidade_lotacao')
    
    if cpf_search:
        lotacoes = lotacoes.filter(str_cpf__icontains=cpf_search)
    
    if valido_filter == 'true':
        lotacoes = lotacoes.filter(flg_valido=True)
    elif valido_filter == 'false':
        lotacoes = lotacoes.filter(flg_valido=False)
    
    # Paginação de lotações
    paginator = Paginator(lotacoes, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    stats = {
        'total': TblLotacao.objects.filter(id_lotacao_versao=lotacao_versao).count(),
        'validos': TblLotacao.objects.filter(
            id_lotacao_versao=lotacao_versao,
            flg_valido=True
        ).count(),
        'invalidos': TblLotacao.objects.filter(
            id_lotacao_versao=lotacao_versao,
            flg_valido=False
        ).count(),
        'inconsistencias': TblLotacaoInconsistencia.objects.filter(
            id_lotacao__id_lotacao_versao=lotacao_versao
        ).count()
    }
    
    context = {
        'lotacao_versao': lotacao_versao,
        'page_obj': page_obj,
        'stats': stats,
        'cpf_search': cpf_search,
        'valido_filter': valido_filter,
    }
    
    return render(request, 'carga_org_lot/lotacao_detail.html', context)


@carga_org_lot_required
def lotacao_inconsistencias(request, lotacao_versao_id):
    """
    GET /carga_org_lot/lotacoes/{id}/inconsistencias/
    
    Lista inconsistências de uma versão de lotação.
    """
    lotacao_versao = get_object_or_404(TblLotacaoVersao, id_lotacao_versao=lotacao_versao_id)
    
    inconsistencias = TblLotacaoInconsistencia.objects.filter(
        id_lotacao__id_lotacao_versao=lotacao_versao
    ).select_related('id_lotacao', 'id_lotacao__id_orgao_lotacao').order_by('-dat_registro')
    
    # Paginação
    paginator = Paginator(inconsistencias, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'lotacao_versao': lotacao_versao,
        'page_obj': page_obj,
    }
    
    return render(request, 'carga_org_lot/lotacao_inconsistencias.html', context)


# ============================================
# CARGAS
# ============================================

@carga_org_lot_required
def carga_list(request):
    """
    GET /carga_org_lot/cargas/
    
    Lista todas as cargas com filtros.
    """
    patriarca_id = request.GET.get('patriarca', '')
    tipo_id = request.GET.get('tipo', '')
    status_id = request.GET.get('status', '')
    
    cargas = TblCargaPatriarca.objects.select_related(
        'id_patriarca',
        'id_tipo_carga',
        'id_status_carga',
        'id_token_envio_carga'
    ).all()
    
    if patriarca_id:
        cargas = cargas.filter(id_patriarca_id=patriarca_id)
    
    if tipo_id:
        cargas = cargas.filter(id_tipo_carga_id=tipo_id)
    
    if status_id:
        cargas = cargas.filter(id_status_carga_id=status_id)
    
    cargas = cargas.order_by('-dat_data_hora_inicio')
    
    # Paginação
    paginator = Paginator(cargas, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Listas para filtros
    patriarcas = TblPatriarca.objects.all()
    tipos_carga = TblTipoCarga.objects.all()
    status_carga = TblStatusCarga.objects.all()
    
    context = {
        'page_obj': page_obj,
        'patriarcas': patriarcas,
        'tipos_carga': tipos_carga,
        'status_carga': status_carga,
        'patriarca_id': patriarca_id,
        'tipo_id': tipo_id,
        'status_id': status_id,
    }
    
    return render(request, 'carga_org_lot/carga_list.html', context)


@carga_org_lot_required
def carga_detail(request, carga_id):
    """
    GET /carga_org_lot/cargas/{id}/
    
    Detalhes de uma carga específica com timeline.
    """
    carga = get_object_or_404(
        TblCargaPatriarca.objects.select_related(
            'id_patriarca',
            'id_tipo_carga',
            'id_status_carga',
            'id_token_envio_carga',
            'id_token_envio_carga__id_status_token_envio_carga'
        ),
        id_carga_patriarca=carga_id
    )
    
    # Timeline de status
    timeline = TblDetalheStatusCarga.objects.filter(
        id_carga_patriarca=carga
    ).select_related('id_status_carga').order_by('dat_registro')
    
    context = {
        'carga': carga,
        'timeline': timeline,
    }
    
    return render(request, 'carga_org_lot/carga_detail.html', context)


# ============================================
# UPLOAD
# ============================================

@carga_org_lot_required
def upload_page(request):
    """
    GET /carga_org_lot/upload/
    
    Página de upload de arquivos (organograma e lotação).
    """
    patriarcas = TblPatriarca.objects.filter(
        id_status_progresso__in=[1, 2, 3]  # Apenas patriarcas ativos
    ).order_by('str_sigla_patriarca')
    
    context = {
        'patriarcas': patriarcas,
    }
    
    return render(request, 'carga_org_lot/upload.html', context)


@carga_org_lot_required
@require_http_methods(["POST"])
def upload_organograma_handler(request):
    """
    POST /carga_org_lot/upload/organograma/
    
    Processa upload de arquivo de organograma.
    """
    # TODO: Implementar lógica de processamento
    messages.info(request, 'Processamento de organograma em desenvolvimento.')
    return redirect('carga_org_lot_web:upload')


@carga_org_lot_required
@require_http_methods(["POST"])
def upload_lotacao_handler(request):
    """
    POST /carga_org_lot/upload/lotacao/
    
    Processa upload de arquivo de lotação.
    """
    # TODO: Implementar lógica de processamento
    messages.info(request, 'Processamento de lotação em desenvolvimento.')
    return redirect('carga_org_lot_web:upload')


# ============================================
# BUSCA/AUTOCOMPLETE
# ============================================

@carga_org_lot_required
def search_orgao_ajax(request):
    """
    GET /carga_org_lot/ajax/search-orgao/?q=termo&patriarca_id=1
    
    Busca órgãos por sigla ou nome (para autocomplete).
    """
    query = request.GET.get('q', '')
    patriarca_id = request.GET.get('patriarca_id', None)
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    orgaos = TblOrgaoUnidade.objects.filter(
        Q(str_sigla__icontains=query) | Q(str_nome__icontains=query),
        flg_ativo=True
    )
    
    if patriarca_id:
        orgaos = orgaos.filter(id_patriarca_id=patriarca_id)
    
    orgaos = orgaos.select_related('id_patriarca')[:20]
    
    results = [
        {
            'id': o.id_orgao_unidade,
            'sigla': o.str_sigla,
            'nome': o.str_nome,
            'patriarca': o.id_patriarca.str_sigla_patriarca,
            'nivel': o.int_nivel_hierarquia
        }
        for o in orgaos
    ]
    
    return JsonResponse({'results': results})
