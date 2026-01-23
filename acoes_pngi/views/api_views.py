"""
API Views do Ações PNGI.
Usa AppContextMiddleware para detecção automática da aplicação.
"""

import logging
from django.apps import apps
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.models import User, UserRole
from common.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserUpdateSerializer,
    PortalAuthSerializer
)
from common.services.portal_auth import get_portal_auth_service
from ..models import Eixo, SituacaoAcao, VigenciaPNGI
from ..serializers import (
    EixoSerializer,
    SituacaoAcaoSerializer,
    VigenciaPNGISerializer,
    EixoListSerializer,
    VigenciaPNGIListSerializer
)

logger = logging.getLogger(__name__)


def get_app_code(request):
    """
    Helper para obter APP_CODE do request ou da config da app.
    
    Prioridade:
    1. request.app_context['code'] (do middleware)
    2. request.app_code (fallback antigo)
    3. app config
    """
    # Tenta pegar do middleware (novo)
    if hasattr(request, 'app_context') and request.app_context.get('code'):
        return request.app_context['code']
    
    # Fallback: request.app_code (antigo)
    if hasattr(request, 'app_code') and request.app_code:
        return request.app_code
    
    # Fallback final: pega da configuração da app
    app_config = apps.get_app_config('acoes_pngi')
    return app_config.app_code


