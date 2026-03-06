# acoes_pngi/permissions.py - VERSÃO REFATORADA

from rest_framework.permissions import BasePermission
from accounts.models import Aplicacao, UserRole
from accounts.services.authorization_service import get_authorization_service

# ============================================================================
# PERMISSÕES ESPECIALIZADAS PNGI (Lógica de negócio específica)
# ============================================================================

class IsGestorPNGI(BasePermission):
    """
    Permissão para CONFIGURAÇÕES CRÍTICAS.
    
    Regras:
    - SAFE_METHODS: Todas as 4 roles podem acessar
    - CREATE/UPDATE/DELETE: Apenas GESTOR_PNGI
    
    Mantida porque implementa lógica de negócio específica de hierarquia PNGI.
    """
    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in self.SAFE_METHODS:
            try:
                app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
                if not app_acoes:
                    return False

                has_any_role = UserRole.objects.filter(
                    user=request.user, aplicacao=app_acoes
                ).exists()

                return has_any_role
            except Exception:
                return False

        # CREATE/UPDATE/DELETE: apenas GESTOR
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
            if not app_acoes:
                return False

            allowed_roles = UserRole.objects.filter(
                user=request.user, aplicacao=app_acoes, role__codigoperfil="GESTOR_PNGI"
            ).exists()

            return allowed_roles
        except Exception:
            return False


class IsGestorPNGIOnly(BasePermission):
    """
    Permissão EXCLUSIVA para GESTOR_PNGI (leitura E escrita).
    
    Usada para: UserManagementViewSet
    Mantida porque é regra de negócio específica (gestão de usuários).
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
            if not app_acoes:
                return False

            return UserRole.objects.filter(
                user=request.user, aplicacao=app_acoes, role__codigoperfil="GESTOR_PNGI"
            ).exists()
        except Exception:
            return False


class IsCoordernadorOrGestorPNGI(BasePermission):
    """
    Permissão para CONFIGURAÇÕES COMPARTILHADAS.
    
    Regras:
    - SAFE_METHODS: Todas as 4 roles
    - CREATE/UPDATE/DELETE: GESTOR_PNGI e COORDENADOR_PNGI
    
    Mantida porque implementa hierarquia de negócio específica.
    """
    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in self.SAFE_METHODS:
            try:
                app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
                if not app_acoes:
                    return False

                has_any_role = UserRole.objects.filter(
                    user=request.user, aplicacao=app_acoes
                ).exists()

                return has_any_role
            except Exception:
                return False

        try:
            app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
            if not app_acoes:
                return False

            allowed_roles = UserRole.objects.filter(
                user=request.user,
                aplicacao=app_acoes,
                role__codigoperfil__in=["COORDENADOR_PNGI", "GESTOR_PNGI"],
            ).exists()

            return allowed_roles
        except Exception:
            return False


class IsCoordernadorGestorOrOperadorPNGI(BasePermission):
    """
    Permissão para OPERAÇÕES.
    
    Regras:
    - SAFE_METHODS: Todas as 4 roles
    - CREATE/UPDATE/DELETE: GESTOR_PNGI, COORDENADOR_PNGI e OPERADOR_ACAO
    
    Mantida porque implementa hierarquia de negócio específica.
    """
    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in self.SAFE_METHODS:
            try:
                app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
                if not app_acoes:
                    return False

                has_any_role = UserRole.objects.filter(
                    user=request.user, aplicacao=app_acoes
                ).exists()

                return has_any_role
            except Exception:
                return False

        try:
            app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
            if not app_acoes:
                return False

            allowed_roles = UserRole.objects.filter(
                user=request.user,
                aplicacao=app_acoes,
                role__codigoperfil__in=[
                    "COORDENADOR_PNGI",
                    "GESTOR_PNGI",
                    "OPERADOR_ACAO",
                    "OPERADOR_PNGI",
                ],
            ).exists()

            return allowed_roles
        except Exception:
            return False


class IsAnyPNGIRole(BasePermission):
    """
    Permissão UNIVERSAL para qualquer usuário com role PNGI.
    
    Mantida porque é check rápido de "tem alguma role PNGI".
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
            if not app_acoes:
                return False

            has_pngi_role = UserRole.objects.filter(
                user=request.user,
                aplicacao=app_acoes,
                role__codigoperfil__in=[
                    "COORDENADOR_PNGI",
                    "GESTOR_PNGI",
                    "OPERADOR_ACAO",
                    "OPERADOR_PNGI",
                    "CONSULTOR_PNGI",
                ],
            ).exists()

            return has_pngi_role
        except Exception:
            return False


# ============================================================================
# PERMISSÕES BASEADAS EM AuthorizationService
# ============================================================================

