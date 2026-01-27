# carga_org_lot/permissions.py
from rest_framework.permissions import BasePermission
from accounts.models import UserRole, Role, Aplicacao


class CanManageCarga(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Tenta via JWT (request.auth)
        if hasattr(request, 'auth') and request.auth:
            roles = request.auth.get('roles', [])
            has_role = any(
                r['application__code'] == 'CARGA_ORG_LOT' and r['role__code'] == 'GESTOR_CARGA'
                for r in roles
            )
            if not has_role:
                return False

            attrs = request.auth.get('attrs', [])
            for a in attrs:
                if (
                    a['application__code'] == 'CARGA_ORG_LOT'
                    and a['key'] == 'can_upload'
                    and a['value'].lower() == 'true'
                ):
                    return True
            return False
        
        # Fallback: verifica diretamente no banco (para testes e sessões)
        try:
            # Busca aplicação CARGA_ORG_LOT (campo correto: codigointerno)
            app_carga = Aplicacao.objects.filter(codigointerno='CARGA_ORG_LOT').first()
            if not app_carga:
                return False
            
            # Busca role GESTOR_CARGA (campo correto: codigoperfil)
            role_gestor = Role.objects.filter(
                codigoperfil='GESTOR_CARGA',
                aplicacao=app_carga
            ).first()
            if not role_gestor:
                return False
            
            # Verifica se usuário tem essa role
            has_role = UserRole.objects.filter(
                user=user,
                role=role_gestor,
                aplicacao=app_carga
            ).exists()
            
            return has_role
            
        except Exception:
            return False


class IsCargaOrgLotUser(CanManageCarga):
    """
    Alias para manter compatibilidade com os testes antigos.
    Herda exatamente a mesma lógica de CanManageCarga.
    """
    pass
