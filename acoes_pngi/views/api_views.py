"""
API Views do Ações PNGI.
Usa AppContextMiddleware para detecção automática da aplicação.
"""

import logging
from django.apps import apps
from django.db import transaction
from django.db.models import Q
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
    Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta,
    Acoes, AcaoPrazo, AcaoDestaque,
    TipoAnotacaoAlinhamento, AcaoAnotacaoAlinhamento,
    UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel
)
from ..serializers import (
    EixoSerializer, EixoListSerializer,
    SituacaoAcaoSerializer,
    VigenciaPNGISerializer, VigenciaPNGIListSerializer,
    TipoEntraveAlertaSerializer,
    AcoesSerializer, AcoesListSerializer,
    AcaoPrazoSerializer,
    AcaoDestaqueSerializer,
    TipoAnotacaoAlinhamentoSerializer,
    AcaoAnotacaoAlinhamentoSerializer,
    UsuarioResponsavelSerializer,
    RelacaoAcaoUsuarioResponsavelSerializer
)
from ..permissions import (
    HasAcoesPermission,
    IsCoordenadorOrAbove,
    IsGestorPNGI,
    IsGestorPNGIOnly,  # ✨ NOVA: para UserManagementViewSet
    IsCoordernadorOrGestorPNGI,
    IsCoordernadorGestorOrOperadorPNGI
)
from ..utils.permissions import (
    get_user_app_permissions,
    get_model_permissions,
    require_api_permission
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
        
        logger.info(f"[{app_code}] Usuário autenticado via portal: {user.email}")
        
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    """
    Retorna permissões do usuário logado para consumo no Next.js.
    ✨ Usa helpers com cache para otimização de performance.
    
    GET /api/v1/acoes_pngi/permissions/
    """
    try:
        # ✨ Usa helper com cache (15 minutos)
        perms = get_user_app_permissions(request.user, 'ACOES_PNGI')
        
        # Buscar role do usuário
        user_role = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).select_related('role').first()
        
        role = user_role.role.codigoperfil if user_role else None
        
        # ✨ Usa helper para permissões por modelo (também com cache)
        specific = {
            'eixo': get_model_permissions(request.user, 'eixo', 'ACOES_PNGI'),
            'situacaoacao': get_model_permissions(request.user, 'situacaoacao', 'ACOES_PNGI'),
            'vigenciapngi': get_model_permissions(request.user, 'vigenciapngi', 'ACOES_PNGI'),
        }
        
        return Response({
            'user_id': request.user.id,
            'email': request.user.email,
            'name': request.user.name,
            'role': role,
            'permissions': list(perms),
            'is_superuser': request.user.is_superuser,
            'groups': {
                'can_manage_config': any(p in perms for p in [
                    'add_eixo', 'change_eixo', 
                    'add_situacaoacao', 'change_situacaoacao',
                    'add_vigenciapngi', 'change_vigenciapngi'
                ]),
                'can_manage_acoes': False,  # Futuramente com model Acao
                'can_delete': any(p.startswith('delete_') for p in perms),
            },
            'specific': specific,
        })
    
    except Exception as e:
        logger.error(f"Erro ao buscar permissões do usuário: {str(e)}")
        return Response(
            {'detail': f'Erro ao buscar permissões: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============================================================================
# VIEWSET DE GERENCIAMENTO DE USUÁRIOS
# ============================================================================

class UserManagementViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de usuários da aplicação.
    
    ✨ Usa request.app_context automaticamente.
    
    Permissões:
    - TODAS as operações (GET/POST/PATCH): Apenas GESTOR_PNGI
    - Demais roles (COORDENADOR, OPERADOR, CONSULTOR) são bloqueadas
    """
    permission_classes = [IsGestorPNGIOnly]  # ✅ CORRIGIDO: GESTOR para tudo
    
    lookup_field = 'pk'
    lookup_value_regex = '.*'
    
    def retrieve(self, request, pk=None):
        """GET /api/v1/acoes_pngi/users/{email}/"""
        return self.get_user_by_email(request, pk)
    
    @action(detail=False, methods=['post'])
    def sync_user(self, request):
        """Sincroniza usuário do portal com roles e atributos."""
        try:
            serializer = UserCreateSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            created = serializer.validated_data.get('_created', False)
            
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
        """Lista usuários com acesso à aplicação atual."""
        try:
            app_code = get_app_code(request)
            
            if not app_code:
                return Response(
                    {'detail': 'Aplicação não identificada'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            user_ids = UserRole.objects.filter(
                aplicacao__codigointerno=app_code
            ).values_list('user_id', flat=True)
            
            users = User.objects.filter(
                id__in=user_ids,
                is_active=True
            )
            
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
        """Busca usuário por email."""
        try:
            user = User.objects.get(email=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        
        except User.DoesNotExist:
            return Response(
                {'detail': f'Usuário com email {pk} não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['patch'])
    def update_user_status(self, request, pk=None):
        """Atualiza status de usuário."""
        try:
            user = User.objects.get(email=pk)
            
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
# VIEWSETS DE ENTIDADES CORE
# ============================================================================

class EixoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Eixos do PNGI.
    
    Permissões:
    - Leitura: CONSULTOR, OPERADOR, COORDENADOR, GESTOR
    - Escrita: Apenas COORDENADOR e GESTOR
    """
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer
    permission_classes = [IsCoordernadorOrGestorPNGI]  # ✅ ATUALIZADO
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaoeixo', 'stralias']
    ordering_fields = ['stralias', 'strdescricaoeixo', 'created_at']
    ordering = ['stralias']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EixoListSerializer
        return EixoSerializer
    
    @action(detail=False, methods=['get'])
    @require_api_permission('view_eixo')
    def list_light(self, request):
        """Endpoint otimizado para listagem rápida."""
        eixos = Eixo.objects.all().values('ideixo', 'strdescricaoeixo', 'stralias')
        return Response({
            'count': len(eixos),
            'results': list(eixos)
        })


class SituacaoAcaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Situações de Ações do PNGI.
    
    Permissões:
    - Leitura: CONSULTOR, OPERADOR, COORDENADOR, GESTOR
    - Escrita: Apenas GESTOR_PNGI (configuração crítica)
    """
    queryset = SituacaoAcao.objects.all()
    serializer_class = SituacaoAcaoSerializer
    permission_classes = [IsGestorPNGI]  # ✅ CORRETO: todos leem, GESTOR escreve
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaosituacao']
    ordering_fields = ['strdescricaosituacao', 'created_at']
    ordering = ['strdescricaosituacao']


class VigenciaPNGIViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Vigências do PNGI.
    
    Permissões:
    - Leitura: CONSULTOR, OPERADOR, COORDENADOR, GESTOR
    - Escrita: Apenas COORDENADOR e GESTOR
    """
    queryset = VigenciaPNGI.objects.all()
    serializer_class = VigenciaPNGISerializer
    permission_classes = [IsCoordernadorOrGestorPNGI]  # ✅ ATUALIZADO
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaovigenciapngi']
    ordering_fields = ['datiniciovigencia', 'datfinalvigencia', 'created_at']
    ordering = ['-datiniciovigencia']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('isvigenciaativa'):
            queryset = queryset.filter(isvigenciaativa=True)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VigenciaPNGIListSerializer
        return VigenciaPNGISerializer
    
    @action(detail=False, methods=['get'])
    @require_api_permission('view_vigenciapngi')
    def vigencia_ativa(self, request):
        """Retorna a vigência atualmente ativa."""
        try:
            vigencia = VigenciaPNGI.objects.get(isvigenciaativa=True)
            serializer = self.get_serializer(vigencia)
            return Response(serializer.data)
        except VigenciaPNGI.DoesNotExist:
            return Response(
                {'detail': 'Nenhuma vigência ativa encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsCoordenadorOrAbove])
    def ativar(self, request, pk=None):
        """Ativa uma vigência específica."""
        try:
            with transaction.atomic():
                VigenciaPNGI.objects.update(isvigenciaativa=False)
                vigencia = self.get_object()
                vigencia.isvigenciaativa = True
                vigencia.save()
                
                serializer = self.get_serializer(vigencia)
                logger.info(f"Vigência {vigencia.idvigenciapngi} ativada por {request.user.email}")
                
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
    
    Permissões:
    - Leitura: CONSULTOR, OPERADOR, COORDENADOR, GESTOR
    - Escrita: Apenas GESTOR_PNGI (configuração crítica)
    """
    queryset = TipoEntraveAlerta.objects.all()
    serializer_class = TipoEntraveAlertaSerializer
    permission_classes = [IsGestorPNGI]  # ✅ CORRETO: todos leem, GESTOR escreve
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaotipoentravealerta']
    ordering_fields = ['strdescricaotipoentravealerta', 'created_at']
    ordering = ['strdescricaotipoentravealerta']


# ============================================================================
# VIEWSETS DE AÇÕES
# ============================================================================

class AcoesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Ações do PNGI.
    
    Permissões:
    - Leitura: CONSULTOR, OPERADOR, COORDENADOR, GESTOR
    - Escrita: OPERADOR, COORDENADOR, GESTOR (CONSULTOR bloqueado)
    """
    queryset = Acoes.objects.select_related(
        'idvigenciapngi', 'idtipoentravealerta'
    ).prefetch_related(
        'prazos', 'destaques', 'anotacoes_alinhamento', 'responsaveis'
    )
    permission_classes = [IsCoordernadorGestorOrOperadorPNGI]  # ✅ JÁ ESTAVA CORRETO
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strapelido', 'strdescricaoacao', 'strdescricaoentrega']
    ordering_fields = ['strapelido', 'datdataentrega', 'created_at']
    ordering = ['strapelido']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('idvigenciapngi'):
            queryset = queryset.filter(idvigenciapngi=self.request.query_params.get('idvigenciapngi'))
        if self.request.query_params.get('idtipoentravealerta'):
            queryset = queryset.filter(idtipoentravealerta=self.request.query_params.get('idtipoentravealerta'))
        return queryset

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
    
    Permissões:
    - Leitura: CONSULTOR, OPERADOR, COORDENADOR, GESTOR
    - Escrita: OPERADOR, COORDENADOR, GESTOR (CONSULTOR bloqueado)
    """
    queryset = AcaoPrazo.objects.select_related('idacao')
    serializer_class = AcaoPrazoSerializer
    permission_classes = [IsCoordernadorGestorOrOperadorPNGI]  # ✅ JÁ ESTAVA CORRETO
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strprazo', 'idacao__strapelido']
    ordering_fields = ['created_at', 'isacaoprazoativo']
    ordering = ['-isacaoprazoativo', '-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('idacao'):
            queryset = queryset.filter(idacao=self.request.query_params.get('idacao'))
        
        # Converte string para booleano
        is_ativo = self.request.query_params.get('isacaoprazoativo')
        if is_ativo is not None:
            is_ativo_bool = is_ativo.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(isacaoprazoativo=is_ativo_bool)
        return queryset

    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas prazos ativos"""
        prazos = self.get_queryset().filter(isacaoprazoativo=True)
        serializer = self.get_serializer(prazos, many=True)
        return Response(serializer.data)


class AcaoDestaqueViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Destaques de Ações.
    
    Permissões:
    - Leitura: CONSULTOR, OPERADOR, COORDENADOR, GESTOR
    - Escrita: OPERADOR, COORDENADOR, GESTOR (CONSULTOR bloqueado)
    """
    queryset = AcaoDestaque.objects.select_related('idacao')
    serializer_class = AcaoDestaqueSerializer
    permission_classes = [IsCoordernadorGestorOrOperadorPNGI]  # ✅ JÁ ESTAVA CORRETO
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['idacao__strapelido']
    ordering_fields = ['datdatadestaque', 'created_at']
    ordering = ['-datdatadestaque']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('idacao'):
            queryset = queryset.filter(idacao=self.request.query_params.get('idacao'))
        return queryset


# ============================================================================
# VIEWSETS DE ALINHAMENTO
# ============================================================================

class TipoAnotacaoAlinhamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Tipos de Anotação de Alinhamento.
    
    Permissões:
    - Leitura: CONSULTOR, OPERADOR, COORDENADOR, GESTOR
    - Escrita: Apenas COORDENADOR e GESTOR (CONSULTOR e OPERADOR bloqueados)
    """
    queryset = TipoAnotacaoAlinhamento.objects.all()
    serializer_class = TipoAnotacaoAlinhamentoSerializer
    permission_classes = [IsCoordernadorOrGestorPNGI]  # ✅ JÁ ESTAVA CORRETO
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaotipoanotacaoalinhamento']
    ordering = ['strdescricaotipoanotacaoalinhamento']


class AcaoAnotacaoAlinhamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Anotações de Alinhamento de Ações.
    
    Permissões:
    - Leitura: CONSULTOR, OPERADOR, COORDENADOR, GESTOR
    - Escrita: OPERADOR, COORDENADOR, GESTOR (CONSULTOR bloqueado)
    """
    queryset = AcaoAnotacaoAlinhamento.objects.select_related(
        'idacao', 'idtipoanotacaoalinhamento'
    )
    serializer_class = AcaoAnotacaoAlinhamentoSerializer
    
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['idacao', 'idtipoanotacaoalinhamento']
    search_fields = [
        'idacao__strapelido', 
        'strdescricaoanotacaoalinhamento', 
        'strnumeromonitoramento',
        'idtipoanotacaoalinhamento__strdescricaotipoanotacaoalinhamento'  # Mantenha se necessário
    ]
    ordering_fields = ['datdataanotacaoalinhamento']
    ordering = ['-datdataanotacaoalinhamento']

    permission_classes = [IsCoordernadorGestorOrOperadorPNGI]    

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('idacao'):
            queryset = queryset.filter(idacao=self.request.query_params.get('idacao'))
        if self.request.query_params.get('idtipoanotacaoalinhamento'):
            queryset = queryset.filter(idtipoanotacaoalinhamento=self.request.query_params.get('idtipoanotacaoalinhamento'))
        return queryset


# ============================================================================
# VIEWSETS DE RESPONSÁVEIS
# ============================================================================
class UsuarioResponsavelViewSet(viewsets.ModelViewSet):
    queryset = UsuarioResponsavel.objects.select_related('idusuario')
    serializer_class = UsuarioResponsavelSerializer
    permission_classes = [IsAuthenticated, HasAcoesPermission]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'strorgao': ['icontains', 'exact'],
        'strtelefone': ['icontains'],
    }
    
    # ✅ CORREÇÃO: Custom search_fields que FUNCIONA com OneToOne
    search_fields = ['strorgao', 'strtelefone']  # Campos diretos
    
    ordering_fields = ['idusuario__name', 'strorgao']
    ordering = ['idusuario__name']

    def get_queryset(self):
        queryset = UsuarioResponsavel.objects.select_related('idusuario')
        
        # ✅ Override search manual
        search = self.request.query_params.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(idusuario__email__icontains=search) |
                Q(idusuario__name__icontains=search) |
                Q(strorgao__icontains=search) |
                Q(strtelefone__icontains=search)
            )
        
        return queryset.distinct()


    def list(self, request, *args, **kwargs):
        print("🔍 DEBUG list() chamado")
        response = super().list(request, *args, **kwargs)
        print(f"🔍 Response data: {list(response.data.keys())}")
        print(f"🔍 Results count: {len(response.data.get('results', []))}")
        print(f"🔍 QS count: {self.get_queryset().count()}")
        return response
        
    def debug_serializer_structure(self):
        """🔍 DEBUG: Ver estrutura real do serializer"""
        print("=== DEBUG SERIALIZER ===")
        response = self.client.get('/api/v1/acoes_pngi/usuarios-responsaveis/')
        print(f"Status: {response.status_code}")
        print(f"Response data keys: {list(response.data.keys()) if response.data else 'NO DATA'}")
        
        results, total = self.get_api_results(response)
        print(f"Results count: {len(results)}, Total: {total}")
        
        if results:
            sample = results[0]
            print("ESTRUTURA COMPLETA DO PRIMEIRO ITEM:")
            print(sample)
            print("CHAVES DISPONÍVEIS:", list(sample.keys()))
            
            # Verificar campos específicos
            print(f"idusuario type: {type(sample.get('idusuario'))}")
            if 'idusuario' in sample:
                print(f"idusuario value: {sample['idusuario']}")
            
            if 'idusuario_name' in sample:
                print(f"idusuario_name: {sample['idusuario_name']}")
        
        print("=== FIM DEBUG ===\n")
    
class RelacaoAcaoUsuarioResponsavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet da relação entre Ação e Usuário Responsável.
    
    Permite:
    - CRUD completo
    - Filtro por ação
    - Filtro por usuário responsável
    - Busca por apelido da ação, nome ou email do usuário
    """

    queryset = RelacaoAcaoUsuarioResponsavel.objects.select_related(
        'idacao',
        'idusuarioresponsavel__idusuario'
    )

    serializer_class = RelacaoAcaoUsuarioResponsavelSerializer
    permission_classes = [IsAuthenticated, HasAcoesPermission]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # 🔎 Filtros exatos
    filterset_fields = {
        'idacao': ['exact'],
        'idusuarioresponsavel': ['exact'],
    }

    # 🔍 Busca textual
    search_fields = [
        'idacao__strapelido',
        'idusuarioresponsavel__idusuario__name',
        'idusuarioresponsavel__idusuario__email',
    ]

    # 🔃 Ordenação
    ordering_fields = [
        'created_at',
        'idacao__strapelido',
        'idusuarioresponsavel__idusuario__name',
    ]

    ordering = ['idacao__strapelido']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtro manual opcional por query param
        idacao = self.request.query_params.get('idacao')
        if idacao:
            queryset = queryset.filter(idacao=idacao)

        idusuarioresponsavel = self.request.query_params.get('idusuarioresponsavel')
        if idusuarioresponsavel:
            queryset = queryset.filter(idusuarioresponsavel=idusuarioresponsavel)

        return queryset.distinct()