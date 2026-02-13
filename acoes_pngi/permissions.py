from rest_framework.permissions import BasePermission
from accounts.models import UserRole, Aplicacao


# ============================================================================
# PERMISSÕES PARA TESTES AUTOMATIZADOS (Novo)
# ============================================================================

class IsGestorPNGI(BasePermission):
    """
    Permissão para CONFIGURAÇÕES CRÍTICAS e GESTÃO DE USUÁRIOS.
    
    Usada para: SituacaoAcao, TipoEntraveAlerta, UserManagementViewSet
    
    Regras:
    - SAFE_METHODS (GET, HEAD, OPTIONS): Todas as 4 roles podem acessar
    - CREATE/UPDATE/DELETE: Apenas GESTOR_PNGI
    - COORDENADOR_PNGI: Bloqueado em escrita (não gerencia estas configurações)
    - OPERADOR_ACAO: Bloqueado em escrita (só gerencia ações)
    - CONSULTOR_PNGI: Bloqueado em escrita (apenas leitura)
    
    Hierarquia:
    GESTOR_PNGI (escrita) > COORDENADOR_PNGI (leitura) > OPERADOR_ACAO (leitura) > CONSULTOR_PNGI (leitura)
    """
    
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
    
    def has_permission(self, request, view):
        # Usuário deve estar autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # SAFE_METHODS: qualquer usuário autenticado com role PNGI
        if request.method in self.SAFE_METHODS:
            try:
                app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
                if not app_acoes:
                    return False
                
                has_any_role = UserRole.objects.filter(
                    user=request.user,
                    aplicacao=app_acoes
                ).exists()
                
                return has_any_role
            except Exception:
                return False
        
        # CREATE/UPDATE/DELETE: apenas GESTOR
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
            if not app_acoes:
                return False
            
            allowed_roles = UserRole.objects.filter(
                user=request.user,
                aplicacao=app_acoes,
                role__codigoperfil='GESTOR_PNGI'
            ).exists()
            
            return allowed_roles
        except Exception:
            return False


class IsCoordernadorOrGestorPNGI(BasePermission):
    """
    Permissão para CONFIGURAÇÕES COMPARTILHADAS.
    
    Usada para: Eixo, VigenciaPNGI, TipoAnotacaoAlinhamento
    
    Regras:
    - SAFE_METHODS (GET, HEAD, OPTIONS): Todas as 4 roles podem acessar
    - CREATE/UPDATE/DELETE: GESTOR_PNGI e COORDENADOR_PNGI
    - OPERADOR_ACAO: Bloqueado em escrita (só gerencia ações)
    - CONSULTOR_PNGI: Bloqueado em escrita (apenas leitura)
    
    Hierarquia:
    GESTOR_PNGI (escrita) = COORDENADOR_PNGI (escrita) > OPERADOR_ACAO (leitura) > CONSULTOR_PNGI (leitura)
    """
    
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
    
    def has_permission(self, request, view):
        # Usuário deve estar autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # SAFE_METHODS: qualquer usuário autenticado com role PNGI
        if request.method in self.SAFE_METHODS:
            try:
                app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
                if not app_acoes:
                    return False
                
                has_any_role = UserRole.objects.filter(
                    user=request.user,
                    aplicacao=app_acoes
                ).exists()
                
                return has_any_role
            except Exception:
                return False
        
        # CREATE/UPDATE/DELETE: apenas COORDENADOR e GESTOR
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
            if not app_acoes:
                return False
            
            allowed_roles = UserRole.objects.filter(
                user=request.user,
                aplicacao=app_acoes,
                role__codigoperfil__in=['COORDENADOR_PNGI', 'GESTOR_PNGI']
            ).exists()
            
            return allowed_roles
        except Exception:
            return False


