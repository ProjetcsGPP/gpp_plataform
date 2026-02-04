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
    
    LÓGICA DE NEGÓCIO (conforme STATUS_PATRIARCA.md):
    
    Status 1 (Nova Carga) - GAS 'novo':
        - Sempre pode selecionar
        
    Status 2 (Organograma em Progresso) - GAS 'em progresso':
        - Sempre pode selecionar
        
    Status 3 (Lotação em Progresso) - GAS 'em progresso':
        - Sempre pode selecionar
        
    Status 4 (Pronto para Carga):
        - Sempre pode selecionar
        
    Status 5 (Carga em Processamento) - GAS 'enviando carga':
        - Se < 1 hora desde dat_alteracao: pode selecionar normalmente
        - Se >= 1 hora ou sem data: requer reset (botão "Atualizar e Selecionar")
        
    Status 6 (Carga Finalizada) - GAS 'carga processada':
        - Se < 1 hora desde dat_alteracao: pode selecionar normalmente
        - Se >= 1 hora ou sem data: requer reset (botão "Atualizar e Selecionar")
        
    Outros status: bloqueado
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
        status_id_num = p.id_status_progresso.id_status_progresso
        
        # Valores padrão
        p.pode_selecionar = False
        p.requer_reset = False
        p.expirado = False
        
        # Cenário 1: Status 1, 2, 3 ou 4 -> pode selecionar diretamente
        # (Nova Carga, Organograma/Lotação em Progresso, Pronto para Carga)
        if status_id_num in [1, 2, 3, 4]:
            p.pode_selecionar = True
            p.acao = 'selecionar'
        
        # Cenário 2: Status 5 ou 6 (Carga em Processamento, Carga Finalizada)
        # Aqui entra a lógica de timeout de 1 hora
        elif status_id_num in [5, 6]:
            expirado = True  # Começa assumindo que expirou (caso mais seguro)
            
            # Verifica se existe data de alteração válida
            if p.dat_alteracao:
                tempo_decorrido = timezone.now() - p.dat_alteracao
                horas_decorridas = tempo_decorrido.total_seconds() / 3600
                
                # Se tem MENOS de 1 hora, NÃO expirou
                if horas_decorridas < 1:
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
    Disponível apenas para status 5 e 6 (com histórico de envio).
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
    
    Todo novo patriarca começa automaticamente com:
    - id_status_progresso = 1 (Nova Carga)
    - dat_criacao = agora
    - id_usuario_criacao = usuário logado
    """
    if request.method == 'POST':
        form = PatriarcaForm(request.POST)
        if form.is_valid():
            # Obter status "Nova Carga" (ID = 1)
            try:
                status_nova_carga = TblStatusProgresso.objects.get(id_status_progresso=1)
            except TblStatusProgresso.DoesNotExist:
                messages.error(
                    request,
                    'Erro crítico: Status "Nova Carga" (ID=1) não encontrado no banco de dados. '
                    'Entre em contato com o administrador do sistema.'
                )
                return redirect('carga_org_lot:patriarca_list')
            
            # Criar patriarca
            patriarca = form.save(commit=False)
            patriarca.id_status_progresso = status_nova_carga  # Forçar status 1
            patriarca.id_usuario_criacao = request.user
            patriarca.dat_criacao = timezone.now()
            patriarca.save()
            
            messages.success(
                request,
                f'Patriarca "{patriarca.str_sigla_patriarca}" criado com sucesso! '
                f'Status inicial: "{status_nova_carga.str_descricao}".'
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
    
    Atenção: O campo id_status_progresso NÃO pode ser alterado via formulário.
    O status é gerenciado automaticamente pelo sistema durante o ciclo de vida.
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
    
    Permite seleção para status 1, 2, 3, 4, 5 (< 1h) e 6 (< 1h).
    """
    patriarca = get_object_or_404(TblPatriarca, pk=pk)
    
    # Verificar se pode selecionar (status 1, 2, 3, 4 ou 5/6 sem timeout)
    status_id = patriarca.id_status_progresso.id_status_progresso
    
    if status_id not in [1, 2, 3, 4, 5, 6]:
        messages.error(
            request,
            f'Patriarca "{patriarca.str_sigla_patriarca}" não pode ser selecionado no status atual.'
        )
        return redirect('carga_org_lot:patriarca_list')
    
    # Se status 5 ou 6, verifica timeout
    if status_id in [5, 6]:
        if patriarca.dat_alteracao:
            tempo_decorrido = timezone.now() - patriarca.dat_alteracao
            horas_decorridas = tempo_decorrido.total_seconds() / 3600
            
            if horas_decorridas >= 1:
                messages.error(
                    request,
                    f'Patriarca "{patriarca.str_sigla_patriarca}" expirou (>1 hora). '
                    f'Use a opção "Atualizar e Selecionar".'
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
    
    # Redirecionar para dashboard
    return redirect('carga_org_lot:dashboard')


@carga_org_lot_required
def patriarca_reset(request, pk):
    """
    GET /carga_org_lot/patriarcas/{id}/reset/
    
    Reseta status do patriarca para "Organograma em Progresso" (Status 2).
    Equivalente a resetPatriarca() do GAS.
    
    Usado quando:
    - Patriarca em status 5 ou 6 expirou (>= 1 hora)
    - Usuário deseja fazer nova carga com novos dados
    """
    patriarca = get_object_or_404(TblPatriarca, pk=pk)
    
    # Obter status "Organograma em Progresso" (Status 2)
    try:
        status_em_progresso = TblStatusProgresso.objects.get(id_status_progresso=2)
    except TblStatusProgresso.DoesNotExist:
        messages.error(request, 'Status "Organograma em Progresso" (2) não encontrado no sistema.')
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
        f'Patriarca "{patriarca.str_sigla_patriarca}" foi resetado para "Organograma em Progresso" '
        f'e selecionado automaticamente. Você pode prosseguir com novo ciclo de carga no dashboard.'
    )
    
    # Redirecionar para dashboard
    return redirect('carga_org_lot:dashboard')
