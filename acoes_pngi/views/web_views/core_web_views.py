"""
Core Web Views - Class-Based Views para entidades principais.
Inclui: Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from ...models import Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta


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
