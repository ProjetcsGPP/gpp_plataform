"""
API Views do Ações PNGI.
Usa AppContextMiddleware para detecção automática da aplicação.
"""

import logging
from django.apps import apps
from django.db.models import Q, Prefetch
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import User, UserRole
from common.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserUpdateSerializer,
    PortalAuthSerializer
)
from common.services.portal_auth import get_portal_auth_service
from ..models import (
    Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta, Acoes,
    AcaoPrazo, AcaoDestaque, TipoAnotacaoAlinhamento,
    AcaoAnotacaoAlinhamento, UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel
)
from ..serializers import (
    EixoSerializer, SituacaoAcaoSerializer, VigenciaPNGISerializer,
    TipoEntraveAlertaSerializer, AcoesSerializer, AcoesListSerializer,
    AcaoPrazoSerializer, AcaoDestaqueSerializer, TipoAnotacaoAlinhamentoSerializer,
    AcaoAnotacaoAlinhamentoSerializer, UsuarioResponsavelSerializer,
    RelacaoAcaoUsuarioResponsavelSerializer, EixoListSerializer,
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
    
    lookup_field = 'pk'
    lookup_value_regex = '.*'
    
    def retrieve(self, request, pk=None):
        """GET /api/v1/acoes_pngi/users/{email}/"""
        return Response({
            "email": pk,
            "app_context": {
                "code": getattr(request.app_context, 'code', None) if hasattr(request, 'app_context') else None,
                "name": getattr(request.app_context, 'name', None) if hasattr(request, 'app_context') else None
            } if hasattr(request, 'app_context') else None
        })
    
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
    """
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['stralias']
    search_fields = ['strdescricaoeixo', 'stralias']
    ordering_fields = ['stralias', 'strdescricaoeixo', 'created_at']
    ordering = ['stralias']
    
    def get_serializer_class(self):
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaosituacao']
    ordering_fields = ['strdescricaosituacao', 'created_at']
    ordering = ['strdescricaosituacao']


class VigenciaPNGIViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Vigências do PNGI.
    """
    queryset = VigenciaPNGI.objects.all()
    serializer_class = VigenciaPNGISerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['isvigenciaativa']
    search_fields = ['strdescricaovigenciapngi']
    ordering_fields = ['datiniciovigencia', 'datfinalvigencia', 'created_at']
    ordering = ['-datiniciovigencia']
    
    def get_serializer_class(self):
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
    
    @action(detail=False, methods=['get'])
    def vigente(self, request):
        """Retorna vigências vigentes no momento"""
        vigencias_ativas = [v for v in self.get_queryset() if v.esta_vigente]
        serializer = self.get_serializer(vigencias_ativas, many=True)
        return Response(serializer.data)
    
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


class TipoEntraveAlertaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Tipos de Entrave/Alerta.
    """
    queryset = TipoEntraveAlerta.objects.all()
    serializer_class = TipoEntraveAlertaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaotipoentravealerta']
    ordering_fields = ['strdescricaotipoentravealerta', 'created_at']
    ordering = ['strdescricaotipoentravealerta']


class AcoesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Ações do PNGI.
    """
    queryset = Acoes.objects.select_related(
        'idvigenciapngi', 'idtipoentravealerta'
    ).prefetch_related(
        'prazos', 'destaques', 'anotacoes_alinhamento', 'responsaveis'
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['idvigenciapngi', 'idtipoentravealerta']
    search_fields = ['strapelido', 'strdescricaoacao', 'strdescricaoentrega']
    ordering_fields = ['strapelido', 'datdataentrega', 'created_at']
    ordering = ['strapelido']

    def get_serializer_class(self):
        if self.action == 'list':
            return AcoesListSerializer
        return AcoesSerializer

    @action(detail=True, methods=['get'])
    def prazos_ativos(self, request, pk=None):
        """Retorna prazos ativos da ação"""
        acao = self.get_object()
        prazos = acao.prazos.filter(isacaoprazoativo=True)
        serializer = AcaoPrazoSerializer(prazos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def responsaveis_list(self, request, pk=None):
        """Retorna lista de responsáveis da ação"""
        acao = self.get_object()
        relacoes = acao.responsaveis.select_related('idusuarioresponsavel__idusuario')
        serializer = RelacaoAcaoUsuarioResponsavelSerializer(relacoes, many=True)
        return Response(serializer.data)


class AcaoPrazoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Prazos de Ações.
    """
    queryset = AcaoPrazo.objects.select_related('idacao')
    serializer_class = AcaoPrazoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['idacao', 'isacaoprazoativo']
    search_fields = ['strprazo', 'idacao__strapelido']
    ordering_fields = ['created_at', 'isacaoprazoativo']
    ordering = ['-isacaoprazoativo', '-created_at']

    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas prazos ativos"""
        prazos = self.get_queryset().filter(isacaoprazoativo=True)
        serializer = self.get_serializer(prazos, many=True)
        return Response(serializer.data)


class AcaoDestaqueViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Destaques de Ações.
    """
    queryset = AcaoDestaque.objects.select_related('idacao')
    serializer_class = AcaoDestaqueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['idacao']
    search_fields = ['idacao__strapelido']
    ordering_fields = ['datdatadestaque', 'created_at']
    ordering = ['-datdatadestaque']


class TipoAnotacaoAlinhamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Tipos de Anotação de Alinhamento.
    """
    queryset = TipoAnotacaoAlinhamento.objects.all()
    serializer_class = TipoAnotacaoAlinhamentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaotipoanotacaoalinhamento']
    ordering_fields = ['strdescricaotipoanotacaoalinhamento', 'created_at']
    ordering = ['strdescricaotipoanotacaoalinhamento']


class AcaoAnotacaoAlinhamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Anotações de Alinhamento.
    """
    queryset = AcaoAnotacaoAlinhamento.objects.select_related(
        'idacao', 'idtipoanotacaoalinhamento'
    )
    serializer_class = AcaoAnotacaoAlinhamentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['idacao', 'idtipoanotacaoalinhamento']
    search_fields = [
        'idacao__strapelido',
        'strdescricaoanotacaoalinhamento',
        'strnumeromonitoramento'
    ]
    ordering_fields = ['datdataanotacaoalinhamento', 'created_at']
    ordering = ['-datdataanotacaoalinhamento']


class UsuarioResponsavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Usuários Responsáveis.
    """
    queryset = UsuarioResponsavel.objects.select_related('idusuario')
    serializer_class = UsuarioResponsavelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['strorgao']
    search_fields = ['idusuario__name', 'idusuario__email', 'strorgao', 'strtelefone']
    ordering_fields = ['created_at']
    ordering = ['idusuario__name']


class RelacaoAcaoUsuarioResponsavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Relações entre Ações e Usuários Responsáveis.
    """
    queryset = RelacaoAcaoUsuarioResponsavel.objects.select_related(
        'idacao', 'idusuarioresponsavel__idusuario'
    )
    serializer_class = RelacaoAcaoUsuarioResponsavelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['idacao', 'idusuarioresponsavel']
    search_fields = [
        'idacao__strapelido',
        'idusuarioresponsavel__idusuario__name'
    ]
    ordering_fields = ['created_at']
    ordering = ['idacaousuarioresponsavel']
