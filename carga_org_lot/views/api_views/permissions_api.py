"""
Permissions API - Endpoint de Permissões do Usuário
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ...utils.permissions import (
    get_user_app_permissions,
    get_user_role,
    is_gestor,
    is_coordenador_or_above,
)

import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    """
    Retorna as permissões do usuário logado para o app CARGA_ORG_LOT.
    
    Endpoint otimizado para consumo no Next.js, fornecendo:
    - Permissões específicas por modelo
    - Permissões agrupadas por tipo
    - Role do usuário
    
    **URL:** `GET /api/v1/carga/permissions/`
    
    **Response:**
    ```json
    {
        "user_id": 123,
        "email": "user@example.com",
        "role": "COORDENADOR_CARGA",
        "permissions": ["view_tblpatriarca", "add_tblpatriarca", ...],
        "groups": {
            "can_view": true,
            "can_add": true,
            "can_change": true,
            "can_delete": false,
            "can_upload": true,
            "can_activate": false
        },
        "specific": {
            "patriarca": {
                "can_view": true,
                "can_add": true,
                "can_change": true,
                "can_delete": false
            },
            "organograma": {...},
            "lotacao": {...}
        }
    }
    ```
    """
    user = request.user
    app_code = 'CARGA_ORG_LOT'
    
    try:
        # Busca todas as permissões do usuário no app
        permissions = get_user_app_permissions(user, app_code)
        
        # Busca role do usuário
        role = get_user_role(user, app_code)
        
        # Verifica níveis de acesso
        is_gest = is_gestor(user, app_code)
        is_coord = is_coordenador_or_above(user, app_code)
        
        # Organiza permissões por modelo
        models = ['tblpatriarca', 'tblorganogramaversao', 'tbllotacaoversao', 
                  'tblcargapatriarca', 'tbltokenenviocarga', 'tblorgaounidade']
        
        specific_perms = {}
        for model in models:
            model_short = model.replace('tbl', '').replace('versao', '')
            specific_perms[model_short] = {
                'can_view': f'view_{model}' in permissions,
                'can_add': f'add_{model}' in permissions,
                'can_change': f'change_{model}' in permissions,
                'can_delete': f'delete_{model}' in permissions,
            }
        
        # Agrupa permissões gerais
        has_any_view = any(p.startswith('view_') for p in permissions)
        has_any_add = any(p.startswith('add_') for p in permissions)
        has_any_change = any(p.startswith('change_') for p in permissions)
        has_any_delete = any(p.startswith('delete_') for p in permissions)
        
        response_data = {
            'user_id': user.id,
            'email': user.email,
            'role': role,
            'permissions': list(permissions),
            'groups': {
                'can_view': has_any_view,
                'can_add': has_any_add,
                'can_change': has_any_change,
                'can_delete': has_any_delete,
                'can_upload': has_any_add,  # Upload requer permissão de adição
                'can_activate': is_coord,  # Apenas Coordenador+ pode ativar
                'is_gestor': is_gest,
                'is_coordenador': is_coord,
            },
            'specific': specific_perms,
        }
        
        logger.info(
            f"Permissões retornadas para {user.email} - "
            f"Role: {role}, Perms: {len(permissions)}"
        )
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erro ao buscar permissões: {str(e)}", exc_info=True)
        return Response(
            {'error': 'Erro ao buscar permissões do usuário'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
