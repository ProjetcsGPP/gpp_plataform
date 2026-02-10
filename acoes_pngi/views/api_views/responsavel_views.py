"""
Responsavel Views - ViewSets para gerenciamento de responsáveis.
Inclui: UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel.
"""

import logging
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from ...models import UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel
from ...serializers import (
    UsuarioResponsavelSerializer,
    RelacaoAcaoUsuarioResponsavelSerializer
)

logger = logging.getLogger(__name__)


class UsuarioResponsavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Usuários Responsáveis.
    """
    queryset = UsuarioResponsavel.objects.select_related('idusuario')
    serializer_class = UsuarioResponsavelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['idusuario__name', 'idusuario__email', 'strorgao', 'strtelefone']
    ordering_fields = ['created_at']
    ordering = ['idusuario__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtro opcional
        if self.request.query_params.get('strorgao'):
            queryset = queryset.filter(strorgao__icontains=self.request.query_params.get('strorgao'))
        return queryset


class RelacaoAcaoUsuarioResponsavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Relações entre Ações e Usuários Responsáveis.
    """
    queryset = RelacaoAcaoUsuarioResponsavel.objects.select_related(
        'idacao', 'idusuarioresponsavel__idusuario'
    )
    serializer_class = RelacaoAcaoUsuarioResponsavelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'idacao__strapelido',
        'idusuarioresponsavel__idusuario__name'
    ]
    ordering_fields = ['created_at']
    ordering = ['idacaousuarioresponsavel']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros opcionais
        if self.request.query_params.get('idacao'):
            queryset = queryset.filter(idacao=self.request.query_params.get('idacao'))
        if self.request.query_params.get('idusuarioresponsavel'):
            queryset = queryset.filter(idusuarioresponsavel=self.request.query_params.get('idusuarioresponsavel'))
        return queryset
