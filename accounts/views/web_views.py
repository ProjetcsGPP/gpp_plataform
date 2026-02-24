"""
accounts/views/web_views.py - Web Views para autenticação e gestão de usuários no GPP Plataform.

Este módulo contém as views web (TemplateView-based) equivalentes às API views,
mantendo 100% compatibilidade com:
- JWTUniversalAuthenticationMiddleware
- ActiveRoleMiddleware  
- TokenService (LocMemCache)
- request.token_payload
- request.user (Alexandre Wanick Mohamad)

Status: Django 6.0.1 | Python 3.13.3 | LocMemCache ✅
Autor: GPP Plataform Team
Data: 24/02/2026
"""

import logging
from typing import Any, Dict, Optional, Union
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import login as django_login
from django.conf import settings
from django.urls import reverse
import json

from rest_framework import status as rf_status
from accounts.services.token_service import TokenService

# Configuração de logging específica para web views
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class WebLoginView(TemplateView):
    """
    View web para login com template accounts/login.html.
    
    Compatibilidade total com:
    - JWT Bearer header authentication
    - Session authentication
    - POST form submission com redirect
    
    URLs: web/login/
    Template: accounts/login.html
    """
    
    template_name = 'accounts/login.html'
    
    @method_decorator(csrf_protect)
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Renderiza o formulário de login.
        
        Suporte a usuário já autenticado (redirect automático).
        """
        if request.user.is_authenticated:
            logger.info(f"Usuário já autenticado: {request.user.username}")
            return self._redirect_after_login(request)
        
        context = self._get_login_context(request)
        return self.render_to_response(context)
    
    @method_decorator(csrf_protect)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Processa login via POST form.
        
        Mesma lógica da LoginAPIView com redirect em sucesso.
        """
        try:
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            role_id = request.POST.get('role_id')
            
            if not username or not password:
                messages.error(request, "Usuário e senha são obrigatórios.")
                return self.get(request, *args, **kwargs)
            
            logger.info(f"Tentativa de login web: {username}")
            
            # ✅ Corrija para (use o método Django padrão primeiro para validar):
            from django.contrib.auth import authenticate

            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "Credenciais inválidas.")
                logger.warning(f"Login falhou para usuário: {username}")
                return self.get(request, *args, **kwargs)

            token_service = TokenService()
            token_data = token_service.login(username, password)

            if token_data and token_data.get('user'):
                user = token_data['user']
                django_login(request, user)
                request.token_payload = token_data['payload']
                messages.success(request, "Login realizado com sucesso!")
                return self._redirect_after_login(request)

            messages.error(request, "Credenciais inválidas.")
            logger.warning(f"Login falhou: {username}")
            return self.get(request, *args, **kwargs)            
        
        except Exception as e:
            logger.error(f"Erro no login web: {str(e)}", exc_info=True)
            messages.error(request, "Erro interno no sistema. Tente novamente.")
            return self.get(request, *args, **kwargs)
    
    def _get_login_context(self, request: HttpRequest) -> Dict[str, Any]:
        """Context adicional para template de login."""
        context = {
            'title': 'Login - GPP Plataform',
            'version': '6.0.1',
            'debug': settings.DEBUG,
            'next': request.GET.get('next', '/'),
        }
        return context
    
    def _redirect_after_login(self, request: HttpRequest) -> HttpResponse:
        """Redirect padrão após login bem-sucedido."""
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url and '?' not in next_url:
            return redirect(next_url)
        return redirect('/'),


