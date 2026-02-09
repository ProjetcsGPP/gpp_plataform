"""
Web Views do Ações PNGI.
Views baseadas em Class-Based Views para interface web.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Prefetch

from ..models import (
    Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta, Acoes,
    AcaoPrazo, AcaoDestaque, TipoAnotacaoAlinhamento,
    AcaoAnotacaoAlinhamento, UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel
)


# ============= EIXO VIEWS =============
class EixoListView(LoginRequiredMixin, ListView):
    model = Eixo
    template_name = 'acoes_pngi/eixo/list.html'
    context_object_name = 'eixos'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(strdescricaoeixo__icontains=search) |
                Q(stralias__icontains=search)
            )
        return queryset


class EixoDetailView(LoginRequiredMixin, DetailView):
    model = Eixo
    template_name = 'acoes_pngi/eixo/detail.html'
    context_object_name = 'eixo'
    pk_url_kwarg = 'ideixo'


class EixoCreateView(LoginRequiredMixin, CreateView):
    model = Eixo
    template_name = 'acoes_pngi/eixo/form.html'
    fields = ['strdescricaoeixo', 'stralias']
    success_url = reverse_lazy('acoes_pngi:eixo_list')

    def form_valid(self, form):
        messages.success(self.request, 'Eixo criado com sucesso!')
        return super().form_valid(form)


class EixoUpdateView(LoginRequiredMixin, UpdateView):
    model = Eixo
    template_name = 'acoes_pngi/eixo/form.html'
    fields = ['strdescricaoeixo', 'stralias']
    pk_url_kwarg = 'ideixo'
    success_url = reverse_lazy('acoes_pngi:eixo_list')

    def form_valid(self, form):
        messages.success(self.request, 'Eixo atualizado com sucesso!')
        return super().form_valid(form)


class EixoDeleteView(LoginRequiredMixin, DeleteView):
    model = Eixo
    template_name = 'acoes_pngi/eixo/confirm_delete.html'
    pk_url_kwarg = 'ideixo'
    success_url = reverse_lazy('acoes_pngi:eixo_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Eixo excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============= SITUACAO ACAO VIEWS =============
class SituacaoAcaoListView(LoginRequiredMixin, ListView):
    model = SituacaoAcao
    template_name = 'acoes_pngi/situacaoacao/list.html'
    context_object_name = 'situacoes'
    paginate_by = 20


class SituacaoAcaoDetailView(LoginRequiredMixin, DetailView):
    model = SituacaoAcao
    template_name = 'acoes_pngi/situacaoacao/detail.html'
    context_object_name = 'situacao'
    pk_url_kwarg = 'idsituacaoacao'


class SituacaoAcaoCreateView(LoginRequiredMixin, CreateView):
    model = SituacaoAcao
    template_name = 'acoes_pngi/situacaoacao/form.html'
    fields = ['strdescricaosituacao']
    success_url = reverse_lazy('acoes_pngi:situacaoacao_list')

    def form_valid(self, form):
        messages.success(self.request, 'Situação criada com sucesso!')
        return super().form_valid(form)


class SituacaoAcaoUpdateView(LoginRequiredMixin, UpdateView):
    model = SituacaoAcao
    template_name = 'acoes_pngi/situacaoacao/form.html'
    fields = ['strdescricaosituacao']
    pk_url_kwarg = 'idsituacaoacao'
    success_url = reverse_lazy('acoes_pngi:situacaoacao_list')

    def form_valid(self, form):
        messages.success(self.request, 'Situação atualizada com sucesso!')
        return super().form_valid(form)


class SituacaoAcaoDeleteView(LoginRequiredMixin, DeleteView):
    model = SituacaoAcao
    template_name = 'acoes_pngi/situacaoacao/confirm_delete.html'
    pk_url_kwarg = 'idsituacaoacao'
    success_url = reverse_lazy('acoes_pngi:situacaoacao_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Situação excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============= VIGENCIA PNGI VIEWS =============
class VigenciaPNGIListView(LoginRequiredMixin, ListView):
    model = VigenciaPNGI
    template_name = 'acoes_pngi/vigenciapngi/list.html'
    context_object_name = 'vigencias'
    paginate_by = 20


class VigenciaPNGIDetailView(LoginRequiredMixin, DetailView):
    model = VigenciaPNGI
    template_name = 'acoes_pngi/vigenciapngi/detail.html'
    context_object_name = 'vigencia'
    pk_url_kwarg = 'idvigenciapngi'


class VigenciaPNGICreateView(LoginRequiredMixin, CreateView):
    model = VigenciaPNGI
    template_name = 'acoes_pngi/vigenciapngi/form.html'
    fields = [
        'strdescricaovigenciapngi', 'datiniciovigencia',
        'datfinalvigencia', 'isvigenciaativa'
    ]
    success_url = reverse_lazy('acoes_pngi:vigenciapngi_list')

    def form_valid(self, form):
        messages.success(self.request, 'Vigência criada com sucesso!')
        return super().form_valid(form)


class VigenciaPNGIUpdateView(LoginRequiredMixin, UpdateView):
    model = VigenciaPNGI
    template_name = 'acoes_pngi/vigenciapngi/form.html'
    fields = [
        'strdescricaovigenciapngi', 'datiniciovigencia',
        'datfinalvigencia', 'isvigenciaativa'
    ]
    pk_url_kwarg = 'idvigenciapngi'
    success_url = reverse_lazy('acoes_pngi:vigenciapngi_list')

    def form_valid(self, form):
        messages.success(self.request, 'Vigência atualizada com sucesso!')
        return super().form_valid(form)


class VigenciaPNGIDeleteView(LoginRequiredMixin, DeleteView):
    model = VigenciaPNGI
    template_name = 'acoes_pngi/vigenciapngi/confirm_delete.html'
    pk_url_kwarg = 'idvigenciapngi'
    success_url = reverse_lazy('acoes_pngi:vigenciapngi_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Vigência excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============= TIPO ENTRAVE ALERTA VIEWS =============
class TipoEntraveAlertaListView(LoginRequiredMixin, ListView):
    model = TipoEntraveAlerta
    template_name = 'acoes_pngi/tipoentravealerta/list.html'
    context_object_name = 'tipos'
    paginate_by = 20


class TipoEntraveAlertaDetailView(LoginRequiredMixin, DetailView):
    model = TipoEntraveAlerta
    template_name = 'acoes_pngi/tipoentravealerta/detail.html'
    context_object_name = 'tipo'
    pk_url_kwarg = 'idtipoentravealerta'


class TipoEntraveAlertaCreateView(LoginRequiredMixin, CreateView):
    model = TipoEntraveAlerta
    template_name = 'acoes_pngi/tipoentravealerta/form.html'
    fields = ['strdescricaotipoentravealerta']
    success_url = reverse_lazy('acoes_pngi:tipoentravealerta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de Entrave/Alerta criado com sucesso!')
        return super().form_valid(form)


class TipoEntraveAlertaUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoEntraveAlerta
    template_name = 'acoes_pngi/tipoentravealerta/form.html'
    fields = ['strdescricaotipoentravealerta']
    pk_url_kwarg = 'idtipoentravealerta'
    success_url = reverse_lazy('acoes_pngi:tipoentravealerta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de Entrave/Alerta atualizado com sucesso!')
        return super().form_valid(form)


class TipoEntraveAlertaDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoEntraveAlerta
    template_name = 'acoes_pngi/tipoentravealerta/confirm_delete.html'
    pk_url_kwarg = 'idtipoentravealerta'
    success_url = reverse_lazy('acoes_pngi:tipoentravealerta_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tipo de Entrave/Alerta excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============= ACOES VIEWS =============
class AcoesListView(LoginRequiredMixin, ListView):
    model = Acoes
    template_name = 'acoes_pngi/acoes/list.html'
    context_object_name = 'acoes'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'idvigenciapngi', 'idtipoentravealerta'
        )
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(strapelido__icontains=search) |
                Q(strdescricaoacao__icontains=search)
            )
        return queryset


class AcoesDetailView(LoginRequiredMixin, DetailView):
    model = Acoes
    template_name = 'acoes_pngi/acoes/detail.html'
    context_object_name = 'acao'
    pk_url_kwarg = 'idacao'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'idvigenciapngi', 'idtipoentravealerta'
        ).prefetch_related(
            'prazos', 'destaques', 'anotacoes_alinhamento',
            Prefetch('responsaveis', queryset=RelacaoAcaoUsuarioResponsavel.objects.select_related(
                'idusuarioresponsavel__idusuario'
            ))
        )


class AcoesCreateView(LoginRequiredMixin, CreateView):
    model = Acoes
    template_name = 'acoes_pngi/acoes/form.html'
    fields = [
        'strapelido', 'strdescricaoacao', 'strdescricaoentrega',
        'idvigenciapngi', 'idtipoentravealerta', 'datdataentrega'
    ]
    success_url = reverse_lazy('acoes_pngi:acoes_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ação criada com sucesso!')
        return super().form_valid(form)


class AcoesUpdateView(LoginRequiredMixin, UpdateView):
    model = Acoes
    template_name = 'acoes_pngi/acoes/form.html'
    fields = [
        'strapelido', 'strdescricaoacao', 'strdescricaoentrega',
        'idvigenciapngi', 'idtipoentravealerta', 'datdataentrega'
    ]
    pk_url_kwarg = 'idacao'
    success_url = reverse_lazy('acoes_pngi:acoes_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ação atualizada com sucesso!')
        return super().form_valid(form)


class AcoesDeleteView(LoginRequiredMixin, DeleteView):
    model = Acoes
    template_name = 'acoes_pngi/acoes/confirm_delete.html'
    pk_url_kwarg = 'idacao'
    success_url = reverse_lazy('acoes_pngi:acoes_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Ação excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============= ACAO PRAZO VIEWS =============
class AcaoPrazoListView(LoginRequiredMixin, ListView):
    model = AcaoPrazo
    template_name = 'acoes_pngi/acaoprazo/list.html'
    context_object_name = 'prazos'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related('idacao')


class AcaoPrazoDetailView(LoginRequiredMixin, DetailView):
    model = AcaoPrazo
    template_name = 'acoes_pngi/acaoprazo/detail.html'
    context_object_name = 'prazo'
    pk_url_kwarg = 'idacaoprazo'


class AcaoPrazoCreateView(LoginRequiredMixin, CreateView):
    model = AcaoPrazo
    template_name = 'acoes_pngi/acaoprazo/form.html'
    fields = ['idacao', 'strprazo', 'isacaoprazoativo']
    success_url = reverse_lazy('acoes_pngi:acaoprazo_list')

    def form_valid(self, form):
        messages.success(self.request, 'Prazo criado com sucesso!')
        return super().form_valid(form)


class AcaoPrazoUpdateView(LoginRequiredMixin, UpdateView):
    model = AcaoPrazo
    template_name = 'acoes_pngi/acaoprazo/form.html'
    fields = ['idacao', 'strprazo', 'isacaoprazoativo']
    pk_url_kwarg = 'idacaoprazo'
    success_url = reverse_lazy('acoes_pngi:acaoprazo_list')

    def form_valid(self, form):
        messages.success(self.request, 'Prazo atualizado com sucesso!')
        return super().form_valid(form)


class AcaoPrazoDeleteView(LoginRequiredMixin, DeleteView):
    model = AcaoPrazo
    template_name = 'acoes_pngi/acaoprazo/confirm_delete.html'
    pk_url_kwarg = 'idacaoprazo'
    success_url = reverse_lazy('acoes_pngi:acaoprazo_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Prazo excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============= ACAO DESTAQUE VIEWS =============
class AcaoDestaqueListView(LoginRequiredMixin, ListView):
    model = AcaoDestaque
    template_name = 'acoes_pngi/acaodestaque/list.html'
    context_object_name = 'destaques'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related('idacao')


class AcaoDestaqueDetailView(LoginRequiredMixin, DetailView):
    model = AcaoDestaque
    template_name = 'acoes_pngi/acaodestaque/detail.html'
    context_object_name = 'destaque'
    pk_url_kwarg = 'idacaodestaque'


class AcaoDestaqueCreateView(LoginRequiredMixin, CreateView):
    model = AcaoDestaque
    template_name = 'acoes_pngi/acaodestaque/form.html'
    fields = ['idacao', 'datdatadestaque']
    success_url = reverse_lazy('acoes_pngi:acaodestaque_list')

    def form_valid(self, form):
        messages.success(self.request, 'Destaque criado com sucesso!')
        return super().form_valid(form)


class AcaoDestaqueUpdateView(LoginRequiredMixin, UpdateView):
    model = AcaoDestaque
    template_name = 'acoes_pngi/acaodestaque/form.html'
    fields = ['idacao', 'datdatadestaque']
    pk_url_kwarg = 'idacaodestaque'
    success_url = reverse_lazy('acoes_pngi:acaodestaque_list')

    def form_valid(self, form):
        messages.success(self.request, 'Destaque atualizado com sucesso!')
        return super().form_valid(form)


class AcaoDestaqueDeleteView(LoginRequiredMixin, DeleteView):
    model = AcaoDestaque
    template_name = 'acoes_pngi/acaodestaque/confirm_delete.html'
    pk_url_kwarg = 'idacaodestaque'
    success_url = reverse_lazy('acoes_pngi:acaodestaque_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Destaque excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============= TIPO ANOTACAO ALINHAMENTO VIEWS =============
class TipoAnotacaoAlinhamentoListView(LoginRequiredMixin, ListView):
    model = TipoAnotacaoAlinhamento
    template_name = 'acoes_pngi/tipoanotacaoalinhamento/list.html'
    context_object_name = 'tipos'
    paginate_by = 20


class TipoAnotacaoAlinhamentoDetailView(LoginRequiredMixin, DetailView):
    model = TipoAnotacaoAlinhamento
    template_name = 'acoes_pngi/tipoanotacaoalinhamento/detail.html'
    context_object_name = 'tipo'
    pk_url_kwarg = 'idtipoanotacaoalinhamento'


class TipoAnotacaoAlinhamentoCreateView(LoginRequiredMixin, CreateView):
    model = TipoAnotacaoAlinhamento
    template_name = 'acoes_pngi/tipoanotacaoalinhamento/form.html'
    fields = ['strdescricaotipoanotacaoalinhamento']
    success_url = reverse_lazy('acoes_pngi:tipoanotacaoalinhamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de Anotação criado com sucesso!')
        return super().form_valid(form)


class TipoAnotacaoAlinhamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoAnotacaoAlinhamento
    template_name = 'acoes_pngi/tipoanotacaoalinhamento/form.html'
    fields = ['strdescricaotipoanotacaoalinhamento']
    pk_url_kwarg = 'idtipoanotacaoalinhamento'
    success_url = reverse_lazy('acoes_pngi:tipoanotacaoalinhamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de Anotação atualizado com sucesso!')
        return super().form_valid(form)


class TipoAnotacaoAlinhamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoAnotacaoAlinhamento
    template_name = 'acoes_pngi/tipoanotacaoalinhamento/confirm_delete.html'
    pk_url_kwarg = 'idtipoanotacaoalinhamento'
    success_url = reverse_lazy('acoes_pngi:tipoanotacaoalinhamento_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tipo de Anotação excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============= ACAO ANOTACAO ALINHAMENTO VIEWS =============
class AcaoAnotacaoAlinhamentoListView(LoginRequiredMixin, ListView):
    model = AcaoAnotacaoAlinhamento
    template_name = 'acoes_pngi/acaoanotacaoalinhamento/list.html'
    context_object_name = 'anotacoes'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related(
            'idacao', 'idtipoanotacaoalinhamento'
        )


class AcaoAnotacaoAlinhamentoDetailView(LoginRequiredMixin, DetailView):
    model = AcaoAnotacaoAlinhamento
    template_name = 'acoes_pngi/acaoanotacaoalinhamento/detail.html'
    context_object_name = 'anotacao'
    pk_url_kwarg = 'idacaoanotacaoalinhamento'


class AcaoAnotacaoAlinhamentoCreateView(LoginRequiredMixin, CreateView):
    model = AcaoAnotacaoAlinhamento
    template_name = 'acoes_pngi/acaoanotacaoalinhamento/form.html'
    fields = [
        'idacao', 'idtipoanotacaoalinhamento', 'datdataanotacaoalinhamento',
        'strdescricaoanotacaoalinhamento', 'strlinkanotacaoalinhamento',
        'strnumeromonitoramento'
    ]
    success_url = reverse_lazy('acoes_pngi:acaoanotacaoalinhamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Anotação criada com sucesso!')
        return super().form_valid(form)


class AcaoAnotacaoAlinhamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = AcaoAnotacaoAlinhamento
    template_name = 'acoes_pngi/acaoanotacaoalinhamento/form.html'
    fields = [
        'idacao', 'idtipoanotacaoalinhamento', 'datdataanotacaoalinhamento',
        'strdescricaoanotacaoalinhamento', 'strlinkanotacaoalinhamento',
        'strnumeromonitoramento'
    ]
    pk_url_kwarg = 'idacaoanotacaoalinhamento'
    success_url = reverse_lazy('acoes_pngi:acaoanotacaoalinhamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Anotação atualizada com sucesso!')
        return super().form_valid(form)


class AcaoAnotacaoAlinhamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = AcaoAnotacaoAlinhamento
    template_name = 'acoes_pngi/acaoanotacaoalinhamento/confirm_delete.html'
    pk_url_kwarg = 'idacaoanotacaoalinhamento'
    success_url = reverse_lazy('acoes_pngi:acaoanotacaoalinhamento_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Anotação excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============= USUARIO RESPONSAVEL VIEWS =============
class UsuarioResponsavelListView(LoginRequiredMixin, ListView):
    model = UsuarioResponsavel
    template_name = 'acoes_pngi/usuarioresponsavel/list.html'
    context_object_name = 'responsaveis'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related('idusuario')


class UsuarioResponsavelDetailView(LoginRequiredMixin, DetailView):
    model = UsuarioResponsavel
    template_name = 'acoes_pngi/usuarioresponsavel/detail.html'
    context_object_name = 'responsavel'
    pk_url_kwarg = 'idusuario'


class UsuarioResponsavelCreateView(LoginRequiredMixin, CreateView):
    model = UsuarioResponsavel
    template_name = 'acoes_pngi/usuarioresponsavel/form.html'
    fields = ['idusuario', 'strtelefone', 'strorgao']
    success_url = reverse_lazy('acoes_pngi:usuarioresponsavel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Responsável criado com sucesso!')
        return super().form_valid(form)


class UsuarioResponsavelUpdateView(LoginRequiredMixin, UpdateView):
    model = UsuarioResponsavel
    template_name = 'acoes_pngi/usuarioresponsavel/form.html'
    fields = ['strtelefone', 'strorgao']
    pk_url_kwarg = 'idusuario'
    success_url = reverse_lazy('acoes_pngi:usuarioresponsavel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Responsável atualizado com sucesso!')
        return super().form_valid(form)


class UsuarioResponsavelDeleteView(LoginRequiredMixin, DeleteView):
    model = UsuarioResponsavel
    template_name = 'acoes_pngi/usuarioresponsavel/confirm_delete.html'
    pk_url_kwarg = 'idusuario'
    success_url = reverse_lazy('acoes_pngi:usuarioresponsavel_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Responsável excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============= RELACAO ACAO USUARIO RESPONSAVEL VIEWS =============
class RelacaoAcaoUsuarioResponsavelListView(LoginRequiredMixin, ListView):
    model = RelacaoAcaoUsuarioResponsavel
    template_name = 'acoes_pngi/relacaoacaousuarioresponsavel/list.html'
    context_object_name = 'relacoes'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related(
            'idacao', 'idusuarioresponsavel__idusuario'
        )


class RelacaoAcaoUsuarioResponsavelDetailView(LoginRequiredMixin, DetailView):
    model = RelacaoAcaoUsuarioResponsavel
    template_name = 'acoes_pngi/relacaoacaousuarioresponsavel/detail.html'
    context_object_name = 'relacao'
    pk_url_kwarg = 'idacaousuarioresponsavel'


class RelacaoAcaoUsuarioResponsavelCreateView(LoginRequiredMixin, CreateView):
    model = RelacaoAcaoUsuarioResponsavel
    template_name = 'acoes_pngi/relacaoacaousuarioresponsavel/form.html'
    fields = ['idacao', 'idusuarioresponsavel']
    success_url = reverse_lazy('acoes_pngi:relacaoacaousuarioresponsavel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Relação criada com sucesso!')
        return super().form_valid(form)


class RelacaoAcaoUsuarioResponsavelUpdateView(LoginRequiredMixin, UpdateView):
    model = RelacaoAcaoUsuarioResponsavel
    template_name = 'acoes_pngi/relacaoacaousuarioresponsavel/form.html'
    fields = ['idacao', 'idusuarioresponsavel']
    pk_url_kwarg = 'idacaousuarioresponsavel'
    success_url = reverse_lazy('acoes_pngi:relacaoacaousuarioresponsavel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Relação atualizada com sucesso!')
        return super().form_valid(form)


class RelacaoAcaoUsuarioResponsavelDeleteView(LoginRequiredMixin, DeleteView):
    model = RelacaoAcaoUsuarioResponsavel
    template_name = 'acoes_pngi/relacaoacaousuarioresponsavel/confirm_delete.html'
    pk_url_kwarg = 'idacaousuarioresponsavel'
    success_url = reverse_lazy('acoes_pngi:relacaoacaousuarioresponsavel_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Relação excluída com sucesso!')
        return super().delete(request, *args, **kwargs)