class IsCoordernadorGestorOrOperadorPNGI(BasePermission):
    """
    Permissão para OPERAÇÕES.
    
    Usada para: Acoes, AcaoPrazo, AcaoDestaque, AcaoAnotacaoAlinhamento,
                UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel
    
    Regras:
    - SAFE_METHODS (GET, HEAD, OPTIONS): Todas as 4 roles podem acessar
    - CREATE/UPDATE/DELETE: GESTOR_PNGI, COORDENADOR_PNGI e OPERADOR_ACAO
    - CONSULTOR_PNGI: Bloqueado em escrita (apenas leitura)
    
    Hierarquia:
    GESTOR_PNGI (escrita) = COORDENADOR_PNGI (escrita) = OPERADOR_ACAO (escrita) > CONSULTOR_PNGI (leitura)
    """
    
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
    
    def has_permission(self, request, view):
        # Usuário deve estar autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # SAFE_METHODS: qualquer usuário autenticado com role PNGI
        if request.method in self.SAFE_METHODS:
            try:
                app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
                if not app_acoes:
                    return False
                
                has_any_role = UserRole.objects.filter(
                    user=request.user,
                    aplicacao=app_acoes
                ).exists()
                
                return has_any_role
            except Exception:
                return False
        
        # CREATE/UPDATE/DELETE: COORDENADOR, GESTOR e OPERADOR
        # NOTA: Aceita tanto OPERADOR_ACAO quanto OPERADOR_PNGI (alias para testes)
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
            if not app_acoes:
                return False
            
            allowed_roles = UserRole.objects.filter(
                user=request.user,
                aplicacao=app_acoes,
                role__codigoperfil__in=['COORDENADOR_PNGI', 'GESTOR_PNGI', 'OPERADOR_ACAO', 'OPERADOR_PNGI']
            ).exists()
            
            return allowed_roles
        except Exception:
            return False


class IsAnyPNGIRole(BasePermission):
    """
    Permissão UNIVERSAL para qualquer usuário com role PNGI.
    
    Regras:
    - Qualquer uma das 4 roles tem acesso: COORDENADOR_PNGI, GESTOR_PNGI, OPERADOR_ACAO, CONSULTOR_PNGI
    - Usuário sem role PNGI é negado
    - Não diferencia entre SAFE_METHODS e escrita (cada ViewSet deve usar outras permissions para isso)
    """
    
    def has_permission(self, request, view):
        # Usuário deve estar autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verificar se tem alguma role PNGI
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
            if not app_acoes:
                return False
            
            has_pngi_role = UserRole.objects.filter(
                user=request.user,
                aplicacao=app_acoes,
                role__codigoperfil__in=[
                    'COORDENADOR_PNGI',
                    'GESTOR_PNGI',
                    'OPERADOR_ACAO',
                    'OPERADOR_PNGI',  # Alias para testes
                    'CONSULTOR_PNGI'
                ]
            ).exists()
            
            return has_pngi_role
        except Exception:
            return False


# ============================================================================
# PERMISSÕES HIERÁRQUICAS (para testes)
# ============================================================================

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
                r['role__code'] in ['COORDENADOR_PNGI', 'GESTOR_PNGI', 'OPERADOR_ACAO', 'OPERADOR_PNGI', 'CONSULTOR_PNGI']
                for r in roles
            )
            return has_role
        
        # Fallback: verifica diretamente no banco (para testes e sessões)
        try:
            app_acoes = Aplicacao.objects.filter(codigointerno='ACOES_PNGI').first()
            if not app_acoes:
                return False
            
            has_role = UserRole.objects.filter(
                user=user,
                aplicacao=app_acoes,
                role__codigoperfil__in=['COORDENADOR_PNGI', 'GESTOR_PNGI', 'OPERADOR_ACAO', 'OPERADOR_PNGI', 'CONSULTOR_PNGI']
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
                r['role__code'] in ['COORDENADOR_PNGI', 'GESTOR_PNGI', 'OPERADOR_ACAO', 'OPERADOR_PNGI']
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
                role__codigoperfil__in=['COORDENADOR_PNGI', 'GESTOR_PNGI', 'OPERADOR_ACAO', 'OPERADOR_PNGI']
            ).exists()
            
            return has_role
            
        except Exception:
            return False