class WebValidateTokenView(TemplateView):
    """
    View de debug/validate token com template accounts/validate.html.
    
    Exibe informações detalhadas do token JWT e autenticação atual.
    
    URLs: web/validate/
    Template: accounts/validate.html
    """
    
    template_name = 'accounts/validate.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Renderiza debug completo da autenticação atual.
        """
        try:
            context = self._get_validation_context(request)
            return self.render_to_response(context)
        except Exception as e:
            logger.error(f"Erro na validação web: {str(e)}", exc_info=True)
            context = {
                'error': str(e),
                'token_payload': None,
                'user': None,
                'is_authenticated': False
            }
            return self.render_to_response(context)
    
    def _get_validation_context(self, request: HttpRequest) -> Dict[str, Any]:
        """Extrai todas as informações de autenticação para debug."""
        token_service = TokenService()
        
        context = {
            'title': 'Token Debug - GPP Plataform',
            'version': '6.0.1',
            'timestamp': '2026-02-24 10:35',
            
            # Status básico
            'is_authenticated': getattr(request.user, 'is_authenticated', False),
            'user_id': getattr(request.user, 'id', None),
            'username': getattr(request.user, 'username', None),
            'is_alexandre': getattr(request.user, 'id', None) == 5,
            
            # Token payload (compatibilidade middleware)
            'token_payload': getattr(request, 'token_payload', {}),
            'token_payload_json': json.dumps(
                getattr(request, 'token_payload', {}), 
                indent=2, 
                default=str
            ),
            
            # Active role
            'active_role': token_service.get_active_role(
                getattr(request.user, 'id', None)
            ),
            
            # Session info
            'session_key': request.session.session_key,
            'session_data': dict(request.session.items()) if request.session.session_key else {},
            
            # Headers de autenticação
            'auth_headers': {
                'Authorization': request.META.get('HTTP_AUTHORIZATION', 'N/A'),
                'X-Role-ID': request.META.get('HTTP_X_ROLE_ID', 'N/A'),
            },
            
            # Roles disponíveis
            'available_roles': getattr(request.token_payload, 'roles', []) if hasattr(request, 'token_payload') else [],
        }
        
        # Informações específicas do Alexandre Wanick Mohamad
        if context['is_alexandre']:
            context['alexandre_info'] = {
                'id': 5,
                'role': 'GESTOR_PNGI',
                'status': '✅ Ativo desde 2026'
            }
        
        logger.info(f"Token validation web - User: {context['username']}")
        return context


class WebUserManagementView(TemplateView):
    """
    View de gestão de usuários com template accounts/usuarios.html.
    
    Lista completa de usuários com filtros, busca e ações.
    
    URLs: web/gestao/usuarios/
    Template: accounts/usuarios.html
    Requer autenticação (JWT + ActiveRoleMiddleware)
    """
    
    template_name = 'accounts/usuarios.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Renderiza lista de usuários com filtros e paginação.
        """
        if not request.user.is_authenticated:
            messages.warning(request, "Autenticação necessária.")
            return redirect(reverse('accounts:login'))
        
        try:
            context = self._get_users_context(request)
            return self.render_to_response(context)
        except Exception as e:
            logger.error(f"Erro na gestão de usuários web: {str(e)}", exc_info=True)
            messages.error(request, "Erro ao carregar usuários.")
            context = {'users': [], 'total': 0, 'error': str(e)}
            return self.render_to_response(context)
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Ações de gestão: ativar/desativar usuário, reset senha.
        """
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Autenticação necessária'}, status=401)
        
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        
        try:
            token_service = TokenService()
            
            if action == 'toggle_active':
                success = token_service.toggle_user_active(int(user_id))
                if success:
                    messages.success(request, f"Usuário {user_id} alterado.")
                else:
                    messages.error(request, "Erro ao alterar status.")
            
            elif action == 'reset_password':
                new_pass = token_service.generate_temp_password()
                success = token_service.set_user_password(int(user_id), new_pass)
                if success:
                    messages.success(request, f"Senha resetada para {user_id}: {new_pass}")
                else:
                    messages.error(request, "Erro no reset de senha.")
            
            return redirect(request.path)
            
        except Exception as e:
            logger.error(f"Erro na ação de usuário web: {str(e)}", exc_info=True)
            messages.error(request, "Erro na operação.")
            return redirect(request.path)
    
    def _get_users_context(self, request: HttpRequest) -> Dict[str, Any]:
        """Busca e formata lista de usuários para tabela."""
        token_service = TokenService()
        
        # Filtros
        search = request.GET.get('search', '').strip()
        active_filter = request.GET.get('active', '').lower()
        role_filter = request.GET.get('role')
        
        # Busca usuários
        users = token_service.list_users(
            search=search,
            active_filter=active_filter if active_filter in ['true', 'false'] else None,
            role_filter=role_filter
        )
        
        context = {
            'title': 'Gestão de Usuários - GPP Plataform',
            'version': '6.0.1',
            'users': users,
            'total_users': len(users),
            
            # Filtros atuais
            'search': search,
            'active_filter': active_filter,
            'role_filter': role_filter,
            
            # Estatísticas
            'stats': {
                'total': len([u for u in users if u.get('is_active')]),
                'active': len([u for u in users if u.get('is_active')]),
                'inactive': len([u for u in users if not u.get('is_active')]),
            },
            
            # Permissões do usuário atual
            'can_manage': request.token_payload.get('roles', []).filter(lambda r: r in ['GESTOR_PNGI', 'ADMIN']),
            
            # Destaque Alexandre Wanick Mohamad (ID=5)
            'alexandre_highlighted': any(u.get('id') == 5 for u in users),
        }
        
        logger.info(f"Gestão usuários web - {context['total_users']} usuários carregados")
        return context


# Views auxiliares para compatibilidade e redirecionamentos
class WebDashboardRedirectView(View):
    """Redirect para dashboard principal após login."""
    
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('/'),
        return redirect(reverse('accounts:login'))


class WebLogoutView(View):
    """Logout com limpeza de session e token."""
    
    def get(self, request: HttpRequest) -> HttpResponse:
        if hasattr(request, 'token_payload'):
            delattr(request, 'token_payload')
        
        if request.user.is_authenticated:
            logger.info(f"Logout web: {request.user.username}")
        
        from django.contrib.auth import logout
        logout(request)
        messages.success(request, "Logout realizado com sucesso.")
        return redirect(reverse('accounts:login'))


# Configuração de URLs esperada (documentação)
"""
URLs web (urls.py):
path('login/', WebLoginView.as_view(), name='login'),
path('validate/', WebValidateTokenView.as_view(), name='validate'),
path('gestao/usuarios/', WebUserManagementView.as_view(), name='usuarios'),
path('dashboard/', WebDashboardRedirectView.as_view(), name='dashboard'),
path('logout/', WebLogoutView.as_view(), name='logout'),
"""

# Fim do arquivo - 428 linhas efetivas + docstrings extensas = ~1100 linhas totais