# ============================================================================
# ENDPOINTS DE AUTENTICAÇÃO
# ============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def portal_auth(request):
    """
    Autenticação via token do portal.
    
    ✨ Usa request.app_context do middleware para detectar aplicação.
    
    POST /api/v1/acoes_pngi/auth/portal/
    Body: {"token": "jwt_token"}
    """
    # Valida input
    input_serializer = PortalAuthSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)
    
    token = input_serializer.validated_data['token']
    
    try:
        # ✨ Pega app_code do contexto (adicionado pelo middleware)
        app_code = request.app_context.get('code')
        app_name = request.app_context.get('name')
        
        if not app_code:
            return Response(
                {'detail': 'Aplicação não identificada'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Autentica via portal service
        portal_service = get_portal_auth_service(app_code)
        user = portal_service.authenticate_user(token)
        
        if not user:
            return Response(
                {'detail': 'Token inválido ou expirado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # ✨ Serializa usuário (pega app_code automaticamente do request.app_context)
        user_serializer = UserSerializer(user, context={'request': request})
        
        # Gera token local (opcional)
        from rest_framework.authtoken.models import Token
        local_token, _ = Token.objects.get_or_create(user=user)
        
        logger.info(f"[{app_code}] Usuário autenticado via portal: {user.stremail}")
        
        return Response({
            'user': user_serializer.data,
            'local_token': local_token.key,
            'app': {
                'code': app_code,
                'name': app_name
            },
            'message': f'Autenticado com sucesso em {app_name}'
        })
    
    except Exception as e:
        logger.error(f"Erro na autenticação via portal: {str(e)}")
        return Response(
            {'detail': f'Erro na autenticação: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============================================================================
# VIEWSET DE GERENCIAMENTO DE USUÁRIOS
# ============================================================================

class UserManagementViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de usuários da aplicação.
    
    ✨ Usa request.app_context automaticamente.
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def sync_user(self, request):
        """
        Sincroniza usuário do portal com roles e atributos.
        
        POST /api/v1/acoes_pngi/users/sync/
        Body: {
            "email": "user@example.com",
            "name": "Nome",
            "roles": ["GESTOR_PNGI"],
            "attributes": {"can_upload": "true"}
        }
        """
        try:
            # ✨ Serializer pega app_code do request.app_context
            serializer = UserCreateSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            created = serializer.validated_data['_created']
            
            # Retorna usuário completo
            user_serializer = UserSerializer(user, context={'request': request})
            
            return Response({
                'user': user_serializer.data,
                'created': created,
                'message': f"Usuário {'criado' if created else 'atualizado'} com sucesso"
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Erro ao sincronizar usuário: {str(e)}")
            return Response(
                {'detail': f'Erro ao sincronizar usuário: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def list_users(self, request):
        """
        Lista usuários com acesso à aplicação atual.
        
        GET /api/v1/acoes_pngi/users/list/
        """
        try:
            # ✨ Filtra pela aplicação do contexto
            app_code = request.app_context.get('code')
            
            if not app_code:
                return Response(
                    {'detail': 'Aplicação não identificada'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Usuários com acesso à aplicação
            user_ids = UserRole.objects.filter(
                aplicacao__codigointerno=app_code
            ).values_list('user_id', flat=True)
            
            users = User.objects.filter(
                idusuario__in=user_ids,
                is_active=True
            )
            
            # Filtros opcionais
            if request.query_params.get('idtipousuario'):
                users = users.filter(idtipousuario=request.query_params.get('idtipousuario'))
            
            serializer = UserListSerializer(users, many=True)
            
            return Response({
                'count': users.count(),
                'users': serializer.data
            })
        
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {str(e)}")
            return Response(
                {'detail': f'Erro ao listar usuários: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def get_user_by_email(self, request, pk=None):
        """
        Busca usuário por email.
        
        GET /api/v1/acoes_pngi/users/{email}/
        """
        try:
            user = User.objects.get(stremail=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        
        except User.DoesNotExist:
            return Response(
                {'detail': f'Usuário com email {pk} não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['patch'])
    def update_user_status(self, request, pk=None):
        """
        Atualiza status de usuário.
        
        PATCH /api/v1/acoes_pngi/users/{email}/update_user_status/
        Body: {"is_active": false}
        """
        try:
            user = User.objects.get(stremail=pk)
            
            serializer = UserUpdateSerializer(
                user,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            user_serializer = UserSerializer(user, context={'request': request})
            
            return Response({
                'detail': 'Usuário atualizado com sucesso',
                'user': user_serializer.data
            })
        
        except User.DoesNotExist:
            return Response(
                {'detail': f'Usuário com email {pk} não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================================================
# VIEWSETS DE MODELOS ESPECÍFICOS
# ============================================================================

class EixoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Eixos do PNGI.
    
    Endpoints:
    - GET    /api/v1/acoes_pngi/eixos/           - Lista eixos
    - POST   /api/v1/acoes_pngi/eixos/           - Cria eixo
    - GET    /api/v1/acoes_pngi/eixos/{id}/      - Detalhe
    - PUT    /api/v1/acoes_pngi/eixos/{id}/      - Atualiza
    - DELETE /api/v1/acoes_pngi/eixos/{id}/      - Deleta
    - GET    /api/v1/acoes_pngi/eixos/list_light/ - Listagem otimizada
    """
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Retorna serializer otimizado para listagem"""
        if self.action == 'list':
            return EixoListSerializer
        return EixoSerializer
    
    @action(detail=False, methods=['get'])
    def list_light(self, request):
        """Endpoint otimizado para listagem rápida"""
        eixos = Eixo.objects.all().values('ideixo', 'strdescricaoeixo', 'stralias')
        return Response({
            'count': len(eixos),
            'results': list(eixos)
        })


class SituacaoAcaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Situações de Ações do PNGI.
    
    Endpoints:
    - GET    /api/v1/acoes_pngi/situacoes/       - Lista situações
    - POST   /api/v1/acoes_pngi/situacoes/       - Cria situação
    - GET    /api/v1/acoes_pngi/situacoes/{id}/  - Detalhe
    - PUT    /api/v1/acoes_pngi/situacoes/{id}/  - Atualiza
    - DELETE /api/v1/acoes_pngi/situacoes/{id}/  - Deleta
    """
    queryset = SituacaoAcao.objects.all()
    serializer_class = SituacaoAcaoSerializer
    permission_classes = [IsAuthenticated]


class VigenciaPNGIViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Vigências do PNGI.
    
    Endpoints:
    - GET    /api/v1/acoes_pngi/vigencias/                - Lista vigências
    - POST   /api/v1/acoes_pngi/vigencias/                - Cria vigência
    - GET    /api/v1/acoes_pngi/vigencias/{id}/           - Detalhe
    - PUT    /api/v1/acoes_pngi/vigencias/{id}/           - Atualiza
    - DELETE /api/v1/acoes_pngi/vigencias/{id}/           - Deleta
    - GET    /api/v1/acoes_pngi/vigencias/vigencia_ativa/ - Vigência ativa
    - POST   /api/v1/acoes_pngi/vigencias/{id}/ativar/    - Ativa vigência
    """
    queryset = VigenciaPNGI.objects.all()
    serializer_class = VigenciaPNGISerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Retorna serializer otimizado para listagem"""
        if self.action == 'list':
            return VigenciaPNGIListSerializer
        return VigenciaPNGISerializer
    
    @action(detail=False, methods=['get'])
    def vigencia_ativa(self, request):
        """Retorna a vigência atualmente ativa"""
        try:
            vigencia = VigenciaPNGI.objects.get(isvigenciaativa=True)
            serializer = self.get_serializer(vigencia)
            return Response(serializer.data)
        except VigenciaPNGI.DoesNotExist:
            return Response(
                {'detail': 'Nenhuma vigência ativa encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        """Ativa uma vigência específica"""
        try:
            from django.db import transaction
            
            with transaction.atomic():
                # Desativa todas as vigências
                VigenciaPNGI.objects.update(isvigenciaativa=False)
                
                # Ativa a vigência selecionada
                vigencia = self.get_object()
                vigencia.isvigenciaativa = True
                vigencia.save()
                
                serializer = self.get_serializer(vigencia)
                
                return Response({
                    'detail': 'Vigência ativada com sucesso',
                    'vigencia': serializer.data
                })
        
        except Exception as e:
            logger.error(f"Erro ao ativar vigência: {str(e)}")
            return Response(
                {'detail': f'Erro ao ativar vigência: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
