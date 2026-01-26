from rest_framework.permissions import BasePermission

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
            app = Aplicacao.objects.get(codigointerno='ACOESPNGI')
            return UserRole.objects.filter(
                user=request.user,
                aplicacao=app
            ).exists()
        except Aplicacao.DoesNotExist:
            return False