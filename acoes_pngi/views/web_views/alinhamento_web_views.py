"""
Alinhamento Web Views - Class-Based Views para anotações de alinhamento.
Inclui: TipoAnotacaoAlinhamento, AcaoAnotacaoAlinhamento.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from ...models import TipoAnotacaoAlinhamento, AcaoAnotacaoAlinhamento


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
