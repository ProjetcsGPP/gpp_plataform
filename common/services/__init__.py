"""
Serviços compartilhados da aplicação Common.
"""

from .portal_auth import PortalAuthService, get_portal_auth_service

__all__ = [
    "get_portal_auth_service",
    "PortalAuthService",
]
