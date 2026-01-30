"""
API Views para Carga Org/Lot.
Usa HasCargaOrgLotPermission para verificação automática de permissões.
"""

import logging
from django.apps import apps
from django.db.models import Q, Count, Prefetch
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.models import User, UserRole
from common.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)

from ..models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblOrgaoUnidade,
    TblOrganogramaJson,
    TblLotacaoVersao,
    TblLotacao,
    TblLotacaoJsonOrgao,
    TblLotacaoInconsistencia,
    TblTokenEnvioCarga,
    TblCargaPatriarca,
    TblDetalheStatusCarga,
    TblStatusProgresso,
    TblStatusTokenEnvioCarga,
    TblStatusCarga,
    TblTipoCarga,
)
from ..serializers import (
    TblPatriarcaSerializer,
    TblPatriarcaLightSerializer,
    TblOrganogramaVersaoSerializer,
    TblOrganogramaVersaoLightSerializer,
    TblOrgaoUnidadeSerializer,
    TblOrgaoUnidadeLightSerializer,
    TblOrgaoUnidadeTreeSerializer,
    TblOrganogramaJsonSerializer,
    TblLotacaoVersaoSerializer,
    TblLotacaoVersaoLightSerializer,
    TblLotacaoSerializer,
    TblLotacaoLightSerializer,
    TblLotacaoJsonOrgaoSerializer,
    TblLotacaoInconsistenciaSerializer,
    TblTokenEnvioCargaSerializer,
    TblCargaPatriarcaSerializer,
    TblDetalheStatusCargaSerializer,
    TblStatusProgressoSerializer,
    TblStatusCargaSerializer,
    TblTipoCargaSerializer,
    TblStatusTokenEnvioCargaSerializer,
)
from ..permissions import (
    HasCargaOrgLotPermission,
    IsCoordenadorOrAbove,
    IsGestor,
)
from ..utils.permissions import (
    get_user_app_permissions,
    get_model_permissions,
    require_api_permission,
)


logger = logging.getLogger(__name__)


def get_app_code(request):
    """
    Helper para obter APP_CODE do request ou da config da app.
    """
    # Tenta pegar do middleware
    if hasattr(request, 'app_context') and request.app_context.get('code'):
        return request.app_context['code']
    
    # Fallback: request.app_code
    if hasattr(request, 'app_code') and request.app_code:
        return request.app_code
    
    # Fallback final: pega da configuração da app
    app_config = apps.get_app_config('carga_org_lot')
    return app_config.app_code


