"""
Context Processor para disponibilizar permissões nos templates.
Adicione em settings.py:

TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            ...,
            'acoes_pngi.context_processors.acoes_permissions',
        ],
    },
}]

Uso nos templates:
    {% if can_add_eixo %}
        <a href="...">Novo Eixo</a>
    {% endif %}
    
    {% if is_gestor_pngi %}
        <button>Ação Admin</button>
    {% endif %}
"""

from accounts.models import UserRole


def acoes_permissions(request):
    """
    Adiciona permissões do usuário ao contexto dos templates.
    
    Variáveis disponíveis:
        - acoes_role: Role do usuário (ex: 'GESTOR_PNGI')
        - is_gestor_pngi: True se usuário é gestor
        - is_coordenador_pngi: True se usuário é coordenador ou superior
        - can_manage_config: True se pode gerenciar configurações
        - can_manage_acoes: True se pode gerenciar ações
        - can_delete: True se pode deletar registros
        - can_add_eixo, can_change_eixo, can_delete_eixo, can_view_eixo
        - can_add_situacaoacao, can_change_situacaoacao, etc.
    """
    if not request.user.is_authenticated:
        return {
            'acoes_role': None,
            'is_gestor_pngi': False,
            'is_coordenador_pngi': False,
            'can_manage_config': False,
            'can_manage_acoes': False,
            'can_delete': False,
        }
    
    user = request.user
    
    # Superusuário tem tudo
    if user.is_superuser:
        return {
            'acoes_role': 'SUPERUSER',
            'is_gestor_pngi': True,
            'is_coordenador_pngi': True,
            'can_manage_config': True,
            'can_manage_acoes': True,
            'can_delete': True,
            'can_add_eixo': True,
            'can_change_eixo': True,
            'can_delete_eixo': True,
            'can_view_eixo': True,
            'can_add_situacaoacao': True,
            'can_change_situacaoacao': True,
            'can_delete_situacaoacao': True,
            'can_view_situacaoacao': True,
            'can_add_vigenciapngi': True,
            'can_change_vigenciapngi': True,
            'can_delete_vigenciapngi': True,
            'can_view_vigenciapngi': True,
        }
    
    # Buscar role do usuário
    user_role = UserRole.objects.filter(
        user=user,
        aplicacao__codigointerno='ACOES_PNGI'
    ).select_related('role').first()
    
    if not user_role:
        return {
            'acoes_role': None,
            'is_gestor_pngi': False,
            'is_coordenador_pngi': False,
            'can_manage_config': False,
            'can_manage_acoes': False,
            'can_delete': False,
        }
    
    role_code = user_role.role.codigoperfil
    
    # Obter permissões específicas
    perms = user.get_app_permissions('ACOES_PNGI')
    
    context = {
        'acoes_role': role_code,
        'is_gestor_pngi': role_code == 'GESTOR_PNGI',
        'is_coordenador_pngi': role_code in ['GESTOR_PNGI', 'COORDENADOR_PNGI'],
        'can_manage_config': role_code in ['GESTOR_PNGI', 'COORDENADOR_PNGI'],
        'can_manage_acoes': role_code in ['GESTOR_PNGI', 'OPERADOR_ACAO'],
        'can_delete': role_code == 'GESTOR_PNGI',
        
        # Eixos
        'can_add_eixo': 'add_eixo' in perms,
        'can_change_eixo': 'change_eixo' in perms,
        'can_delete_eixo': 'delete_eixo' in perms,
        'can_view_eixo': 'view_eixo' in perms,
        
        # Situações
        'can_add_situacaoacao': 'add_situacaoacao' in perms,
        'can_change_situacaoacao': 'change_situacaoacao' in perms,
        'can_delete_situacaoacao': 'delete_situacaoacao' in perms,
        'can_view_situacaoacao': 'view_situacaoacao' in perms,
        
        # Vigências
        'can_add_vigenciapngi': 'add_vigenciapngi' in perms,
        'can_change_vigenciapngi': 'change_vigenciapngi' in perms,
        'can_delete_vigenciapngi': 'delete_vigenciapngi' in perms,
        'can_view_vigenciapngi': 'view_vigenciapngi' in perms,
    }
    
    return context
