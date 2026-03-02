"""
Web Views usando Class-Based Views com AuthorizationService.
Migração gradual de web_views.py (function-based) para CBV.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.db.models import Prefetch

from ..models import (
    Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta,
    TipoAnotacaoAlinhamento, Acoes, AcaoPrazo, AcaoDestaque,
    AcaoAnotacaoAlinhamento, UsuarioResponsavel,
    RelacaoAcaoUsuarioResponsavel
)
from ..mixins import (
    AuthorizationPermissionMixin,
    ReadOnlyWebMixin,
    CreateUpdateWebMixin,
    DeleteWebMixin
)


# ============================================================================
# MIXIN CUSTOMIZADO PARA ACOES_PNGI
# ============================================================================

class AcoesPNGIAccessMixin(LoginRequiredMixin):
    """
    Mixin base para todas as views web de Ações PNGI.
    Verifica se usuário tem acesso à aplicação.
    """
    login_url = '/acoes-pngi/login/'
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar se tem acesso à aplicação
        from accounts.models import UserRole
        
        has_access = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).exists()
        
        if not has_access:
            messages.error(request, 'Você não tem permissão para acessar esta aplicação.')
            return redirect('acoes_pngi_web:login')
        
        return super().dispatch(request, *args, **kwargs)


# ============================================================================
# EIXOS (CONFIGURAÇÕES - Nível 2)
# ============================================================================

class EixoListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista todos os eixos - Requer: view_eixo"""
    model = Eixo
    permission_model = 'eixo'
    template_name = 'acoes_pngi/eixos/list.html'
    context_object_name = 'eixos'
    ordering = ['stralias']


class EixoCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria novo eixo - Requer: add_eixo (GESTOR ou COORDENADOR)"""
    model = Eixo
    permission_model = 'eixo'
    permission_action = 'add'
    template_name = 'acoes_pngi/eixos/form.html'
    fields = ['strdescricaoeixo', 'stralias']
    success_url = reverse_lazy('acoes_pngi_web:eixos_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Eixo "{form.instance.strdescricaoeixo}" criado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar eixo. Verifique os campos.')
        return super().form_invalid(form)


class EixoUpdateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, UpdateView):
    """Atualiza eixo - Requer: change_eixo (GESTOR ou COORDENADOR)"""
    model = Eixo
    permission_model = 'eixo'
    permission_action = 'change'
    template_name = 'acoes_pngi/eixos/form.html'
    fields = ['strdescricaoeixo', 'stralias']
    success_url = reverse_lazy('acoes_pngi_web:eixos_list')
    context_object_name = 'eixo'
    
    def form_valid(self, form):
        messages.success(self.request, f'Eixo "{form.instance.strdescricaoeixo}" atualizado com sucesso!')
        return super().form_valid(form)


class EixoDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta eixo - Requer: delete_eixo (GESTOR ou COORDENADOR)"""
    model = Eixo
    permission_model = 'eixo'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:eixos_list')
    template_name = 'acoes_pngi/eixos/confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nome = self.object.strdescricaoeixo
        messages.success(request, f'Eixo "{nome}" deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# VIGÊNCIAS PNGI (CONFIGURAÇÕES - Nível 2)
# ============================================================================

class VigenciaListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista vigências - Requer: view_vigenciapngi"""
    model = VigenciaPNGI
    permission_model = 'vigenciapngi'
    template_name = 'acoes_pngi/vigencias/list.html'
    context_object_name = 'vigencias'
    ordering = ['-datiniciovigencia']


class VigenciaCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria vigência - Requer: add_vigenciapngi (GESTOR ou COORDENADOR)"""
    model = VigenciaPNGI
    permission_model = 'vigenciapngi'
    permission_action = 'add'
    template_name = 'acoes_pngi/vigencias/form.html'
    fields = ['strdescricaovigenciapngi', 'datiniciovigencia', 'datfinalvigencia', 'isvigenciaativa']
    success_url = reverse_lazy('acoes_pngi_web:vigencias_list')
    
    def form_valid(self, form):
        # Se está ativando, desativar outras
        if form.instance.isvigenciaativa:
            VigenciaPNGI.objects.filter(isvigenciaativa=True).update(isvigenciaativa=False)
        
        messages.success(self.request, f'Vigência criada com sucesso!')
        return super().form_valid(form)


class VigenciaUpdateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, UpdateView):
    """Atualiza vigência - Requer: change_vigenciapngi (GESTOR ou COORDENADOR)"""
    model = VigenciaPNGI
    permission_model = 'vigenciapngi'
    permission_action = 'change'
    template_name = 'acoes_pngi/vigencias/form.html'
    fields = ['strdescricaovigenciapngi', 'datiniciovigencia', 'datfinalvigencia', 'isvigenciaativa']
    success_url = reverse_lazy('acoes_pngi_web:vigencias_list')
    context_object_name = 'vigencia'
    
    def form_valid(self, form):
        # Se está ativando, desativar outras
        if form.instance.isvigenciaativa and not self.object.isvigenciaativa:
            VigenciaPNGI.objects.filter(isvigenciaativa=True).exclude(pk=self.object.pk).update(isvigenciaativa=False)
        
        messages.success(self.request, f'Vigência atualizada com sucesso!')
        return super().form_valid(form)


class VigenciaDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta vigência - Requer: delete_vigenciapngi (GESTOR ou COORDENADOR)"""
    model = VigenciaPNGI
    permission_model = 'vigenciapngi'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:vigencias_list')
    template_name = 'acoes_pngi/vigencias/confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, f'Vigência deletada com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# SITUAÇÃO AÇÃO (CONFIGURAÇÕES - Nível 1 - Apenas GESTOR)
# ============================================================================

class SituacaoAcaoListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista situações - Requer: view_situacaoacao"""
    model = SituacaoAcao
    permission_model = 'situacaoacao'
    template_name = 'acoes_pngi/situacoes/list.html'
    context_object_name = 'situacoes'
    ordering = ['strdescricaosituacao']


class SituacaoAcaoCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria situação - Requer: add_situacaoacao (Apenas GESTOR)"""
    model = SituacaoAcao
    permission_model = 'situacaoacao'
    permission_action = 'add'
    template_name = 'acoes_pngi/situacoes/form.html'
    fields = ['strdescricaosituacao']
    success_url = reverse_lazy('acoes_pngi_web:situacoes_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Situação "{form.instance.strdescricaosituacao}" criada com sucesso!')
        return super().form_valid(form)


class SituacaoAcaoUpdateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, UpdateView):
    """Atualiza situação - Requer: change_situacaoacao (Apenas GESTOR)"""
    model = SituacaoAcao
    permission_model = 'situacaoacao'
    permission_action = 'change'
    template_name = 'acoes_pngi/situacoes/form.html'
    fields = ['strdescricaosituacao']
    success_url = reverse_lazy('acoes_pngi_web:situacoes_list')
    context_object_name = 'situacao'


class SituacaoAcaoDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta situação - Requer: delete_situacaoacao (Apenas GESTOR)"""
    model = SituacaoAcao
    permission_model = 'situacaoacao'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:situacoes_list')
    template_name = 'acoes_pngi/situacoes/confirm_delete.html'


# ============================================================================
# TIPO ENTRAVE/ALERTA (CONFIGURAÇÕES - Nível 1 - Apenas GESTOR)
# ============================================================================

class TipoEntraveAlertaListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista tipos de entrave - Requer: view_tipoentravealerta"""
    model = TipoEntraveAlerta
    permission_model = 'tipoentravealerta'
    template_name = 'acoes_pngi/tipos_entrave/list.html'
    context_object_name = 'tipos_entrave'
    ordering = ['strdescricaotipoentravealerta']


class TipoEntraveAlertaCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria tipo de entrave - Requer: add_tipoentravealerta (Apenas GESTOR)"""
    model = TipoEntraveAlerta
    permission_model = 'tipoentravealerta'
    permission_action = 'add'
    template_name = 'acoes_pngi/tipos_entrave/form.html'
    fields = ['strdescricaotipoentravealerta']
    success_url = reverse_lazy('acoes_pngi_web:tipos_entrave_list')


class TipoEntraveAlertaUpdateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, UpdateView):
    """Atualiza tipo de entrave - Requer: change_tipoentravealerta (Apenas GESTOR)"""
    model = TipoEntraveAlerta
    permission_model = 'tipoentravealerta'
    permission_action = 'change'
    template_name = 'acoes_pngi/tipos_entrave/form.html'
    fields = ['strdescricaotipoentravealerta']
    success_url = reverse_lazy('acoes_pngi_web:tipos_entrave_list')
    context_object_name = 'tipo_entrave'


class TipoEntraveAlertaDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta tipo de entrave - Requer: delete_tipoentravealerta (Apenas GESTOR)"""
    model = TipoEntraveAlerta
    permission_model = 'tipoentravealerta'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:tipos_entrave_list')
    template_name = 'acoes_pngi/tipos_entrave/confirm_delete.html'


# ============================================================================
# TIPO ANOTAÇÃO ALINHAMENTO (CONFIGURAÇÕES - Nível 2)
# ============================================================================

class TipoAnotacaoAlinhamentoListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista tipos de anotação - Requer: view_tipoanotacaoalinhamento"""
    model = TipoAnotacaoAlinhamento
    permission_model = 'tipoanotacaoalinhamento'
    template_name = 'acoes_pngi/tipos_anotacao/list.html'
    context_object_name = 'tipos_anotacao'
    ordering = ['strdescricaotipoanotacaoalinhamento']


class TipoAnotacaoAlinhamentoCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria tipo de anotação - Requer: add_tipoanotacaoalinhamento (GESTOR ou COORDENADOR)"""
    model = TipoAnotacaoAlinhamento
    permission_model = 'tipoanotacaoalinhamento'
    permission_action = 'add'
    template_name = 'acoes_pngi/tipos_anotacao/form.html'
    fields = ['strdescricaotipoanotacaoalinhamento']
    success_url = reverse_lazy('acoes_pngi_web:tipos_anotacao_list')


class TipoAnotacaoAlinhamentoUpdateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, UpdateView):
    """Atualiza tipo de anotação - Requer: change_tipoanotacaoalinhamento (GESTOR ou COORDENADOR)"""
    model = TipoAnotacaoAlinhamento
    permission_model = 'tipoanotacaoalinhamento'
    permission_action = 'change'
    template_name = 'acoes_pngi/tipos_anotacao/form.html'
    fields = ['strdescricaotipoanotacaoalinhamento']
    success_url = reverse_lazy('acoes_pngi_web:tipos_anotacao_list')
    context_object_name = 'tipo_anotacao'


class TipoAnotacaoAlinhamentoDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta tipo de anotação - Requer: delete_tipoanotacaoalinhamento (GESTOR ou COORDENADOR)"""
    model = TipoAnotacaoAlinhamento
    permission_model = 'tipoanotacaoalinhamento'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:tipos_anotacao_list')
    template_name = 'acoes_pngi/tipos_anotacao/confirm_delete.html'

# ============================================================================
# AÇÕES (OPERAÇÕES - GESTOR, COORDENADOR, OPERADOR)
# ============================================================================

class AcoesListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista ações - Requer: view_acoes"""
    model = Acoes
    permission_model = 'acoes'
    template_name = 'acoes_pngi/acoes/list.html'
    context_object_name = 'acoes'
    ordering = ['strapelido']
    
    def get_queryset(self):
        return super().get_queryset().select_related(
            'ideixo', 'idsituacaoacao', 'idvigenciapngi', 'idtipoentravealerta'
        )


class AcoesCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria ação - Requer: add_acoes (GESTOR, COORDENADOR ou OPERADOR)"""
    model = Acoes
    permission_model = 'acoes'
    permission_action = 'add'
    template_name = 'acoes_pngi/acoes/form.html'
    fields = [
        'strapelido', 'strdescricaoacao', 'strdescricaoentrega',
        'datdataentrega', 'ideixo', 'idsituacaoacao', 'idvigenciapngi',
        'idtipoentravealerta'
    ]
    success_url = reverse_lazy('acoes_pngi_web:acoes_list')


class AcoesUpdateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, UpdateView):
    """Atualiza ação - Requer: change_acoes (GESTOR, COORDENADOR ou OPERADOR)"""
    model = Acoes
    permission_model = 'acoes'
    permission_action = 'change'
    template_name = 'acoes_pngi/acoes/form.html'
    fields = [
        'strapelido', 'strdescricaoacao', 'strdescricaoentrega',
        'datdataentrega', 'ideixo', 'idsituacaoacao', 'idvigenciapngi',
        'idtipoentravealerta'
    ]
    success_url = reverse_lazy('acoes_pngi_web:acoes_list')
    context_object_name = 'acao'


class AcoesDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta ação - Requer: delete_acoes (GESTOR, COORDENADOR ou OPERADOR)"""
    model = Acoes
    permission_model = 'acoes'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:acoes_list')
    template_name = 'acoes_pngi/acoes/confirm_delete.html'


# ============================================================================
# AÇÃO PRAZO (Vinculado a Ações)
# ============================================================================

class AcaoPrazoListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista prazos - Requer: view_acaoprazo"""
    model = AcaoPrazo
    permission_model = 'acaoprazo'
    template_name = 'acoes_pngi/prazos/list.html'
    context_object_name = 'prazos'
    ordering = ['-isacaoprazoativo', '-created_at']
    
    def get_queryset(self):
        acao_id = self.kwargs.get('acao_id')
        if acao_id:
            return super().get_queryset().filter(idacao_id=acao_id)
        return super().get_queryset().select_related('idacao')


class AcaoPrazoCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria prazo - Requer: add_acaoprazo (GESTOR, COORDENADOR ou OPERADOR)"""
    model = AcaoPrazo
    permission_model = 'acaoprazo'
    permission_action = 'add'
    template_name = 'acoes_pngi/prazos/form.html'
    fields = ['idacao', 'strprazo', 'isacaoprazoativo']
    success_url = reverse_lazy('acoes_pngi_web:prazos_list')


class AcaoPrazoUpdateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, UpdateView):
    """Atualiza prazo - Requer: change_acaoprazo (GESTOR, COORDENADOR ou OPERADOR)"""
    model = AcaoPrazo
    permission_model = 'acaoprazo'
    permission_action = 'change'
    template_name = 'acoes_pngi/prazos/form.html'
    fields = ['idacao', 'strprazo', 'isacaoprazoativo']
    success_url = reverse_lazy('acoes_pngi_web:prazos_list')
    context_object_name = 'prazo'


class AcaoPrazoDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta prazo - Requer: delete_acaoprazo (GESTOR, COORDENADOR ou OPERADOR)"""
    model = AcaoPrazo
    permission_model = 'acaoprazo'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:prazos_list')
    template_name = 'acoes_pngi/prazos/confirm_delete.html'


# ============================================================================
# AÇÃO DESTAQUE
# ============================================================================

class AcaoDestaqueListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista destaques - Requer: view_acaodestaque"""
    model = AcaoDestaque
    permission_model = 'acaodestaque'
    template_name = 'acoes_pngi/destaques/list.html'
    context_object_name = 'destaques'
    ordering = ['-datdatadestaque']


class AcaoDestaqueCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria destaque - Requer: add_acaodestaque (GESTOR, COORDENADOR ou OPERADOR)"""
    model = AcaoDestaque
    permission_model = 'acaodestaque'
    permission_action = 'add'
    template_name = 'acoes_pngi/destaques/form.html'
    fields = ['idacao', 'datdatadestaque']
    success_url = reverse_lazy('acoes_pngi_web:destaques_list')


class AcaoDestaqueUpdateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, UpdateView):
    """Atualiza destaque - Requer: change_acaodestaque (GESTOR, COORDENADOR ou OPERADOR)"""
    model = AcaoDestaque
    permission_model = 'acaodestaque'
    permission_action = 'change'
    template_name = 'acoes_pngi/destaques/form.html'
    fields = ['idacao', 'datdatadestaque']
    success_url = reverse_lazy('acoes_pngi_web:destaques_list')
    context_object_name = 'destaque'


class AcaoDestaqueDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta destaque - Requer: delete_acaodestaque (GESTOR, COORDENADOR ou OPERADOR)"""
    model = AcaoDestaque
    permission_model = 'acaodestaque'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:destaques_list')
    template_name = 'acoes_pngi/destaques/confirm_delete.html'


# ============================================================================
# AÇÃO ANOTAÇÃO ALINHAMENTO
# ============================================================================

class AcaoAnotacaoAlinhamentoListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista anotações - Requer: view_acaoanotacaoalinhamento"""
    model = AcaoAnotacaoAlinhamento
    permission_model = 'acaoanotacaoalinhamento'
    template_name = 'acoes_pngi/anotacoes/list.html'
    context_object_name = 'anotacoes'
    ordering = ['-datdataanotacaoalinhamento']


class AcaoAnotacaoAlinhamentoCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria anotação - Requer: add_acaoanotacaoalinhamento (GESTOR, COORDENADOR ou OPERADOR)"""
    model = AcaoAnotacaoAlinhamento
    permission_model = 'acaoanotacaoalinhamento'
    permission_action = 'add'
    template_name = 'acoes_pngi/anotacoes/form.html'
    fields = [
        'idacao', 'idtipoanotacaoalinhamento', 'datdataanotacaoalinhamento',
        'strdescricaoanotacaoalinhamento', 'strlinkanotacaoalinhamento',
        'strnumeromonitoramento'
    ]
    success_url = reverse_lazy('acoes_pngi_web:anotacoes_list')


class AcaoAnotacaoAlinhamentoUpdateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, UpdateView):
    """Atualiza anotação - Requer: change_acaoanotacaoalinhamento (GESTOR, COORDENADOR ou OPERADOR)"""
    model = AcaoAnotacaoAlinhamento
    permission_model = 'acaoanotacaoalinhamento'
    permission_action = 'change'
    template_name = 'acoes_pngi/anotacoes/form.html'
    fields = [
        'idacao', 'idtipoanotacaoalinhamento', 'datdataanotacaoalinhamento',
        'strdescricaoanotacaoalinhamento', 'strlinkanotacaoalinhamento',
        'strnumeromonitoramento'
    ]
    success_url = reverse_lazy('acoes_pngi_web:anotacoes_list')
    context_object_name = 'anotacao'


class AcaoAnotacaoAlinhamentoDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta anotação - Requer: delete_acaoanotacaoalinhamento (GESTOR, COORDENADOR ou OPERADOR)"""
    model = AcaoAnotacaoAlinhamento
    permission_model = 'acaoanotacaoalinhamento'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:anotacoes_list')
    template_name = 'acoes_pngi/anotacoes/confirm_delete.html'


# ============================================================================
# USUÁRIO RESPONSÁVEL
# ============================================================================

class UsuarioResponsavelListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista responsáveis - Requer: view_usuarioresponsavel"""
    model = UsuarioResponsavel
    permission_model = 'usuarioresponsavel'
    template_name = 'acoes_pngi/responsaveis/list.html'
    context_object_name = 'responsaveis'
    
    def get_queryset(self):
        return super().get_queryset().select_related('idusuario')


class UsuarioResponsavelCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria responsável - Requer: add_usuarioresponsavel (GESTOR, COORDENADOR ou OPERADOR)"""
    model = UsuarioResponsavel
    permission_model = 'usuarioresponsavel'
    permission_action = 'add'
    template_name = 'acoes_pngi/responsaveis/form.html'
    fields = ['idusuario', 'strtelefone', 'strorgao']
    success_url = reverse_lazy('acoes_pngi_web:responsaveis_list')


class UsuarioResponsavelUpdateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, UpdateView):
    """Atualiza responsável - Requer: change_usuarioresponsavel (GESTOR, COORDENADOR ou OPERADOR)"""
    model = UsuarioResponsavel
    permission_model = 'usuarioresponsavel'
    permission_action = 'change'
    template_name = 'acoes_pngi/responsaveis/form.html'
    fields = ['strtelefone', 'strorgao']
    success_url = reverse_lazy('acoes_pngi_web:responsaveis_list')
    context_object_name = 'responsavel'


class UsuarioResponsavelDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta responsável - Requer: delete_usuarioresponsavel (GESTOR, COORDENADOR ou OPERADOR)"""
    model = UsuarioResponsavel
    permission_model = 'usuarioresponsavel'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:responsaveis_list')
    template_name = 'acoes_pngi/responsaveis/confirm_delete.html'


# ============================================================================
# RELAÇÃO AÇÃO-USUÁRIO RESPONSÁVEL
# ============================================================================

class RelacaoAcaoUsuarioResponsavelListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """Lista relações - Requer: view_relacaoacaousuarioresponsavel"""
    model = RelacaoAcaoUsuarioResponsavel
    permission_model = 'relacaoacaousuarioresponsavel'
    template_name = 'acoes_pngi/relacoes/list.html'
    context_object_name = 'relacoes'
    
    def get_queryset(self):
        return super().get_queryset().select_related('idacao', 'idusuarioresponsavel__idusuario')


class RelacaoAcaoUsuarioResponsavelCreateView(AcoesPNGIAccessMixin, CreateUpdateWebMixin, CreateView):
    """Cria relação - Requer: add_relacaoacaousuarioresponsavel (GESTOR, COORDENADOR ou OPERADOR)"""
    model = RelacaoAcaoUsuarioResponsavel
    permission_model = 'relacaoacaousuarioresponsavel'
    permission_action = 'add'
    template_name = 'acoes_pngi/relacoes/form.html'
    fields = ['idacao', 'idusuarioresponsavel']
    success_url = reverse_lazy('acoes_pngi_web:relacoes_list')


class RelacaoAcaoUsuarioResponsavelDeleteView(AcoesPNGIAccessMixin, DeleteWebMixin, DeleteView):
    """Deleta relação - Requer: delete_relacaoacaousuarioresponsavel (GESTOR, COORDENADOR ou OPERADOR)"""
    model = RelacaoAcaoUsuarioResponsavel
    permission_model = 'relacaoacaousuarioresponsavel'
    permission_action = 'delete'
    success_url = reverse_lazy('acoes_pngi_web:relacoes_list')
    template_name = 'acoes_pngi/relacoes/confirm_delete.html'


class AcoesCompletasListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """
    📊 Lista COMPLETA de Ações com TODAS as relações:
    
    ✅ Eixo, Situação, Vigência, Tipo Entrave
    ✅ Responsáveis (com telefone/orgão)
    ✅ Prazo ativo
    ✅ Destaques (com data)
    ✅ Anotações de alinhamento (com tipo e data)
    
    Requer: view_acoes
    Template: acoes_pngi/acoes/completa_list.html
    """
    model = Acoes
    permission_model = 'acoes'
    template_name = 'acoes_pngi/acoes/completa_list.html'
    context_object_name = 'acoes'
    paginate_by = 25  # Paginação para performance
    
    def get_queryset(self):
        """
        Query otimizada com todas as relações pré-carregadas (sem N+1 queries)
        """
        return Acoes.objects.select_related(
            'ideixo',           # Eixo
            'idsituacaoacao',   # Situação
            'idvigenciapngi',   # Vigência
            'idtipoentravealerta'  # Tipo entrave
        ).prefetch_related(
            Prefetch(
                'responsaveis',  # RelacaoAcaoUsuarioResponsavel
                queryset=RelacaoAcaoUsuarioResponsavel.objects.select_related(
                    'idusuarioresponsavel__idusuario'  # UsuarioResponsavel → User
                ),
                to_attr='responsaveis_completos'
            ),
            Prefetch(
                'prazos',  # AcaoPrazo
                queryset=AcaoPrazo.objects.filter(isacaoprazoativo=True),
                to_attr='prazo_ativo'
            ),
            Prefetch(
                'destaques',  # AcaoDestaque
                queryset=AcaoDestaque.objects.order_by('-datdatadestaque')[:3],
                to_attr='ultimos_destaques'
            ),
            Prefetch(
                'anotacoes_alinhamento',  # AcaoAnotacaoAlinhamento
                queryset=AcaoAnotacaoAlinhamento.objects.select_related(
                    'idtipoanotacaoalinhamento'
                ).order_by('-datdataanotacaoalinhamento')[:5],
                to_attr='ultimas_anotacoes'
            ),
            Prefetch(
                'responsaveis',  # ← RelacaoAcaoUsuarioResponsavel (M2M)
                queryset=RelacaoAcaoUsuarioResponsavel.objects.select_related(
                    'idusuarioresponsavel__idusuario'  # UsuarioResponsavel → User (public)
                ),
                to_attr='responsaveis_completos'  # ← Lista acessível no template
            )
        ).filter(
            idvigenciapngi__isvigenciaativa=True  # Apenas ações da vigência ativa
        ).order_by('strapelido')
    
    def get_context_data(self, **kwargs):
        """
        Contexto enriquecido para template:
        - Estatísticas globais
        - Filtros ativos
        - Permissões do usuário
        """
        context = super().get_context_data(**kwargs)
        
        # Estatísticas
        context['stats'] = {
            'total_acoes': Acoes.objects.count(),
            'acoes_com_prazo_ativo': AcaoPrazo.objects.filter(isacaoprazoativo=True).count(),
            'acoes_com_responsavel': RelacaoAcaoUsuarioResponsavel.objects.count(),
            'acoes_com_destaque': AcaoDestaque.objects.count(),
        }
        
        # Permissões do usuário (injetadas pelo AuthorizationService)
        context['can_edit_acoes'] = self.request.user.has_app_perm('ACOES_PNGI', 'change_acoes')
        context['can_add_responsavel'] = self.request.user.has_app_perm('ACOES_PNGI', 'add_usuarioresponsavel')
        
        return context

class AcoesPorResponsavelListView(AcoesPNGIAccessMixin, ReadOnlyWebMixin, ListView):
    """
    👥 Lista ações agrupadas por USUÁRIO RESPONSÁVEL
    Requer: view_usuarioresponsavel + view_acoes
    """
    template_name = 'acoes_pngi/acoes/por_responsavel.html'
    context_object_name = 'responsaveis'
    
    def get_queryset(self):
        return UsuarioResponsavel.objects.prefetch_related(
            Prefetch(
                'acoes',  # ← Inverso: UsuarioResponsavel → RelacaoAcaoUsuarioResponsavel → Acoes
                queryset=RelacaoAcaoUsuarioResponsavel.objects.prefetch_related(
                    Prefetch('idacao__ideixo'),
                    Prefetch('idacao__idsituacaoacao'),
                    Prefetch('idacao__idvigenciapngi')
                ).select_related('idacao'),
                to_attr='acoes_relacionadas'
            )
        ).select_related('idusuario').filter(
            acoes__idvigenciapngi__isvigenciaativa=True
        ).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_relacoes'] = RelacaoAcaoUsuarioResponsavel.objects.count()
        return context
    