class IsAcoesPNGIUser(BasePermission):
    """
    🔄 MIGRADO: Agora usa AuthorizationService quando disponível.
    
    Verifica se usuário tem qualquer acesso à aplicação Ações PNGI.
    Aceita qualquer perfil PNGI.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Usar AuthorizationService se token_payload disponível
        token_payload = getattr(request, "token_payload", {})
        if token_payload:
            app_code = token_payload.get("app_code")
            active_role_id = token_payload.get("active_role_id")
            
            if app_code == "ACOES_PNGI" and active_role_id:
                # Usuário tem role ativa = tem acesso
                return True

        # Fallback: verifica diretamente no banco (para testes e sessões)
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
            if not app_acoes:
                return False

            has_role = UserRole.objects.filter(
                user=user,
                aplicacao=app_acoes,
                role__codigoperfil__in=[
                    "COORDENADOR_PNGI",
                    "GESTOR_PNGI",
                    "OPERADOR_ACAO",
                    "OPERADOR_PNGI",
                    "CONSULTOR_PNGI",
                ],
            ).exists()

            return has_role

        except Exception:
            return False


class CanViewAcoesPngi(IsAcoesPNGIUser):
    """
    Permissão para visualização (leitura).
    Herda de IsAcoesPNGIUser - qualquer usuário com acesso pode visualizar.
    """
    pass


class CanEditAcoesPngi(BasePermission):
    """
    🔄 MIGRADO: Agora usa AuthorizationService.
    
    Permissão para edição de ações.
    Permite: COORDENADOR_PNGI, GESTOR_PNGI, OPERADOR_ACAO.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Usar AuthorizationService se disponível
        token_payload = getattr(request, "token_payload", {})
        if token_payload:
            app_code = token_payload.get("app_code")
            active_role_id = token_payload.get("active_role_id")
            
            if app_code == "ACOES_PNGI" and active_role_id:
                auth_service = get_authorization_service()
                # Verifica permissão de mudança em qualquer modelo (generic check)
                # Para check específico, views devem usar HasModelPermission
                try:
                    from accounts.models import Role
                    role = Role.objects.get(id=active_role_id)
                    return role.codigoperfil in [
                        "COORDENADOR_PNGI", 
                        "GESTOR_PNGI", 
                        "OPERADOR_ACAO", 
                        "OPERADOR_PNGI"
                    ]
                except:
                    return False

        # Fallback: verifica diretamente no banco
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
            if not app_acoes:
                return False

            has_role = UserRole.objects.filter(
                user=user,
                aplicacao=app_acoes,
                role__codigoperfil__in=[
                    "COORDENADOR_PNGI",
                    "GESTOR_PNGI",
                    "OPERADOR_ACAO",
                    "OPERADOR_PNGI",
                ],
            ).exists()

            return has_role

        except Exception:
            return False


class CanManageAcoesPngi(BasePermission):
    """
    🔄 MIGRADO: Agora usa AuthorizationService.
    
    Permissão para gerenciamento completo.
    Permite: COORDENADOR_PNGI, GESTOR_PNGI.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Usar AuthorizationService se disponível
        token_payload = getattr(request, "token_payload", {})
        if token_payload:
            app_code = token_payload.get("app_code")
            active_role_id = token_payload.get("active_role_id")
            
            if app_code == "ACOES_PNGI" and active_role_id:
                try:
                    from accounts.models import Role
                    role = Role.objects.get(id=active_role_id)
                    return role.codigoperfil in ["COORDENADOR_PNGI", "GESTOR_PNGI"]
                except:
                    return False

        # Fallback: verifica diretamente no banco
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno="ACOES_PNGI").first()
            if not app_acoes:
                return False

            has_role = UserRole.objects.filter(
                user=user,
                aplicacao=app_acoes,
                role__codigoperfil__in=["COORDENADOR_PNGI", "GESTOR_PNGI"],
            ).exists()

            return has_role

        except Exception:
            return False


# ============================================================================
# ✅ IMPORTAR DO SERVIÇO CENTRALIZADO
# ============================================================================

# Importar classes do AuthorizationService
from accounts.services.authorization_service import (
    HasModelPermission,
    ReadOnlyOrHasPermission,
)

# Nota: Usar HasModelPermission em vez de:
# - HasAcoesPermission (removida)
# - CanAddOnly (removida)
# - HasSpecificPermission/CanAddEixo/CanChangeEixo/CanDeleteEixo (removidas)
#
# Exemplo de uso nas views:
# class EixoViewSet(viewsets.ModelViewSet):
#     permission_classes = [HasModelPermission]
#     permission_model = 'eixo'
