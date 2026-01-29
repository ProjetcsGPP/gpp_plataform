# accounts/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from .models import UserRole

class ActiveRoleMiddleware:
    """
    Middleware que garante que o usuário tenha um papel ativo selecionado
    para a aplicação que está acessando
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs que não precisam de papel ativo
        self.exempt_urls = [
            '/accounts/login/',
            '/accounts/logout/',
            '/accounts/select-role/',
            '/admin/',
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        # Se não está autenticado ou URL isenta, prossegue
        if not request.user.is_authenticated or self._is_exempt(request.path):
            return self.get_response(request)
        
        # Pega código da aplicação atual da URL
        app_code = self._get_app_code_from_path(request.path)
        
        if app_code:
            # Verifica se existe papel ativo na sessão para esta aplicação
            session_key = f'active_role_{app_code}'
            active_role_id = request.session.get(session_key)
            
            # Valida se o papel ainda existe e pertence ao usuário
            if active_role_id:
                try:
                    active_role = UserRole.objects.select_related('role', 'aplicacao').get(
                        id=active_role_id,
                        user=request.user,
                        aplicacao__codigointerno=app_code
                    )
                    request.active_role = active_role
                except UserRole.DoesNotExist:
                    # Papel inválido, limpa sessão
                    del request.session[session_key]
                    return redirect('accounts:select_role', app_code=app_code)
            else:
                # Não tem papel ativo, redireciona para seleção
                return redirect('accounts:select_role', app_code=app_code)
        
        response = self.get_response(request)
        return response
    
    def _is_exempt(self, path):
        """Verifica se a URL está isenta"""
        return any(path.startswith(url) for url in self.exempt_urls)
    
    def _get_app_code_from_path(self, path):
        """Extrai código da aplicação da URL"""
        if path.startswith('/acoes-pngi/'):
            return 'ACOES_PNGI'
        elif path.startswith('/carga_org_lot/'):
            return 'CARGA_ORG_LOT'
        elif path.startswith('/portal/'):
            return 'PORTAL'
        return None
