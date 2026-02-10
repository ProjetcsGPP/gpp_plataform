"""
Responsavel Web Views - Class-Based Views para gerenciamento de responsáveis.
Inclui: UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from ...models import UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel


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
