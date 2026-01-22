from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.apps import apps
import logging

from ..models import Eixo, SituacaoAcao, VigenciaPNGI
from accounts.models import User

# Imports de serializers específicos desta app
from ..serializers import (
    EixoSerializer,
    EixoListSerializer,
    SituacaoAcaoSerializer,
    VigenciaPNGISerializer,
    VigenciaPNGIListSerializer,
)

# Imports de serializers genéricos do common
from common.serializers import (
    UserSerializer,
    UserListSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    PortalAuthSerializer,
)

# Import do serviço genérico
from common.services.portal_auth import get_portal_auth_service

logger = logging.getLogger(__name__)


def get_app_code(request):
    """Helper para obter APP_CODE do request ou da config da app"""
    # Tenta pegar do middleware
    if hasattr(request, 'app_code') and request.app_code:
        return request.app_code
    
    # Fallback: pega da configuração da app
    app_config = apps.get_app_config('acoes_pngi')
    return app_config.app_code


# ============================================================================
# VIEWSETS DE MODELOS ESPECÍFICOS
# ============================================================================

class EixoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Eixos do PNGI.
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
    """
    queryset = SituacaoAcao.objects.all()
    serializer_class = SituacaoAcaoSerializer
    permission_classes = [IsAuthenticated]


class VigenciaPNGIViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Vigências do PNGI.
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
                {'detail': 'Nenhuma vigência ativa encontrada.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        """Ativa uma vigência específica"""
        try:
            from django.db import transaction
            
            with transaction.atomic():
                VigenciaPNGI.objects.update(isvigenciaativa=False)
                vigencia = self.get_object()
                vigencia.isvigenciaativa = True
                vigencia.save()
                
                serializer = self.get_serializer(vigencia)
                return Response({
                    'detail': 'Vigência ativada com sucesso.',
                    'vigencia': serializer.data
                })
        except Exception as e:
            return Response(
                {'detail': f'Erro ao ativar vigência: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================================================
# ENDPOINTS DE AUTENTICAÇÃO (USA SERIALIZERS DO COMMON)
# ============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def portal_auth(request):
    """
    Endpoint para autenticação via Portal.
    Usa serializers genéricos do common.
    """
    # Valida input usando serializer genérico
    input_serializer = PortalAuthSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)
    
    token = input_serializer.validated_data['token']
    
    try:
        # Obtém APP_CODE dinamicamente
        app_code = get_app_code(request)
        
        # Cria instância do serviço genérico
        portal_service = get_portal_auth_service(app_code)
        
        # Autentica via portal
        user = portal_service.authenticate_user(token)
        
        if not user:
            return Response(
                {'detail': 'Token inválido ou expirado.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Serializa dados usando serializer genérico do common
        user_serializer = UserSerializer(
            user,
            context={'app_code': app_code, 'request': request}
        )
        
        # Gera token local
        from rest_framework.authtoken.models import Token
        local_token, _ = Token.objects.get_or_create(user=user)
        
        logger.info(f"[{app_code}] Usuário autenticado via portal: {user.stremail}")
        
        return Response(
            {
                'user': user_serializer.data,
                'local_token': local_token.key,
                'app_code': app_code
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Erro na autenticação via portal: {str(e)}")
        return Response(
            {'detail': f'Erro na autenticação: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============================================================================
# VIEWSET DE GERENCIAMENTO DE USUÁRIOS (USA SERIALIZERS DO COMMON)
# ============================================================================

class UserManagementViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciar usuários.
    Usa serializers genéricos do common.
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def sync_user_from_portal(self, request):
        """Sincroniza um usuário do portal"""
        # Obtém APP_CODE
        app_code = get_app_code(request)
        
        # Usa serializer genérico do common
        serializer = UserCreateSerializer(
            data=request.data,
            context={'app_code': app_code, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        try:
            user = serializer.save()
            created = serializer.validated_data.get('_created', False)
            
            # Retorna dados usando serializer genérico
            user_serializer = UserSerializer(
                user,
                context={'app_code': app_code, 'request': request}
            )
            
            return Response(
                {
                    'detail': f'Usuário {"criado" if created else "atualizado"} com sucesso.',
                    'user': user_serializer.data,
                    'created': created,
                    'app_code': app_code
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar usuário: {str(e)}")
            return Response(
                {'detail': f'Erro ao sincronizar usuário: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def list_users(self, request):
        """Lista usuários usando serializer genérico"""
        try:
            queryset = User.objects.filter(is_active=True)
            
            # Filtros opcionais
            if request.query_params.get('idtipousuario'):
                queryset = queryset.filter(idtipousuario=request.query_params.get('idtipousuario'))
            
            # Usa serializer genérico do common
            serializer = UserListSerializer(queryset, many=True)
            
            return Response(
                {
                    'count': queryset.count(),
                    'users': serializer.data
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {str(e)}")
            return Response(
                {'detail': f'Erro ao listar usuários: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def get_user_by_email(self, request, pk=None):
        """Busca usuário por email usando serializer genérico"""
        try:
            user = User.objects.get(stremail=pk)
            app_code = get_app_code(request)
            
            # Usa serializer genérico do common
            serializer = UserSerializer(
                user,
                context={'app_code': app_code, 'request': request}
            )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response(
                {'detail': f'Usuário com email {pk} não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['patch'])
    def update_user_status(self, request, pk=None):
        """Atualiza status de usuário usando serializer genérico"""
        try:
            user = User.objects.get(stremail=pk)
            
            # Usa serializer genérico do common
            serializer = UserUpdateSerializer(
                user,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            app_code = get_app_code(request)
            user_serializer = UserSerializer(
                user,
                context={'app_code': app_code, 'request': request}
            )
            
            return Response(
                {
                    'detail': 'Usuário atualizado com sucesso.',
                    'user': user_serializer.data
                },
                status=status.HTTP_200_OK
            )
            
        except User.DoesNotExist:
            return Response(
                {'detail': f'Usuário com email {pk} não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
