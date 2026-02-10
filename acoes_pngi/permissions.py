from rest_framework.permissions import BasePermission
from accounts.models import UserRole, Role, Aplicacao


class IsAcoesPNGIUser(BasePermission):
    """
    Permissão base para verificar se usuário tem qualquer acesso à aplicação Ações PNGI.
    Aceita qualquer um dos 4 perfis: COORDENADOR_PNGI, GESTOR_PNGI, OPERADOR_ACAO, CONSULTOR_PNGI.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Tenta via JWT (request.auth)
        if hasattr(request, 'auth') and request.auth:
            roles = request.auth.get('roles', [])
            has_role = any(
                r['application__code'] == 'ACOES_PNGI' and 
                r['role__code'] in ['COORDENADOR_PNGI', 'GESTOR_PNGI', 'OPERADOR_ACAO', 'CONSULTOR_PNGI']
                for r in roles
            )
            return has_role
        
        # Fallback: verifica diretamente no banco (para testes e sessões)
        try:
            # Busca aplicação ACOES_PNGI (campo correto: codigointerno)
            app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
            if not app_acoes:
                return False
            
            # Verifica se usuário tem qualquer role da aplicação
            has_role = UserRole.objects.filter(
                user=user,
                aplicacao=app_acoes,
                role__codigoperfil__in=['COORDENADOR_PNGI', 'GESTOR_PNGI', 'OPERADOR_ACAO', 'CONSULTOR_PNGI']
            ).exists()
            
            return has_role
            
        except Exception:
            return False


class CanViewAcoesPngi(IsAcoesPNGIUser):
    """
    Permissão para visualização (leitura).
    Permite acesso a TODOS os perfis: COORDENADOR_PNGI, GESTOR_PNGI, OPERADOR_ACAO, CONSULTOR_PNGI.
    
    Herda de IsAcoesPNGIUser, então qualquer usuário com acesso à aplicação pode visualizar.
    """
    pass


class CanEditAcoesPngi(BasePermission):
    """
    Permissão para edição de ações.
    Permite: COORDENADOR_PNGI, GESTOR_PNGI, OPERADOR_ACAO.
    Bloqueia: CONSULTOR_PNGI (apenas leitura).
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Tenta via JWT (request.auth)
        if hasattr(request, 'auth') and request.auth:
            roles = request.auth.get('roles', [])
            has_role = any(
                r['application__code'] == 'ACOES_PNGI' and 
                r['role__code'] in ['COORDENADOR_PNGI', 'GESTOR_PNGI', 'OPERADOR_ACAO']
                for r in roles
            )
            return has_role
        
        # Fallback: verifica diretamente no banco
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
            if not app_acoes:
                return False
            
            has_role = UserRole.objects.filter(
                user=user,
                aplicacao=app_acoes,
                role__codigoperfil__in=['COORDENADOR_PNGI', 'GESTOR_PNGI', 'OPERADOR_ACAO']
            ).exists()
            
            return has_role
            
        except Exception:
            return False


class CanManageAcoesPngi(BasePermission):
    """
    Permissão para gerenciamento completo (incluindo configurações).
    Permite: COORDENADOR_PNGI, GESTOR_PNGI.
    Bloqueia: OPERADOR_ACAO (apenas ações), CONSULTOR_PNGI (apenas leitura).
    
    Equivalente ao CanManageCarga do carga_org_lot.
    Usado para endpoints administrativos e configurações.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Tenta via JWT (request.auth)
        if hasattr(request, 'auth') and request.auth:
            roles = request.auth.get('roles', [])
            has_role = any(
                r['application__code'] == 'ACOES_PNGI' and 
                r['role__code'] in ['COORDENADOR_PNGI', 'GESTOR_PNGI']
                for r in roles
            )
            if not has_role:
                return False

            # Verifica atributo can_upload (se necessário para algumas operações)
            attrs = request.auth.get('attrs', [])
            for a in attrs:
                if (
                    a['application__code'] == 'ACOES_PNGI'
                    and a['key'] == 'can_upload'
                    and a['value'].lower() == 'true'
                ):
                    return True
            
            # Se tem role de gestor/coordenador, permite mesmo sem atributo específico
            return has_role
        
        # Fallback: verifica diretamente no banco
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
            if not app_acoes:
                return False
            
            has_role = UserRole.objects.filter(
                user=user,
                aplicacao=app_acoes,
                role__codigoperfil__in=['COORDENADOR_PNGI', 'GESTOR_PNGI']
            ).exists()
            
            return has_role
            
        except Exception:
            return False


# Alias para compatibilidade com código antigo
class CanManageCarga(CanManageAcoesPngi):
    """
    Alias para manter compatibilidade com código antigo.
    Herda exatamente a mesma lógica de CanManageAcoesPngi.
    """
    pass
