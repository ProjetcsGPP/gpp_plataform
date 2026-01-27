"""
API ViewSet para Patriarca
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ...models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblLotacaoVersao,
)
from ...serializers import (
    TblPatriarcaSerializer,
    TblOrganogramaVersaoSerializer,
    TblLotacaoVersaoSerializer,
)


class PatriarcaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Patriarcas.
    
    list:    GET /api/carga_org_lot/patriarcas/
    create:  POST /api/carga_org_lot/patriarcas/
    retrieve: GET /api/carga_org_lot/patriarcas/{id}/
    update:  PUT /api/carga_org_lot/patriarcas/{id}/
    partial_update: PATCH /api/carga_org_lot/patriarcas/{id}/
    destroy: DELETE /api/carga_org_lot/patriarcas/{id}/
    """
    queryset = TblPatriarca.objects.select_related(
        'id_status_progresso',
        'id_usuario_criacao'
    ).all()
    serializer_class = TblPatriarcaSerializer
    permission_classes = [IsAuthenticated]
    
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
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def organogramas(self, request, pk=None):
        """
        GET /api/carga_org_lot/patriarcas/{id}/organogramas/
        
        Lista organogramas do patriarca.
        """
        patriarca = self.get_object()
        organogramas = TblOrganogramaVersao.objects.filter(
            id_patriarca=patriarca
        ).order_by('-dat_processamento')
        
        serializer = TblOrganogramaVersaoSerializer(organogramas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def lotacoes(self, request, pk=None):
        """
        GET /api/carga_org_lot/patriarcas/{id}/lotacoes/
        
        Lista versões de lotação do patriarca.
        """
        patriarca = self.get_object()
        lotacoes = TblLotacaoVersao.objects.filter(
            id_patriarca=patriarca
        ).order_by('-dat_processamento')
        
        serializer = TblLotacaoVersaoSerializer(lotacoes, many=True)
        return Response(serializer.data)
