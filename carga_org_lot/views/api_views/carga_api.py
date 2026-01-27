"""
API ViewSet para Carga
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ...models import (
    TblCargaPatriarca,
    TblDetalheStatusCarga,
)
from ...serializers import TblCargaPatriarcaSerializer


class CargaPatriarcaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Cargas de Patriarca.
    
    list:    GET /api/carga_org_lot/cargas/
    create:  POST /api/carga_org_lot/cargas/
    retrieve: GET /api/carga_org_lot/cargas/{id}/
    """
    queryset = TblCargaPatriarca.objects.select_related(
        'id_patriarca',
        'id_status_carga',
        'id_tipo_carga',
        'id_token_envio_carga'
    ).all()
    serializer_class = TblCargaPatriarcaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por patriarca
        patriarca_id = self.request.query_params.get('patriarca', None)
        if patriarca_id:
            queryset = queryset.filter(id_patriarca_id=patriarca_id)
        
        # Filtro por tipo de carga
        tipo_carga = self.request.query_params.get('tipo', None)
        if tipo_carga:
            queryset = queryset.filter(id_tipo_carga_id=tipo_carga)
        
        # Filtro por status
        status_id = self.request.query_params.get('status', None)
        if status_id:
            queryset = queryset.filter(id_status_carga_id=status_id)
        
        return queryset.order_by('-dat_data_hora_inicio')
    
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """
        GET /api/carga_org_lot/cargas/{id}/timeline/
        
        Timeline de mudanças de status da carga.
        """
        carga = self.get_object()
        
        detalhes = TblDetalheStatusCarga.objects.filter(
            id_carga_patriarca=carga
        ).select_related('id_status_carga').order_by('dat_registro')
        
        timeline = detalhes.values(
            'id_detalhe_status_carga',
            'dat_registro',
            'id_status_carga__str_descricao',
            'id_status_carga__flg_sucesso',
            'str_mensagem'
        )
        
        return Response({
            'carga_id': carga.id_carga_patriarca,
            'timeline': list(timeline)
        })
