"""
Alinhamento Views - ViewSets para gerenciamento de anotações de alinhamento.
Inclui: TipoAnotacaoAlinhamento, AcaoAnotacaoAlinhamento.
"""

import logging
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from ...models import TipoAnotacaoAlinhamento, AcaoAnotacaoAlinhamento
from ...serializers import (
    TipoAnotacaoAlinhamentoSerializer,
    AcaoAnotacaoAlinhamentoSerializer
)

logger = logging.getLogger(__name__)


class TipoAnotacaoAlinhamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Tipos de Anotação de Alinhamento.
    """
    queryset = TipoAnotacaoAlinhamento.objects.all()
    serializer_class = TipoAnotacaoAlinhamentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'idacao__strapelido',
        'strdescricaoanotacaoalinhamento',
        'strnumeromonitoramento'
    ]
    ordering_fields = ['datdataanotacaoalinhamento', 'created_at']
    ordering = ['-datdataanotacaoalinhamento']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros opcionais
        if self.request.query_params.get('idacao'):
            queryset = queryset.filter(idacao=self.request.query_params.get('idacao'))
        if self.request.query_params.get('idtipoanotacaoalinhamento'):
            queryset = queryset.filter(idtipoanotacaoalinhamento=self.request.query_params.get('idtipoanotacaoalinhamento'))
        return queryset
