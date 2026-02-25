"""
acoes_pngi/mixins.py

Mixin para Web Views usar AuthorizationService.
"""

from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.services import get_authorization_service
import logging

logger = logging.getLogger(__name__)


class AuthorizationPermissionMixin(LoginRequiredMixin):
    """
    🔑 Mixin para Web Views.
    
    Uso:
        class EixoWebCreateView(AuthorizationPermissionMixin, CreateView):
            model = Eixo
            permission_model = 'eixo'  # ← Mesmo das API Views
            permission_action = 'add'  # add/view/change/delete
    
    Extrai token_payload do middleware ou sessão.
    """
    
    permission_model = None  # ← Obrigatório (ex: 'eixo')
    permission_action = 'view'  # ← add/view/change/delete
    
    def dispatch(self, request, *args, **kwargs):
        # Superusuário sempre passa
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        # Verificar autenticação PNGI
        if not hasattr(request.user, 'id') or not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # Extrair token_payload (middleware JWT)
        token_payload = getattr(request, 'token_payload', {})
        user_id = request.user.id
        app_code = token_payload.get('app_code', 'ACOES_PNGI')
        active_role_id = token_payload.get('active_role_id')
        
        if not all([user_id, active_role_id]):
            logger.warning(f"Token inválido para web view: user_id={user_id}")
            return self.handle_no_permission()
        
        # 🆕 AuthorizationService
        auth_service = get_authorization_service()
        has_perm = auth_service.can(
            user_id=user_id,
            app_code=app_code,
            active_role_id=active_role_id,
            action=self.permission_action,
            model_name=self.permission_model
        )
        
        if not has_perm:
            logger.info(
                f"Acesso negado WEB: user={user_id}, action={self.permission_action}, "
                f"model={self.permission_model}"
            )
            return HttpResponseForbidden("Você não tem permissão para esta operação.")
        
        logger.debug(f"✅ WEB autorizado: user={user_id}, {self.permission_action}_{self.permission_model}")
        return super().dispatch(request, *args, **kwargs)


class ReadOnlyWebMixin(AuthorizationPermissionMixin):
    """Mixin para views apenas leitura."""
    
    permission_action = 'view'


class CreateUpdateWebMixin(AuthorizationPermissionMixin):
    """Mixin para create/update."""
    
    permission_action = 'add'
    
    def get_permission_action(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return 'add' if self.request.path.endswith('create/') else 'change'
        return 'view'


class DeleteWebMixin(AuthorizationPermissionMixin):
    """Mixin para delete."""
    
    permission_action = 'delete'
