"""IAM Models

Currently imports from accounts app for backward compatibility.
In Phase 3 of migration, these models will be moved here.

Migration Strategy:
- Phase 1: Services use accounts.models (current)
- Phase 2: Refactor domain apps to use services
- Phase 3: Move models here, update AUTH_USER_MODEL
- Phase 4: Prepare for microservice extraction
"""

# Temporary imports for Phase 1
from accounts.models import (
    User,
    Aplicacao,
    Role,
    UserRole,
    Attribute,
    RolePermission,
    UserManager,
)

__all__ = [
    'User',
    'Aplicacao',
    'Role',
    'UserRole',
    'Attribute',
    'RolePermission',
    'UserManager',
]