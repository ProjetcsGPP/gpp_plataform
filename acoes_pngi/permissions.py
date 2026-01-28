from rest_framework.permissions import BasePermission


# ============================================================================
# PERMISSÕES EXISTENTES (mantidas)
# ============================================================================

class CanManageCarga(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # RBAC: checa se usuário tem role 'GESTOR_PNGI' para esta aplicação
        roles = request.auth.get('roles', []) if hasattr(request, 'auth') else []
        has_role = any(
            r['application__code'] == 'ACOES_PNGI' and r['role__code'] == 'GESTOR_PNGI'
            for r in roles
        )
        if not has_role:
            return False

        # ABAC simples: atributo 'can_upload' == 'true'
        attrs = request.auth.get('attrs', [])
        for a in attrs:
            if (
                a['application__code'] == 'ACOES_PNGI'
                and a['key'] == 'can_upload'
                and a['value'].lower() == 'true'
            ):
                return True
        return False


class IsAcoesPNGIUser(BasePermission):
    """
    Permissão para usuários do app Ações PNGI
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verifica se o usuário tem role para a aplicação ACOESPNGI
        from accounts.models import UserRole, Aplicacao
        
        try:
            app = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
            return UserRole.objects.filter(
                user=request.user,
                aplicacao=app
            ).exists()
        except Aplicacao.DoesNotExist:
            return False


# ============================================================================
# NOVAS PERMISSÕES (baseadas no sistema nativo do Django)
# ============================================================================

class HasAcoesPermission(BasePermission):
    """
    Verifica permissões usando sistema nativo do Django
    Usa automaticamente o model da ViewSet
    
    Uso:
    class EixoViewSet(viewsets.ModelViewSet):
        permission_classes = [HasAcoesPermission]
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
        
        # Inferir model da view
        if hasattr(view, 'queryset') and view.queryset is not None:
            model_name = view.queryset.model._meta.model_name
        else:
            return False
        
        # Construir codename (ex: add_eixo)
        action = self.permission_map.get(request.method, 'view')
        perm_codename = f'{action}_{model_name}'
        
        # Verificar usando o helper do User
        return request.user.has_app_perm('ACOES_PNGI', perm_codename)
    
    def has_object_permission(self, request, view, obj):
        # Se tem permissão de model, tem de objeto
        return self.has_permission(request, view)


class IsGestorPNGI(BasePermission):
    """
    Apenas gestores PNGI têm acesso
    
    Uso:
    class ConfiguracoesViewSet(viewsets.ModelViewSet):
        permission_classes = [IsGestorPNGI]
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        from accounts.models import UserRole
        user_role = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).select_related('role').first()
        
        return user_role and user_role.role.codigoperfil == 'GESTOR_PNGI'


class IsCoordenadorOrAbove(BasePermission):
    """
    Coordenadores e Gestores têm acesso
    
    Uso:
    class RelatoriosViewSet(viewsets.ModelViewSet):
        permission_classes = [IsCoordenadorOrAbove]
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        from accounts.models import UserRole
        user_role = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).select_related('role').first()
        
        allowed_roles = ['GESTOR_PNGI', 'COORDENADOR_PNGI']
        return user_role and user_role.role.codigoperfil in allowed_roles


class ReadOnly(BasePermission):
    """
    Permite apenas métodos de leitura (GET, HEAD, OPTIONS)
    
    Uso:
    class PublicDataViewSet(viewsets.ModelViewSet):
        permission_classes = [IsAuthenticated, ReadOnly]
    """
    
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS']


class CanAddOnly(BasePermission):
    """
    Permite apenas criar novos registros (POST)
    Útil para operadores que só podem criar ações
    
    Uso:
    class AcaoViewSet(viewsets.ModelViewSet):
        permission_classes = [CanAddOnly]
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Permite GET (listar/detalhe) e POST (criar)
        if request.method in ['GET', 'HEAD', 'OPTIONS', 'POST']:
            if hasattr(view, 'queryset') and view.queryset is not None:
                model_name = view.queryset.model._meta.model_name
                
                if request.method == 'POST':
                    return request.user.has_app_perm('ACOES_PNGI', f'add_{model_name}')
                else:
                    return request.user.has_app_perm('ACOES_PNGI', f'view_{model_name}')
        
        return False


class HasSpecificPermission(BasePermission):
    """
    Classe base para criar permissões específicas rapidamente
    
    Uso:
    class CanDeleteEixo(HasSpecificPermission):
        required_permission = 'delete_eixo'
    """
    required_permission = None
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if not self.required_permission:
            return False
        
        return request.user.has_app_perm('ACOES_PNGI', self.required_permission)


# Exemplos de permissões específicas usando a classe base
class CanAddEixo(HasSpecificPermission):
    """Permite apenas adicionar eixos"""
    required_permission = 'add_eixo'


class CanChangeEixo(HasSpecificPermission):
    """Permite apenas modificar eixos"""
    required_permission = 'change_eixo'


class CanDeleteEixo(HasSpecificPermission):
    """Permite apenas deletar eixos"""
    required_permission = 'delete_eixo'
