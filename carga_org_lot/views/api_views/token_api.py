"""
API ViewSets para Token de Envio e Tabelas Auxiliares
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.utils import timezone

from ...models import (
    TblTokenEnvioCarga,
    TblStatusProgresso,
    TblStatusCarga,
    TblTipoCarga,
    TblStatusTokenEnvioCarga,
)
from ...serializers import (
    TblTokenEnvioCargaSerializer,
    TblStatusProgressoSerializer,
    TblStatusCargaSerializer,
    TblTipoCargaSerializer,
    TblStatusTokenEnvioCargaSerializer,
)


# ============================================
# VIEWSETS PARA TABELAS AUXILIARES (READ-ONLY)
# ============================================

class StatusProgressoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet READ-ONLY para Status Progresso.
    
    list:     GET /api/carga_org_lot/status-progresso/
    retrieve: GET /api/carga_org_lot/status-progresso/{id}/
    """
    queryset = TblStatusProgresso.objects.all()
    serializer_class = TblStatusProgressoSerializer
    permission_classes = [IsAuthenticated]


class StatusCargaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet READ-ONLY para Status Carga.
    
    list:     GET /api/carga_org_lot/status-carga/
    retrieve: GET /api/carga_org_lot/status-carga/{id}/
    """
    queryset = TblStatusCarga.objects.all()
    serializer_class = TblStatusCargaSerializer
    permission_classes = [IsAuthenticated]


class TipoCargaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet READ-ONLY para Tipo Carga.
    
    list:     GET /api/carga_org_lot/tipo-carga/
    retrieve: GET /api/carga_org_lot/tipo-carga/{id}/
    """
    queryset = TblTipoCarga.objects.all()
    serializer_class = TblTipoCargaSerializer
    permission_classes = [IsAuthenticated]


class StatusTokenEnvioCargaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet READ-ONLY para Status Token Envio Carga.
    
    list:     GET /api/carga_org_lot/status-token/
    retrieve: GET /api/carga_org_lot/status-token/{id}/
    """
    queryset = TblStatusTokenEnvioCarga.objects.all()
    serializer_class = TblStatusTokenEnvioCargaSerializer
    permission_classes = [IsAuthenticated]


# ============================================
# VIEWSET PARA TOKEN DE ENVIO
# ============================================

class TokenEnvioCargaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Tokens de Envio de Carga.
    
    Tokens são usados para rastrear processos de envio de dados à API externa.
    
    list:    GET /api/carga_org_lot/tokens/
    create:  POST /api/carga_org_lot/tokens/
    retrieve: GET /api/carga_org_lot/tokens/{id}/
    update:   PUT /api/carga_org_lot/tokens/{id}/
    partial_update: PATCH /api/carga_org_lot/tokens/{id}/
    destroy:  DELETE /api/carga_org_lot/tokens/{id}/
    """
    queryset = TblTokenEnvioCarga.objects.select_related(
        'id_patriarca',
        'id_status_token_envio_carga'
    ).all()
    serializer_class = TblTokenEnvioCargaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtros via query params"""
        queryset = super().get_queryset()
        
        # Filtro por patriarca
        patriarca_id = self.request.query_params.get('patriarca', None)
        if patriarca_id:
            queryset = queryset.filter(id_patriarca_id=patriarca_id)
        
        # Filtro por status
        status_id = self.request.query_params.get('status', None)
        if status_id:
            queryset = queryset.filter(id_status_token_envio_carga_id=status_id)
        
        # Filtro apenas ativos (sem data fim)
        apenas_ativos = self.request.query_params.get('ativos', None)
        if apenas_ativos == 'true':
            queryset = queryset.filter(dat_data_hora_fim__isnull=True)
        
        return queryset.order_by('-dat_data_hora_inicio')
    
    @action(detail=True, methods=['get'])
    def cargas(self, request, pk=None):
        """
        GET /api/carga_org_lot/tokens/{id}/cargas/
        
        Lista cargas associadas ao token.
        """
        token = self.get_object()
        
        from ...models import TblCargaPatriarca
        from ...serializers import TblCargaPatriarcaSerializer
        
        cargas = TblCargaPatriarca.objects.filter(
            id_token_envio_carga=token
        ).select_related(
            'id_patriarca',
            'id_status_carga',
            'id_tipo_carga'
        ).order_by('-dat_data_hora_inicio')
        
        serializer = TblCargaPatriarcaSerializer(cargas, many=True)
        
        return Response({
            'token_id': token.id_token_envio_carga,
            'total_cargas': cargas.count(),
            'cargas': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        """
        POST /api/carga_org_lot/tokens/{id}/finalizar/
        
        Finaliza um token (define data/hora fim).
        
        Body (opcional):
            - status_id: ID do novo status (se quiser alterar)
        """
        token = self.get_object()
        
        if token.dat_data_hora_fim:
            return Response(
                {'error': 'Token já foi finalizado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualizar data fim
        token.dat_data_hora_fim = timezone.now()
        
        # Atualizar status se fornecido
        novo_status_id = request.data.get('status_id', None)
        if novo_status_id:
            token.id_status_token_envio_carga_id = novo_status_id
        
        token.save()
        
        serializer = self.get_serializer(token)
        return Response({
            'message': 'Token finalizado com sucesso',
            'token': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def validar(self, request, pk=None):
        """
        GET /api/carga_org_lot/tokens/{id}/validar/
        
        Valida se o token ainda é válido (não finalizado).
        """
        token = self.get_object()
        
        valido = token.dat_data_hora_fim is None
        
        return Response({
            'token_id': token.id_token_envio_carga,
            'valido': valido,
            'data_inicio': token.dat_data_hora_inicio,
            'data_fim': token.dat_data_hora_fim,
            'status': token.id_status_token_envio_carga.str_descricao,
            'duracao_minutos': self._calcular_duracao(token) if not valido else None
        })
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """
        GET /api/carga_org_lot/tokens/estatisticas/
        
        Estatísticas gerais de tokens.
        """
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'ativos': queryset.filter(dat_data_hora_fim__isnull=True).count(),
            'finalizados': queryset.filter(dat_data_hora_fim__isnull=False).count(),
            'por_status': list(
                queryset.values('id_status_token_envio_carga__str_descricao')
                .annotate(count=Count('id_token_envio_carga'))
                .order_by('-count')
            ),
            'por_patriarca': list(
                queryset.values('id_patriarca__str_sigla_patriarca')
                .annotate(count=Count('id_token_envio_carga'))
                .order_by('-count')[:10]
            )
        }
        
        return Response(stats)
    
    def _calcular_duracao(self, token):
        """Calcula duração do token em minutos"""
        if not token.dat_data_hora_fim:
            return None
        
        duracao = token.dat_data_hora_fim - token.dat_data_hora_inicio
        return int(duracao.total_seconds() / 60)