# ============================================================================
# ENDPOINT DE PERMISSÕES
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    """
    Retorna permissões do usuário logado para consumo no Next.js.
    ✨ Usa helpers com cache para otimização de performance.
    
    GET /api/v1/carga_org_lot/permissions/
    """
    try:
        app_code = get_app_code(request)
        perms = get_user_app_permissions(request.user, app_code)
        
        # Buscar role do usuário
        user_role = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno=app_code
        ).select_related('role').first()
        
        role = user_role.role.codigoperfil if user_role else None
        
        # Permissões por modelo
        specific = {
            'patriarca': get_model_permissions(request.user, 'tblpatriarca', app_code),
            'organograma': get_model_permissions(request.user, 'tblorganogramaversao', app_code),
            'orgao_unidade': get_model_permissions(request.user, 'tblorgaounidade', app_code),
            'lotacao': get_model_permissions(request.user, 'tbllotacaoversao', app_code),
            'carga': get_model_permissions(request.user, 'tblcargapatriarca', app_code),
            'token': get_model_permissions(request.user, 'tbltokenenviocarga', app_code),
        }
        
        return Response({
            'user_id': request.user.id,
            'email': request.user.email,
            'name': request.user.name,
            'role': role,
            'permissions': list(perms),
            'is_superuser': request.user.is_superuser,
            'groups': {
                'can_manage_patriarcas': any(p in perms for p in [
                    'add_tblpatriarca', 'change_tblpatriarca'
                ]),
                'can_upload': any(p in perms for p in [
                    'add_tblorganogramaversao', 'add_tbllotacaoversao'
                ]),
                'can_process': any(p in perms for p in [
                    'change_tblorganogramaversao', 'change_tbllotacaoversao'
                ]),
                'can_send_api': 'pode_enviar_api' in perms,
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
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    lookup_value_regex = '.*'
    
    def retrieve(self, request, pk=None):
        """GET /api/v1/carga_org_lot/users/{email}/"""
        return self.get_user_by_email(request, pk)
    
    @action(detail=False, methods=['post'])
    def sync_user(self, request):
        """
        Sincroniza usuário do portal.
        POST /api/v1/carga_org_lot/users/sync_user/
        """
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
        """
        Lista usuários com acesso à aplicação.
        GET /api/v1/carga_org_lot/users/list_users/
        """
        try:
            app_code = get_app_code(request)
            
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
        """
        Busca usuário por email.
        GET /api/v1/carga_org_lot/users/{email}/
        """
        try:
            user = User.objects.get(email=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        
        except User.DoesNotExist:
            return Response(
                {'detail': f'Usuário com email {pk} não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================================================
# VIEWSET: TABELAS AUXILIARES (STATUS)
# ============================================================================

class StatusProgressoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para Status de Progresso (somente leitura)"""
    queryset = TblStatusProgresso.objects.all()
    serializer_class = TblStatusProgressoSerializer
    permission_classes = [IsAuthenticated]


class StatusCargaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para Status de Carga (somente leitura)"""
    queryset = TblStatusCarga.objects.all()
    serializer_class = TblStatusCargaSerializer
    permission_classes = [IsAuthenticated]


class TipoCargaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para Tipo de Carga (somente leitura)"""
    queryset = TblTipoCarga.objects.all()
    serializer_class = TblTipoCargaSerializer
    permission_classes = [IsAuthenticated]


class StatusTokenEnvioCargaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para Status Token Envio Carga (somente leitura)"""
    queryset = TblStatusTokenEnvioCarga.objects.all()
    serializer_class = TblStatusTokenEnvioCargaSerializer
    permission_classes = [IsAuthenticated]


# ============================================================================
# VIEWSET: PATRIARCAS
# ============================================================================

class PatriarcaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Patriarcas.
    
    🔒 Permissões verificadas automaticamente:
    - GET: requer view_tblpatriarca
    - POST: requer add_tblpatriarca
    - PUT/PATCH: requer change_tblpatriarca
    - DELETE: requer delete_tblpatriarca
    """
    queryset = TblPatriarca.objects.select_related(
        'id_status_progresso',
        'id_usuario_criacao'
    ).all()
    serializer_class = TblPatriarcaSerializer
    permission_classes = [HasCargaOrgLotPermission]
    
    def get_serializer_class(self):
        """Retorna serializer otimizado para listagem"""
        if self.action == 'list':
            return TblPatriarcaLightSerializer
        return TblPatriarcaSerializer
    
    def get_queryset(self):
        """Permite filtros via query params"""
        queryset = super().get_queryset()
        
        # Filtro por sigla
        sigla = self.request.query_params.get('sigla', None)
        if sigla:
            queryset = queryset.filter(str_sigla_patriarca__icontains=sigla)
        
        # Filtro por status
        status_id = self.request.query_params.get('status', None)
        if status_id:
            queryset = queryset.filter(id_status_progresso_id=status_id)
        
        return queryset.order_by('str_sigla_patriarca')
    
    def perform_create(self, serializer):
        """Define usuário de criação"""
        serializer.save(id_usuario_criacao=self.request.user)
    
    def perform_update(self, serializer):
        """Define usuário de alteração"""
        serializer.save(
            id_usuario_alteracao=self.request.user,
            dat_alteracao=timezone.now()
        )
    
    @action(detail=False, methods=['get'])
    @require_api_permission('view_tblpatriarca')
    def list_light(self, request):
        """
        Endpoint otimizado para listagem rápida.
        GET /api/v1/carga_org_lot/patriarcas/list_light/
        """
        patriarcas = TblPatriarca.objects.all().values(
            'id_patriarca', 
            'str_sigla_patriarca', 
            'str_nome'
        )
        return Response({
            'count': len(patriarcas),
            'results': list(patriarcas)
        })
    
    @action(detail=True, methods=['get'])
    def organogramas(self, request, pk=None):
        """
        GET /api/v1/carga_org_lot/patriarcas/{id}/organogramas/
        Lista organogramas do patriarca.
        """
        patriarca = self.get_object()
        organogramas = TblOrganogramaVersao.objects.filter(
            id_patriarca=patriarca
        ).order_by('-dat_processamento')
        
        serializer = TblOrganogramaVersaoLightSerializer(organogramas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def lotacoes(self, request, pk=None):
        """
        GET /api/v1/carga_org_lot/patriarcas/{id}/lotacoes/
        Lista versões de lotação do patriarca.
        """
        patriarca = self.get_object()
        lotacoes = TblLotacaoVersao.objects.filter(
            id_patriarca=patriarca
        ).order_by('-dat_processamento')
        
        serializer = TblLotacaoVersaoLightSerializer(lotacoes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def estatisticas(self, request, pk=None):
        """
        GET /api/v1/carga_org_lot/patriarcas/{id}/estatisticas/
        Estatísticas do patriarca.
        """
        patriarca = self.get_object()
        
        stats = {
            'patriarca': {
                'id': patriarca.id_patriarca,
                'sigla': patriarca.str_sigla_patriarca,
                'nome': patriarca.str_nome,
            },
            'organogramas': {
                'total': patriarca.versoes_organograma.count(),
                'ativos': patriarca.versoes_organograma.filter(flg_ativo=True).count(),
            },
            'lotacoes': {
                'total': patriarca.versoes_lotacao.count(),
                'ativas': patriarca.versoes_lotacao.filter(flg_ativo=True).count(),
            },
            'cargas': {
                'total': patriarca.cargas.count(),
                'por_status': list(
                    patriarca.cargas.values('id_status_carga__str_descricao')
                    .annotate(count=Count('id_carga_patriarca'))
                ),
            },
        }
        
        return Response(stats)


# ============================================================================
# VIEWSET: ORGANOGRAMAS
# ============================================================================

class OrganogramaVersaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Versões de Organograma.
    
    🔒 Permissões verificadas automaticamente.
    """
    queryset = TblOrganogramaVersao.objects.select_related('id_patriarca').all()
    serializer_class = TblOrganogramaVersaoSerializer
    permission_classes = [HasCargaOrgLotPermission]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TblOrganogramaVersaoLightSerializer
        return TblOrganogramaVersaoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por patriarca
        patriarca_id = self.request.query_params.get('patriarca', None)
        if patriarca_id:
            queryset = queryset.filter(id_patriarca_id=patriarca_id)
        
        # Filtro apenas ativos
        apenas_ativos = self.request.query_params.get('ativos', None)
        if apenas_ativos == 'true':
            queryset = queryset.filter(flg_ativo=True)
        
        # Filtro por status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(str_status_processamento=status)
        
        return queryset.order_by('-dat_processamento')
    
    @action(detail=True, methods=['post'], permission_classes=[IsCoordenadorOrAbove])
    def ativar(self, request, pk=None):
        """
        Ativa um organograma específico.
        🔒 Apenas Coordenadores e Gestores.
        
        POST /api/v1/carga_org_lot/organogramas/{id}/ativar/
        """
        try:
            from django.db import transaction
            
            with transaction.atomic():
                organograma = self.get_object()
                patriarca = organograma.id_patriarca
                
                # Desativa todos os organogramas do patriarca
                TblOrganogramaVersao.objects.filter(
                    id_patriarca=patriarca
                ).update(flg_ativo=False)
                
                # Ativa o organograma selecionado
                organograma.flg_ativo = True
                organograma.save()
                
                serializer = self.get_serializer(organograma)
                
                logger.info(
                    f"Organograma {organograma.id_organograma_versao} ativado por {request.user.email}"
                )
                
                return Response({
                    'detail': 'Organograma ativado com sucesso',
                    'organograma': serializer.data
                })
        
        except Exception as e:
            logger.error(f"Erro ao ativar organograma: {str(e)}")
            return Response(
                {'detail': f'Erro ao ativar organograma: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def orgaos(self, request, pk=None):
        """
        GET /api/v1/carga_org_lot/organogramas/{id}/orgaos/
        Lista órgãos/unidades (flat).
        """
        organograma = self.get_object()
        orgaos = TblOrgaoUnidade.objects.filter(
            id_organograma_versao=organograma
        ).select_related(
            'id_orgao_unidade_pai'
        ).order_by('str_numero_hierarquia')
        
        serializer = TblOrgaoUnidadeLightSerializer(orgaos, many=True)
        return Response({
            'count': orgaos.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def hierarquia(self, request, pk=None):
        """
        GET /api/v1/carga_org_lot/organogramas/{id}/hierarquia/
        Retorna estrutura hierárquica em árvore.
        """
        organograma = self.get_object()
        
        # Buscar órgãos raiz
        orgaos_raiz = TblOrgaoUnidade.objects.filter(
            id_organograma_versao=organograma,
            id_orgao_unidade_pai__isnull=True,
            flg_ativo=True
        ).order_by('str_numero_hierarquia')
        
        serializer = TblOrgaoUnidadeTreeSerializer(orgaos_raiz, many=True)
        
        return Response({
            'organograma_id': organograma.id_organograma_versao,
            'patriarca': organograma.id_patriarca.str_sigla_patriarca,
            'hierarquia': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def json_envio(self, request, pk=None):
        """
        GET /api/v1/carga_org_lot/organogramas/{id}/json_envio/
        Retorna JSON formatado para envio.
        """
        organograma = self.get_object()
        
        try:
            json_org = TblOrganogramaJson.objects.get(id_organograma_versao=organograma)
            serializer = TblOrganogramaJsonSerializer(json_org)
            return Response(serializer.data)
        except TblOrganogramaJson.DoesNotExist:
            return Response(
                {'detail': 'JSON de envio não encontrado para este organograma'},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================================================
# VIEWSET: ÓRGÃOS/UNIDADES
# ============================================================================

class OrgaoUnidadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Órgãos/Unidades.
    
    🔒 Permissões verificadas automaticamente.
    """
    queryset = TblOrgaoUnidade.objects.select_related(
        'id_patriarca',
        'id_organograma_versao',
        'id_orgao_unidade_pai'
    ).all()
    serializer_class = TblOrgaoUnidadeSerializer
    permission_classes = [HasCargaOrgLotPermission]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TblOrgaoUnidadeLightSerializer
        return TblOrgaoUnidadeSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por patriarca
        patriarca_id = self.request.query_params.get('patriarca', None)
        if patriarca_id:
            queryset = queryset.filter(id_patriarca_id=patriarca_id)
        
        # Filtro por organograma
        organograma_id = self.request.query_params.get('organograma', None)
        if organograma_id:
            queryset = queryset.filter(id_organograma_versao_id=organograma_id)
        
        # Filtro apenas ativos
        apenas_ativos = self.request.query_params.get('ativos', None)
        if apenas_ativos == 'true':
            queryset = queryset.filter(flg_ativo=True)
        
        # Filtro apenas raiz
        apenas_raiz = self.request.query_params.get('raiz', None)
        if apenas_raiz == 'true':
            queryset = queryset.filter(id_orgao_unidade_pai__isnull=True)
        
        # Busca por sigla ou nome
        q = self.request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(str_sigla__icontains=q) | Q(str_nome__icontains=q)
            )
        
        return queryset.order_by('str_numero_hierarquia')
    
    def perform_create(self, serializer):
        serializer.save(id_usuario_criacao=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(
            id_usuario_alteracao=self.request.user,
            dat_alteracao=timezone.now()
        )


# ============================================================================
# VIEWSET: LOTAÇÕES
# ============================================================================

class LotacaoVersaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Versões de Lotação.
    
    🔒 Permissões verificadas automaticamente.
    """
    queryset = TblLotacaoVersao.objects.select_related(
        'id_patriarca',
        'id_organograma_versao'
    ).all()
    serializer_class = TblLotacaoVersaoSerializer
    permission_classes = [HasCargaOrgLotPermission]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TblLotacaoVersaoLightSerializer
        return TblLotacaoVersaoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por patriarca
        patriarca_id = self.request.query_params.get('patriarca', None)
        if patriarca_id:
            queryset = queryset.filter(id_patriarca_id=patriarca_id)
        
        # Filtro apenas ativas
        apenas_ativas = self.request.query_params.get('ativas', None)
        if apenas_ativas == 'true':
            queryset = queryset.filter(flg_ativo=True)
        
        # Filtro por status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(str_status_processamento=status)
        
        return queryset.order_by('-dat_processamento')
    
    @action(detail=True, methods=['post'], permission_classes=[IsCoordenadorOrAbove])
    def ativar(self, request, pk=None):
        """
        Ativa uma versão de lotação específica.
        🔒 Apenas Coordenadores e Gestores.
        
        POST /api/v1/carga_org_lot/lotacoes/{id}/ativar/
        """
        try:
            from django.db import transaction
            
            with transaction.atomic():
                lotacao = self.get_object()
                patriarca = lotacao.id_patriarca
                
                # Desativa todas as lotações do patriarca
                TblLotacaoVersao.objects.filter(
                    id_patriarca=patriarca
                ).update(flg_ativo=False)
                
                # Ativa a lotação selecionada
                lotacao.flg_ativo = True
                lotacao.save()
                
                serializer = self.get_serializer(lotacao)
                
                logger.info(
                    f"Lotação {lotacao.id_lotacao_versao} ativada por {request.user.email}"
                )
                
                return Response({
                    'detail': 'Lotação ativada com sucesso',
                    'lotacao': serializer.data
                })
        
        except Exception as e:
            logger.error(f"Erro ao ativar lotação: {str(e)}")
            return Response(
                {'detail': f'Erro ao ativar lotação: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def registros(self, request, pk=None):
        """
        GET /api/v1/carga_org_lot/lotacoes/{id}/registros/
        Lista registros de lotação (servidores).
        """
        versao = self.get_object()
        
        # Paginação
        page_size = int(request.query_params.get('page_size', 100))
        page = int(request.query_params.get('page', 1))
        offset = (page - 1) * page_size
        
        # Filtros
        lotacoes = TblLotacao.objects.filter(id_lotacao_versao=versao)
        
        valido = request.query_params.get('valido', None)
        if valido == 'true':
            lotacoes = lotacoes.filter(flg_valido=True)
        elif valido == 'false':
            lotacoes = lotacoes.filter(flg_valido=False)
        
        cpf = request.query_params.get('cpf', None)
        if cpf:
            lotacoes = lotacoes.filter(str_cpf__icontains=cpf)
        
        orgao_id = request.query_params.get('orgao', None)
        if orgao_id:
            lotacoes = lotacoes.filter(id_orgao_lotacao_id=orgao_id)
        
        total = lotacoes.count()
        lotacoes = lotacoes.select_related(
            'id_orgao_lotacao',
            'id_unidade_lotacao'
        )[offset:offset+page_size]
        
        serializer = TblLotacaoLightSerializer(lotacoes, many=True)
        
        return Response({
            'total': total,
            'page': page,
            'page_size': page_size,
            'pages': (total + page_size - 1) // page_size,
            'results': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def inconsistencias(self, request, pk=None):
        """
        GET /api/v1/carga_org_lot/lotacoes/{id}/inconsistencias/
        Lista inconsistências.
        """
        versao = self.get_object()
        
        inconsistencias = TblLotacaoInconsistencia.objects.filter(
            id_lotacao__id_lotacao_versao=versao
        ).select_related(
            'id_lotacao',
            'id_lotacao__id_orgao_lotacao'
        ).order_by('-dat_registro')
        
        serializer = TblLotacaoInconsistenciaSerializer(inconsistencias, many=True)
        
        return Response({
            'total': inconsistencias.count(),
            'inconsistencias': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def estatisticas(self, request, pk=None):
        """
        GET /api/v1/carga_org_lot/lotacoes/{id}/estatisticas/
        Estatísticas da versão.
        """
        versao = self.get_object()
        
        stats = {
            'total_registros': versao.total_lotacoes,
            'validos': versao.total_validas,
            'invalidos': versao.total_invalidas,
            'taxa_sucesso': round(
                (versao.total_validas / versao.total_lotacoes * 100) if versao.total_lotacoes > 0 else 0,
                2
            ),
            'total_inconsistencias': TblLotacaoInconsistencia.objects.filter(
                id_lotacao__id_lotacao_versao=versao
            ).count(),
            'por_orgao': list(
                TblLotacao.objects.filter(id_lotacao_versao=versao)
                .values('id_orgao_lotacao__str_sigla')
                .annotate(count=Count('id_lotacao'))
                .order_by('-count')[:10]
            )
        }
        
        return Response(stats)


# ============================================================================
# VIEWSET: CARGAS
# ============================================================================

class CargaPatriarcaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Cargas de Patriarca.
    
    🔒 Permissões verificadas automaticamente.
    """
    queryset = TblCargaPatriarca.objects.select_related(
        'id_patriarca',
        'id_status_carga',
        'id_tipo_carga',
        'id_token_envio_carga'
    ).all()
    serializer_class = TblCargaPatriarcaSerializer
    permission_classes = [HasCargaOrgLotPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por patriarca
        patriarca_id = self.request.query_params.get('patriarca', None)
        if patriarca_id:
            queryset = queryset.filter(id_patriarca_id=patriarca_id)
        
        # Filtro por tipo
        tipo_id = self.request.query_params.get('tipo', None)
        if tipo_id:
            queryset = queryset.filter(id_tipo_carga_id=tipo_id)
        
        # Filtro por status
        status_id = self.request.query_params.get('status', None)
        if status_id:
            queryset = queryset.filter(id_status_carga_id=status_id)
        
        return queryset.order_by('-dat_data_hora_inicio')
    
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """
        GET /api/v1/carga_org_lot/cargas/{id}/timeline/
        Timeline de mudanças de status.
        """
        carga = self.get_object()
        
        detalhes = TblDetalheStatusCarga.objects.filter(
            id_carga_patriarca=carga
        ).select_related('id_status_carga').order_by('dat_registro')
        
        serializer = TblDetalheStatusCargaSerializer(detalhes, many=True)
        
        return Response({
            'carga_id': carga.id_carga_patriarca,
            'timeline': serializer.data
        })


# ============================================================================
# VIEWSET: TOKENS
# ============================================================================

class TokenEnvioCargaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Tokens de Envio de Carga.
    
    🔒 Permissões verificadas automaticamente.
    """
    queryset = TblTokenEnvioCarga.objects.select_related(
        'id_patriarca',
        'id_status_token_envio_carga'
    ).all()
    serializer_class = TblTokenEnvioCargaSerializer
    permission_classes = [HasCargaOrgLotPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por patriarca
        patriarca_id = self.request.query_params.get('patriarca', None)
        if patriarca_id:
            queryset = queryset.filter(id_patriarca_id=patriarca_id)
        
        # Filtro apenas ativos
        apenas_ativos = self.request.query_params.get('ativos', None)
        if apenas_ativos == 'true':
            queryset = queryset.filter(dat_data_hora_fim__isnull=True)
        
        return queryset.order_by('-dat_data_hora_inicio')


# ============================================================================
# ENDPOINT DE DASHBOARD
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    GET /api/v1/carga_org_lot/dashboard/
    Retorna estatísticas gerais do sistema.
    """
    # Filtro por patriarca (opcional)
    patriarca_id = request.query_params.get('patriarca', None)
    
    # Base queryset
    patriarcas_qs = TblPatriarca.objects.all()
    if patriarca_id:
        patriarcas_qs = patriarcas_qs.filter(id_patriarca=patriarca_id)
    
    stats = {
        'patriarcas': {
            'total': patriarcas_qs.count(),
            'por_status': list(
                patriarcas_qs.values('id_status_progresso__str_descricao')
                .annotate(count=Count('id_patriarca'))
            )
        },
        'organogramas': {
            'total': TblOrganogramaVersao.objects.filter(
                id_patriarca__in=patriarcas_qs
            ).count(),
            'ativos': TblOrganogramaVersao.objects.filter(
                id_patriarca__in=patriarcas_qs,
                flg_ativo=True
            ).count(),
            'por_status': list(
                TblOrganogramaVersao.objects.filter(
                    id_patriarca__in=patriarcas_qs
                ).values('str_status_processamento')
                .annotate(count=Count('id_organograma_versao'))
            ),
        },
        'lotacoes': {
            'total_versoes': TblLotacaoVersao.objects.filter(
                id_patriarca__in=patriarcas_qs
            ).count(),
            'versoes_ativas': TblLotacaoVersao.objects.filter(
                id_patriarca__in=patriarcas_qs,
                flg_ativo=True
            ).count(),
            'total_registros': TblLotacao.objects.filter(
                id_patriarca__in=patriarcas_qs
            ).count(),
            'validos': TblLotacao.objects.filter(
                id_patriarca__in=patriarcas_qs,
                flg_valido=True
            ).count(),
            'invalidos': TblLotacao.objects.filter(
                id_patriarca__in=patriarcas_qs,
                flg_valido=False
            ).count(),
        },
        'cargas': {
            'total': TblCargaPatriarca.objects.filter(
                id_patriarca__in=patriarcas_qs
            ).count(),
            'por_status': list(
                TblCargaPatriarca.objects.filter(
                    id_patriarca__in=patriarcas_qs
                ).values('id_status_carga__str_descricao')
                .annotate(count=Count('id_carga_patriarca'))
            ),
            'por_tipo': list(
                TblCargaPatriarca.objects.filter(
                    id_patriarca__in=patriarcas_qs
                ).values('id_tipo_carga__str_descricao')
                .annotate(count=Count('id_carga_patriarca'))
            )
        }
    }
    
    return Response(stats)


# ============================================================================
# ENDPOINTS DE BUSCA RÁPIDA
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_orgao(request):
    """
    GET /api/v1/carga_org_lot/search/orgao/?q=termo&patriarca_id=1
    Busca órgãos por sigla ou nome.
    """
    query = request.query_params.get('q', '')
    patriarca_id = request.query_params.get('patriarca_id', None)
    
    if len(query) < 2:
        return Response({'results': []})
    
    orgaos = TblOrgaoUnidade.objects.filter(
        Q(str_sigla__icontains=query) | Q(str_nome__icontains=query),
        flg_ativo=True
    )
    
    if patriarca_id:
        orgaos = orgaos.filter(id_patriarca_id=patriarca_id)
    
    orgaos = orgaos.select_related('id_patriarca')[:20]
    
    results = [
        {
            'id': o.id_orgao_unidade,
            'sigla': o.str_sigla,
            'nome': o.str_nome,
            'patriarca': o.id_patriarca.str_sigla_patriarca,
            'nivel': o.int_nivel_hierarquia
        }
        for o in orgaos
    ]
    
    return Response({'results': results})
