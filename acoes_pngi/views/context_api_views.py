"""
API Views de Contexto para Ações PNGI
Retorna dados dos context_processors para consumo no Next.js

Esta camada garante que tanto as páginas Django quanto o Next.js
tenham acesso aos mesmos dados de contexto, permissões e perfis.

Padrão: Baseado em carga_org_lot/views/context_api_views.py
"""

import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserRole
from django.apps import apps
from ..context_processors import (
    acoes_permissions,
    acoes_pngi_context,
    acoes_pngi_models_context,
)

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def app_context_api(request):
    """
    Retorna informações completas da aplicação Ações PNGI.
    
    ✨ Usa os context_processors para garantir consistência entre Django e Next.js
    
    GET /api/v1/acoes_pngi/context/app/
    
    Resposta:
    {
        "code": "ACOES_PNGI",
        "name": "Ações PNGI",
        "icon": "fas fa-tasks",
        "url_namespace": "acoes_pngi",
        "user_roles": [
            {
                "id": 3,
                "name": "Gestor Ações PNGI",
                "code": "GESTOR_PNGI",
                "is_active": true
            }
        ]
    }
    """
    try:
        # Mock resolver_match para context processor funcionar
        class MockMatch:
            app_name = 'acoes_pngi'
        
        request.resolver_match = MockMatch()
        request.session = request.session or {}
        
        # Usa context processor direto
        context = acoes_pngi_context(request)
        
        # Garante que tem os dados
        if not context.get('app_context'):
            return Response(
                {'detail': 'Contexto da aplicação não disponível'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = {
            'code': context['app_context']['code'],
            'name': context['app_context']['name'],
            'icon': context['app_context']['icon'],
            'url_namespace': context['app_context']['url_namespace'],
        }
        
        # Inclui perfis do usuário se existir
        if context.get('user_roles_in_app'):
            response_data['user_roles'] = context['user_roles_in_app']
        else:
            response_data['user_roles'] = []
        
        logger.info(f"Contexto da app retornado para usuário: {request.user.email}")
        
        return Response(response_data)
    
    except Exception as e:
        logger.error(f"Erro ao retornar contexto da app: {str(e)}")
        return Response(
            {'detail': f'Erro ao retornar contexto: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions_api(request):
    """
    Retorna permissões completas do usuário de forma estruturada.
    
    ✨ Usa context_processors para garantir consistência
    
    GET /api/v1/acoes_pngi/context/permissions/
    
    Resposta:
    {
        "user_id": 1,
        "email": "user@example.com",
        "name": "João Silva",
        "permissions": [
            "view_eixo",
            "add_eixo",
            "change_eixo",
            "delete_eixo",
            "view_situacaoacao",
            "add_situacaoacao",
            "change_situacaoacao",
            "delete_situacaoacao",
            "view_vigenciapngi",
            "add_vigenciapngi",
            "change_vigenciapngi",
            "delete_vigenciapngi"
        ],
        "models_permissions": {
            "eixo": {
                "view": true,
                "add": true,
                "change": true,
                "delete": true
            },
            "situacaoacao": {
                "view": false,
                "add": false,
                "change": false,
                "delete": false
            },
            "vigenciapngi": {
                "view": true,
                "add": true,
                "change": true,
                "delete": false
            }
        },
        "role": "GESTOR_PNGI",
        "role_name": "Gestor Ações PNGI"
    }
    """
    try:
        # Mock resolver_match para context processor funcionar
        class MockMatch:
            app_name = 'acoes_pngi'
        
        request.resolver_match = MockMatch()
        request.session = request.session or {}
        
        # Usa context processor para permissões
        perms_context = acoes_permissions(request)
        
        # Extrai informações do usuário
        user_role = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).select_related('role').first()
        
        role_code = user_role.role.codigoperfil if user_role else None
        role_name = user_role.role.nomeperfil if user_role else None
        
        response_data = {
            'user_id': request.user.id,
            'email': request.user.email,
            'name': request.user.name if hasattr(request.user, 'name') else request.user.first_name,
            'permissions': perms_context.get('acoes_permissions', []),
            'models_permissions': perms_context.get('acoes_models_perms', {}),
            'role': role_code,
            'role_name': role_name,
        }
        
        logger.info(f"Permissões retornadas para usuário: {request.user.email}")
        
        return Response(response_data)
    
    except Exception as e:
        logger.error(f"Erro ao retornar permissões do usuário: {str(e)}")
        return Response(
            {'detail': f'Erro ao retornar permissões: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def models_info_api(request):
    """
    Retorna informações sobre os modelos da aplicação.
    
    ✨ Útil para Next.js gerar labels e validações dinamicamente
    
    GET /api/v1/acoes_pngi/context/models/
    
    Resposta:
    {
        "models": {
            "eixo": {
                "model_name": "eixo",
                "verbose_name": "Eixo",
                "verbose_name_plural": "Eixos",
                "app_label": "acoes_pngi",
                "db_table": "tbleixos"
            },
            "situacao_acao": {
                "model_name": "situacaoacao",
                "verbose_name": "Situação de Ação",
                "verbose_name_plural": "Situações de Ação",
                "app_label": "acoes_pngi",
                "db_table": "tblsituacaoacao"
            },
            "vigencia_pngi": {
                "model_name": "vigenciapngi",
                "verbose_name": "Vigência PNGI",
                "verbose_name_plural": "Vigências PNGI",
                "app_label": "acoes_pngi",
                "db_table": "tblvigenciapngi"
            }
        }
    }
    """
    try:
        # Mock resolver_match para context processor funcionar
        class MockMatch:
            app_name = 'acoes_pngi'
        
        request.resolver_match = MockMatch()
        request.session = request.session or {}
        
        # Usa context processor para informações de modelos
        models_context = acoes_pngi_models_context(request)
        
        response_data = {
            'models': models_context.get('acoes_models_info', {})
        }
        
        return Response(response_data)
    
    except Exception as e:
        logger.error(f"Erro ao retornar informações de modelos: {str(e)}")
        return Response(
            {'detail': f'Erro ao retornar informações: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def full_context_api(request):
    """
    Retorna contexto COMPLETO da aplicação (app + permissões + modelos).
    
    ✨ Endpoint único para o Next.js sincronizar todo o contexto
    
    GET /api/v1/acoes_pngi/context/full/
    
    Resposta:
    {
        "app": {...app context...},
        "permissions": {...user permissions...},
        "models": {...models info...},
        "timestamp": "2026-02-05T14:30:00Z"
    }
    """
    try:
        from django.utils import timezone
        
        # Mock resolver_match para context processor funcionar
        class MockMatch:
            app_name = 'acoes_pngi'
        
        request.resolver_match = MockMatch()
        request.session = request.session or {}
        
        # Obtém todos os contextos
        app_ctx = acoes_pngi_context(request)
        perms_ctx = acoes_permissions(request)
        models_ctx = acoes_pngi_models_context(request)
        
        # Busca role do usuário
        user_role = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).select_related('role').first()
        
        role_code = user_role.role.codigoperfil if user_role else None
        role_name = user_role.role.nomeperfil if user_role else None
        
        response_data = {
            'app': {
                'code': app_ctx.get('app_context', {}).get('code'),
                'name': app_ctx.get('app_context', {}).get('name'),
                'icon': app_ctx.get('app_context', {}).get('icon'),
                'url_namespace': app_ctx.get('app_context', {}).get('url_namespace'),
                'user_roles': app_ctx.get('user_roles_in_app', []),
            },
            'permissions': {
                'user_id': request.user.id,
                'email': request.user.email,
                'name': request.user.name if hasattr(request.user, 'name') else request.user.first_name,
                'permissions': perms_ctx.get('acoes_permissions', []),
                'models_permissions': perms_ctx.get('acoes_models_perms', {}),
                'role': role_code,
                'role_name': role_name,
            },
            'models': models_ctx.get('acoes_models_info', {}),
            'timestamp': timezone.now().isoformat(),
        }
        
        logger.info(f"Contexto completo retornado para usuário: {request.user.email}")
        
        return Response(response_data)
    
    except Exception as e:
        logger.error(f"Erro ao retornar contexto completo: {str(e)}")
        return Response(
            {'detail': f'Erro ao retornar contexto: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
