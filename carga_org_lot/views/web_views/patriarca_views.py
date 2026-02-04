"""
Views de Patriarca para Carga Org/Lot
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from ...models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblLotacaoVersao,
    TblCargaPatriarca,
    TblStatusProgresso,
)
from ...forms import PatriarcaForm
from .auth_views import carga_org_lot_required


@carga_org_lot_required
def patriarca_list(request):
    """
    GET /carga_org_lot/patriarcas/
    
    Lista todos os patriarcas com filtros, paginação e lógica de ações.
    Equivalente a carregarPatriarcas() do GAS.
    
    LÓGICA DE NEGÓCIO:
    - Status "Novo" (1) ou "Em Progresso" (2): sempre pode selecionar
    - Status "Enviando Carga" (3) ou "Carga Processada" (4):
        * Se < 1 hora desde dat_alteracao: pode selecionar normalmente
        * Se >= 1 hora ou sem data: requer reset (botão "Atualizar e Selecionar")
    - Outros status: bloqueado
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
    
    # Calcular ações disponíveis para cada patriarca
    for p in patriarcas:
        status_desc = p.id_status_progresso.str_descricao
        status_id_num = p.id_status_progresso.id_status_progresso
        
        # Valores padrão
        p.pode_selecionar = False
        p.requer_reset = False
        p.expirado = False
        
        # Cenário 1: Status "Novo" ou "Em Progresso" -> pode selecionar diretamente
        if status_id_num in [1, 2]:  # 1=Novo, 2=Em Progresso
            p.pode_selecionar = True
            p.acao = 'selecionar'
        
        # Cenário 2: Status "Enviando Carga" (3) ou "Carga Processada" (4)
        elif status_id_num in [3, 4]:
            expirado = True  # Começa assumindo que expirou (caso mais seguro)
            
            # Verifica se existe data de alteração válida
            if p.dat_alteracao:
                tempo_decorrido = timezone.now() - p.dat_alteracao
                horas_decorridas = tempo_decorrido.total_seconds() / 3600
                
                # Se tem MENOS de 1 hora, NÃO expirou
                if horas_decorridas <= 1:
                    expirado = False
            # Se dat_alteracao for nula/inválida, 'expirado' permanece True
            
            p.expirado = expirado
            
            if expirado:
                # Se expirou (ou data inválida), mostra botão "Atualizar e Selecionar"
                p.requer_reset = True
                p.acao = 'reset'
            else:
                # Se ainda está no prazo, pode selecionar normalmente
                p.pode_selecionar = True
                p.acao = 'selecionar'
        
        # Cenário 3: Outros status -> bloqueado
        else:
            p.acao = 'bloqueado'
        
        # Informações adicionais
        p.tem_organograma = p.tem_organograma_ativo
        p.tem_lotacao = p.tem_lotacao_ativa
    
    # Paginação
    paginator = Paginator(patriarcas, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Lista de status para filtro
    status_list = TblStatusProgresso.objects.all()
    
    # Patriarca selecionado na sessão
    patriarca_selecionado = request.session.get('patriarca_selecionado')
    
    context = {
        'page_obj': page_obj,
        'status_list': status_list,
        'search': search,
        'status_id': status_id,
        'patriarca_selecionado': patriarca_selecionado,
    }
    
    return render(request, 'carga_org_lot/patriarca_list.html', context)


@carga_org_lot_required
def patriarca_detail(request, pk):
    """
    GET /carga_org_lot/patriarcas/{id}/
    
    Detalhes de um patriarca específico.
    """
    patriarca = get_object_or_404(
        TblPatriarca.objects.select_related(
            'id_status_progresso',
            'id_usuario_criacao'
        ),
        id_patriarca=pk
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


@carga_org_lot_required
def patriarca_create(request):
    """
    GET/POST /carga_org_lot/patriarcas/novo/
    
    Cria novo patriarca.
    Equivalente a incluirNovoPatriarca() do GAS.
    """
    if request.method == 'POST':
        form = PatriarcaForm(request.POST)
        if form.is_valid():
            patriarca = form.save(commit=False)
            patriarca.id_usuario_criacao = request.user
            patriarca.dat_criacao = timezone.now()
            patriarca.save()
            
            messages.success(
                request,
                f'Patriarca "{patriarca.str_sigla_patriarca}" criado com sucesso!'
            )
            return redirect('carga_org_lot:patriarca_list')
        else:
            messages.error(
                request,
                'Erro ao criar patriarca. Verifique os campos abaixo.'
            )
    else:
        form = PatriarcaForm()
    
    context = {
        'form': form,
        'action': 'Criar',
    }
    
    return render(request, 'carga_org_lot/patriarca_form.html', context)


@carga_org_lot_required
def patriarca_update(request, pk):
    """
    GET/POST /carga_org_lot/patriarcas/{id}/editar/
    
    Edita patriarca existente.
    Equivalente a editarPatriarca() do GAS.
    """
    patriarca = get_object_or_404(TblPatriarca, pk=pk)
    
    if request.method == 'POST':
        form = PatriarcaForm(request.POST, instance=patriarca)
        if form.is_valid():
            patriarca = form.save(commit=False)
            patriarca.id_usuario_alteracao = request.user
            patriarca.dat_alteracao = timezone.now()
            patriarca.save()
            
            messages.success(
                request,
                f'Patriarca "{patriarca.str_sigla_patriarca}" atualizado com sucesso!'
            )
            return redirect('carga_org_lot:patriarca_list')
        else:
            messages.error(
                request,
                'Erro ao atualizar patriarca. Verifique os campos abaixo.'
            )
    else:
        form = PatriarcaForm(instance=patriarca)
    
    context = {
        'form': form,
        'patriarca': patriarca,
        'action': 'Editar',
    }
    
    return render(request, 'carga_org_lot/patriarca_form.html', context)


@carga_org_lot_required
def patriarca_select(request, pk):
    """
    GET /carga_org_lot/patriarcas/{id}/selecionar/
    
    Seleciona patriarca na sessão.
    Equivalente a setSelectedPatriarca() do GAS.
    """
    patriarca = get_object_or_404(TblPatriarca, pk=pk)
    
    # Verificar se pode selecionar
    if patriarca.id_status_progresso.id_status_progresso not in [1, 2]:
        messages.error(
            request,
            f'Patriarca "{patriarca.str_sigla_patriarca}" não pode ser selecionado no status atual. '
            f'Use a opção "Resetar" se necessário.'
        )
        return redirect('carga_org_lot:patriarca_list')
    
    # Salvar na sessão
    request.session['patriarca_selecionado'] = {
        'id': patriarca.id_patriarca,
        'sigla': patriarca.str_sigla_patriarca,
        'nome': patriarca.str_nome,
        'id_externo': str(patriarca.id_externo_patriarca),
        'status_id': patriarca.id_status_progresso.id_status_progresso,
        'status_descricao': patriarca.id_status_progresso.str_descricao,
    }
    request.session.modified = True
    
    messages.success(
        request,
        f'Patriarca "{patriarca.str_sigla_patriarca}" selecionado com sucesso! '
        f'Você pode prosseguir com as operações de carga no dashboard.'
    )
    
    # Redirecionar para dashboard ao invés de upload_organograma (evita HTTP 405)
    return redirect('carga_org_lot:dashboard')


@carga_org_lot_required
def patriarca_reset(request, pk):
    """
    GET /carga_org_lot/patriarcas/{id}/reset/
    
    Reseta status do patriarca para "Em Progresso".
    Equivalente a resetPatriarca() do GAS.
    """
    patriarca = get_object_or_404(TblPatriarca, pk=pk)
    
    # Obter status "Em Progresso"
    try:
        status_em_progresso = TblStatusProgresso.objects.get(id_status_progresso=2)
    except TblStatusProgresso.DoesNotExist:
        messages.error(request, 'Status "Em Progresso" não encontrado no sistema.')
        return redirect('carga_org_lot:patriarca_list')
    
    # Atualizar patriarca
    patriarca.id_status_progresso = status_em_progresso
    patriarca.dat_alteracao = timezone.now()
    patriarca.id_usuario_alteracao = request.user
    patriarca.save()
    
    # Selecionar automaticamente
    request.session['patriarca_selecionado'] = {
        'id': patriarca.id_patriarca,
        'sigla': patriarca.str_sigla_patriarca,
        'nome': patriarca.str_nome,
        'id_externo': str(patriarca.id_externo_patriarca),
        'status_id': patriarca.id_status_progresso.id_status_progresso,
        'status_descricao': patriarca.id_status_progresso.str_descricao,
    }
    request.session.modified = True
    
    messages.success(
        request,
        f'Patriarca "{patriarca.str_sigla_patriarca}" foi resetado para "Em Progresso" '
        f'e selecionado automaticamente. Você pode prosseguir com as operações no dashboard.'
    )
    
    # Redirecionar para dashboard ao invés de upload_organograma (evita HTTP 405)
    return redirect('carga_org_lot:dashboard')
