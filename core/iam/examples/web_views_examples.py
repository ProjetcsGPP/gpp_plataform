"""Example: Refactored Web Views

Examples of how to refactor traditional Django views
to use IAM decorators.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from core.iam.interfaces.decorators import (
    require_permission,
    require_any_permission,
    require_role,
)

# Assuming these imports
# from acoes_pngi.models import Eixo, Acoes
# from acoes_pngi.forms import EixoForm, AcoesForm


# ============================================================================
# FUNCTION-BASED VIEWS
# ============================================================================

@require_permission('ACOES_PNGI', 'view_eixo')
def eixo_list(request):
    """List all eixos - read permission required"""
    # eixos = Eixo.objects.all().order_by('stralias')
    # return render(request, 'acoes_pngi/eixo_list.html', {'eixos': eixos})
    return render(request, 'eixo_list.html', {})


@require_permission('ACOES_PNGI', 'add_eixo')
def eixo_create(request):
    """Create new eixo - add permission required"""
    # if request.method == 'POST':
    #     form = EixoForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Eixo criado com sucesso!')
    #         return redirect('acoes:eixo_list')
    # else:
    #     form = EixoForm()
    # return render(request, 'acoes_pngi/eixo_form.html', {'form': form})
    return render(request, 'eixo_form.html', {})


@require_any_permission('ACOES_PNGI', 'change_eixo', 'add_eixo')
def eixo_edit(request, pk):
    """Edit eixo - change OR add permission"""
    # eixo = get_object_or_404(Eixo, pk=pk)
    # if request.method == 'POST':
    #     form = EixoForm(request.POST, instance=eixo)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Eixo atualizado!')
    #         return redirect('acoes:eixo_list')
    # else:
    #     form = EixoForm(instance=eixo)
    # return render(request, 'acoes_pngi/eixo_form.html', {
    #     'form': form,
    #     'eixo': eixo
    # })
    return render(request, 'eixo_form.html', {})


@require_role('ACOES_PNGI', 'GESTOR_PNGI', 'COORDENADOR_PNGI')
def config_dashboard(request):
    """Configuration dashboard - only GESTOR and COORDENADOR"""
    # stats = {
    #     'total_eixos': Eixo.objects.count(),
    #     'total_acoes': Acoes.objects.count(),
    #     # ...
    # }
    # return render(request, 'acoes_pngi/config_dashboard.html', stats)
    return render(request, 'config_dashboard.html', {})


# ============================================================================
# CLASS-BASED VIEWS
# ============================================================================

from django.contrib.auth.mixins import UserPassesTestMixin
from core.iam.services import AuthorizationService


class IAMPermissionMixin(UserPassesTestMixin):
    """Mixin for CBVs that checks IAM permissions"""
    
    # Override these in your view
    app_code = 'ACOES_PNGI'
    required_permission = None
    required_roles = []
    
    def test_func(self):
        """Check if user has required permission or role"""
        user = self.request.user
        
        if not user or not user.is_authenticated:
            return False
        
        # Check permission if specified
        if self.required_permission:
            return AuthorizationService.user_has_permission(
                user, self.app_code, self.required_permission
            )
        
        # Check roles if specified
        if self.required_roles:
            return AuthorizationService.user_has_any_role(
                user, self.app_code, self.required_roles
            )
        
        return False
    
    def handle_no_permission(self):
        """Custom handling when permission denied"""
        messages.error(
            self.request,
            'Você não possui permissão para acessar esta página.'
        )
        return redirect('portal:dashboard')


class EixoListView(IAMPermissionMixin, ListView):
    """List view with IAM permission check"""
    # model = Eixo
    # template_name = 'acoes_pngi/eixo_list.html'
    # context_object_name = 'eixos'
    app_code = 'ACOES_PNGI'
    required_permission = 'view_eixo'
    
    # def get_queryset(self):
    #     return Eixo.objects.all().order_by('stralias')


class EixoCreateView(IAMPermissionMixin, CreateView):
    """Create view with IAM permission check"""
    # model = Eixo
    # form_class = EixoForm
    # template_name = 'acoes_pngi/eixo_form.html'
    # success_url = reverse_lazy('acoes:eixo_list')
    app_code = 'ACOES_PNGI'
    required_permission = 'add_eixo'
    
    def form_valid(self, form):
        messages.success(self.request, 'Eixo criado com sucesso!')
        return super().form_valid(form)


class EixoUpdateView(IAMPermissionMixin, UpdateView):
    """Update view with IAM permission check"""
    # model = Eixo
    # form_class = EixoForm
    # template_name = 'acoes_pngi/eixo_form.html'
    # success_url = reverse_lazy('acoes:eixo_list')
    app_code = 'ACOES_PNGI'
    required_permission = 'change_eixo'
    
    def form_valid(self, form):
        messages.success(self.request, 'Eixo atualizado!')
        return super().form_valid(form)


class ConfigDashboardView(IAMPermissionMixin, ListView):
    """Dashboard requiring specific roles"""
    # template_name = 'acoes_pngi/config_dashboard.html'
    app_code = 'ACOES_PNGI'
    required_roles = ['GESTOR_PNGI', 'COORDENADOR_PNGI']
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['stats'] = {
    #         'total_eixos': Eixo.objects.count(),
    #         'total_acoes': Acoes.objects.count(),
    #     }
    #     return context


# ============================================================================
# CHECKING PERMISSIONS IN TEMPLATE CONTEXT
# ============================================================================

def acao_detail(request, pk):
    """Detail view with permission checks for actions"""
    # acao = get_object_or_404(Acoes, pk=pk)
    
    # Check various permissions for showing/hiding UI elements
    context = {
        # 'acao': acao,
        'can_edit': AuthorizationService.user_has_permission(
            request.user, 'ACOES_PNGI', 'change_acoes'
        ),
        'can_delete': AuthorizationService.user_has_permission(
            request.user, 'ACOES_PNGI', 'delete_acoes'
        ),
        'is_gestor': AuthorizationService.user_has_role(
            request.user, 'ACOES_PNGI', 'GESTOR_PNGI'
        ),
    }
    
    # return render(request, 'acoes_pngi/acao_detail.html', context)
    return render(request, 'acao_detail.html', context)


# ============================================================================
# TEMPLATE USAGE EXAMPLE
# ============================================================================

"""
In templates, use the IAM context middleware:

{% if request.user_has_permission 'ACOES_PNGI' 'change_eixo' %}
    <a href="{% url 'acoes:eixo_edit' eixo.pk %}">Editar</a>
{% endif %}

{% if request.user_has_role 'ACOES_PNGI' 'GESTOR_PNGI' %}
    <a href="{% url 'acoes:config' %}">Configurações</a>
{% endif %}

Or create custom template tags:

# acoes_pngi/templatetags/iam_tags.py
from django import template
from core.iam.services import AuthorizationService

register = template.Library()

@register.simple_tag(takes_context=True)
def has_permission(context, app_code, permission):
    user = context['request'].user
    return AuthorizationService.user_has_permission(user, app_code, permission)

@register.simple_tag(takes_context=True)
def has_role(context, app_code, role_code):
    user = context['request'].user
    return AuthorizationService.user_has_role(user, app_code, role_code)

Then in template:
{% load iam_tags %}

{% has_permission 'ACOES_PNGI' 'change_eixo' as can_edit %}
{% if can_edit %}
    <a href="...">Editar</a>
{% endif %}
"""
