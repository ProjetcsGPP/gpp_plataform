from django import template
register = template.Library() 
from accounts.services.authorization_service import get_authorization_service

@register.filter
def has_permission(request, codename):
    auth = get_authorization_service()
    payload = getattr(request, 'token_payload', {})
    user_id = getattr(request.user, 'id', 0)
    
    if not payload.get('active_role_id'):
        return False
    
    # Extrair model_name do codename
    model_name = codename.split('_', 1)[1] if '_' in codename else ''
    action = codename.split('_')[0]
    
    return auth.can(
        user_id=user_id,
        app_code=payload.get('app_code', 'ACOES_PNGI'),
        active_role_id=payload['active_role_id'],
        action=action,
        model_name=model_name
    )