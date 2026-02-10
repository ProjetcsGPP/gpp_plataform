"""
Acoes Views - ViewSets para gerenciamento de ações.
Inclui: Acoes, AcaoPrazo, AcaoDestaque.
"""

import logging
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ...models import Acoes, AcaoPrazo, AcaoDestaque
from ...serializers import (
    AcoesSerializer, AcoesListSerializer,
    AcaoPrazoSerializer,
    AcaoDestaqueSerializer,
    RelacaoAcaoUsuarioResponsavelSerializer
)

logger = logging.getLogger(__name__)


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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strapelido', 'strdescricaoacao', 'strdescricaoentrega']
    ordering_fields = ['strapelido', 'datdataentrega', 'created_at']
    ordering = ['strapelido']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros opcionais via query params
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
    """
    queryset = AcaoPrazo.objects.select_related('idacao')
    serializer_class = AcaoPrazoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strprazo', 'idacao__strapelido']
    ordering_fields = ['created_at', 'isacaoprazoativo']
    ordering = ['-isacaoprazoativo', '-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros opcionais
        if self.request.query_params.get('idacao'):
            queryset = queryset.filter(idacao=self.request.query_params.get('idacao'))
        if self.request.query_params.get('isacaoprazoativo'):
            queryset = queryset.filter(isacaoprazoativo=self.request.query_params.get('isacaoprazoativo'))
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
    """
    queryset = AcaoDestaque.objects.select_related('idacao')
    serializer_class = AcaoDestaqueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['idacao__strapelido']
    ordering_fields = ['datdatadestaque', 'created_at']
    ordering = ['-datdatadestaque']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtro opcional
        if self.request.query_params.get('idacao'):
            queryset = queryset.filter(idacao=self.request.query_params.get('idacao'))
        return queryset
