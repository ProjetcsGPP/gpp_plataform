"""
Responsavel Views - ViewSets para gerenciamento de responsáveis.
Inclui: UsuarioResponsavel, RelacaoAcaoUsuarioResponsavel.
"""

import logging
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

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
