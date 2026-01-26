# carga_org_lot/permissions.py
from rest_framework.permissions import BasePermission


class CanManageCarga(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        roles = request.auth.get('roles', []) if hasattr(request, 'auth') else []
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


class IsCargaOrgLotUser(CanManageCarga):
    """
    Alias para manter compatibilidade com os testes antigos.
    Herda exatamente a mesma lógica de CanManageCarga.
    """
    pass
