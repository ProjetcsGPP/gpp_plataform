# portal/services/portal_authorization.py
"""
Portal Authorization Service - Valida acesso a aplicações via RBAC

Integra com accounts.services.authorization_service para validação centralizada.
"""

import logging
from typing import Optional

from accounts.models import Aplicacao, UserRole
from accounts.services.authorization_service import get_authorization_service

logger = logging.getLogger(__name__)


class PortalAuthorizationService:
    """
    Serviço de autorização específico do Portal.
    
    Responsável por validar:
    - Acesso a aplicações
    - Visualização de aplicações
    - Listagem de aplicações disponíveis
    """

    def __init__(self):
        self.auth_service = get_authorization_service()

    def user_can_access_application(
        self, user_id: int, app_code: str
    ) -> bool:
        """
        Verifica se o usuário tem acesso a uma aplicação específica.
        
        Args:
            user_id: ID do usuário
            app_code: Código interno da aplicação (ex: 'ACOES_PNGI')
            
        Returns:
            True se o usuário tem pelo menos uma role na aplicação
        """
        try:
            has_access = UserRole.objects.filter(
                user_id=user_id, 
                aplicacao__codigointerno=app_code
            ).exists()
            
            logger.debug(
                f"🔐 Access check: user={user_id}, app={app_code}, "
                f"result={has_access}"
            )
            
            return has_access
            
        except Exception as e:
            logger.error(
                f"💥 Error checking application access: {e}", 
                exc_info=True
            )
            return False

    def get_user_applications(self, user_id: int) -> list[dict]:
        """
        Retorna lista de aplicações que o usuário pode acessar.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Lista de dicionários com dados das aplicações
        """
        try:
            user_roles = UserRole.objects.filter(
                user_id=user_id
            ).select_related("aplicacao")

            # Remove duplicatas de aplicações
            apps_dict = {}
            for ur in user_roles:
                app = ur.aplicacao
                # ✅ CORRIGIDO: Verifica se app não é None antes de acessar atributos
                if app and app.idaplicacao not in apps_dict:
                    apps_dict[app.idaplicacao] = {
                        "id": app.idaplicacao,
                        "codigo": app.codigointerno,
                        "nome": app.nomeaplicacao,
                        "url": app.base_url or "",
                        "showInPortal": app.isshowinportal,
                    }

            # Retorna apenas apps que devem aparecer no portal
            applications = [
                app for app in apps_dict.values() 
                if app["showInPortal"]
            ]
            
            logger.info(
                f"📱 User {user_id} has access to {len(applications)} "
                f"applications"
            )
            
            return applications
            
        except Exception as e:
            logger.error(
                f"💥 Error getting user applications: {e}", 
                exc_info=True
            )
            return []

    def get_application_by_code(self, app_code: str) -> Optional[dict]:
        """
        Busca aplicação por código interno.
        
        Args:
            app_code: Código interno da aplicação
            
        Returns:
            Dicionário com dados da aplicação ou None
        """
        try:
            app = Aplicacao.objects.get(codigointerno=app_code)
            return {
                "id": app.idaplicacao,
                "codigo": app.codigointerno,
                "nome": app.nomeaplicacao,
                "url": app.base_url or "",
                "showInPortal": app.isshowinportal,
            }
        except Aplicacao.DoesNotExist:
            logger.warning(f"❌ Application not found: {app_code}")
            return None


# Singleton instance
_portal_auth_service: Optional[PortalAuthorizationService] = None


def get_portal_authorization_service() -> PortalAuthorizationService:
    """Factory para obter instância singleton do serviço."""
    global _portal_auth_service
    if _portal_auth_service is None:
        _portal_auth_service = PortalAuthorizationService()
    return _portal_auth_service