class CanManageAcoesPngi(BasePermission):
    """
    Permissão para gerenciamento completo (incluindo configurações).
    Permite: COORDENADOR_PNGI, GESTOR_PNGI.
    Bloqueia: OPERADOR_ACAO (apenas ações), CONSULTOR_PNGI (apenas leitura).
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


# ============================================================================
# PERMISSÕES EXISTENTES (mantidas para compatibilidade)
# ============================================================================

class CanManageCarga(BasePermission):
    """Alias para manter compatibilidade com código antigo"""
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        roles = request.auth.get('roles', []) if hasattr(request, 'auth') else []
        has_role = any(
            r['application__code'] == 'ACOES_PNGI' and r['role__code'] == 'GESTOR_PNGI'
            for r in roles
        )
        if not has_role:
            return False

        attrs = request.auth.get('attrs', [])
        for a in attrs:
            if (
                a['application__code'] == 'ACOES_PNGI'
                and a['key'] == 'can_upload'
                and a['value'].lower() == 'true'
            ):
                return True
        return False


# ============================================================================
# PERMISSÕES BASEADAS NO SISTEMA NATIVO DO DJANGO
# ============================================================================

class HasAcoesPermission(BasePermission):
    """
    Verifica permissões usando sistema nativo do Django
    Usa automaticamente o model da ViewSet
    """
    
    permission_map = {
        'GET': 'view',
        'HEAD': 'view',
        'OPTIONS': 'view',
        'POST': 'add',
        'PUT': 'change',
        'PATCH': 'change',
        'DELETE': 'delete',
    }
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if hasattr(view, 'queryset') and view.queryset is not None:
            model_name = view.queryset.model._meta.model_name
        else:
            return False
        
        action = self.permission_map.get(request.method, 'view')
        perm_codename = f'{action}_{model_name}'
        
        return request.user.has_app_perm('ACOES_PNGI', perm_codename)
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsGestorPNGILegacy(BasePermission):
    """Apenas gestores PNGI têm acesso (versão antiga sem SAFE_METHODS)"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        user_role = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).select_related('role').first()
        
        return user_role and user_role.role.codigoperfil == 'GESTOR_PNGI'


class IsCoordenadorOrAbove(BasePermission):
    """Coordenadores e Gestores têm acesso"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        user_role = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).select_related('role').first()
        
        allowed_roles = ['GESTOR_PNGI', 'COORDENADOR_PNGI']
        return user_role and user_role.role.codigoperfil in allowed_roles


class ReadOnly(BasePermission):
    """Permite apenas métodos de leitura (GET, HEAD, OPTIONS)"""
    
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS']


class CanAddOnly(BasePermission):
    """Permite apenas criar novos registros (POST)"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if request.method in ['GET', 'HEAD', 'OPTIONS', 'POST']:
            if hasattr(view, 'queryset') and view.queryset is not None:
                model_name = view.queryset.model._meta.model_name
                
                if request.method == 'POST':
                    return request.user.has_app_perm('ACOES_PNGI', f'add_{model_name}')
                else:
                    return request.user.has_app_perm('ACOES_PNGI', f'view_{model_name}')
        
        return False


class HasSpecificPermission(BasePermission):
    """Classe base para criar permissões específicas rapidamente"""
    required_permission = None
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if not self.required_permission:
            return False
        
        return request.user.has_app_perm('ACOES_PNGI', self.required_permission)


class CanAddEixo(HasSpecificPermission):
    """Permite apenas adicionar eixos"""
    required_permission = 'add_eixo'


class CanChangeEixo(HasSpecificPermission):
    """Permite apenas modificar eixos"""
    required_permission = 'change_eixo'


class CanDeleteEixo(HasSpecificPermission):
    """Permite apenas deletar eixos"""
    required_permission = 'delete_eixo'
