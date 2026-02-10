"""
Acoes Web Views - Class-Based Views para gerenciamento de ações.
Inclui: Acoes, AcaoPrazo, AcaoDestaque.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Prefetch

from ...models import Acoes, AcaoPrazo, AcaoDestaque, RelacaoAcaoUsuarioResponsavel


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
