"""
Serviços compartilhados da aplicação Common.
"""

from .portal_auth import get_portal_auth_service, PortalAuthService

__all__ = [
    'get_portal_auth_service',
    'PortalAuthService',
]
