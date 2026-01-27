"""
API ViewSet para Lotação
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

from ...models import (
    TblLotacaoVersao,
    TblLotacao,
    TblLotacaoInconsistencia,
)
from ...serializers import (
    TblLotacaoVersaoSerializer,
    TblLotacaoSerializer,
)


class LotacaoVersaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Versões de Lotação.
    
    list:    GET /api/carga_org_lot/lotacoes/
    create:  POST /api/carga_org_lot/lotacoes/
    retrieve: GET /api/carga_org_lot/lotacoes/{id}/
    """
    queryset = TblLotacaoVersao.objects.select_related(
        'id_patriarca',
        'id_organograma_versao'
    ).all()
    serializer_class = TblLotacaoVersaoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        patriarca_id = self.request.query_params.get('patriarca', None)
        if patriarca_id:
            queryset = queryset.filter(id_patriarca_id=patriarca_id)
        
        return queryset.order_by('-dat_processamento')
    
    @action(detail=True, methods=['get'])
    def registros(self, request, pk=None):
        """
        GET /api/carga_org_lot/lotacoes/{id}/registros/
        
        Lista registros de lotação (servidores).
        """
        versao = self.get_object()
        
        # Paginação
        page_size = int(request.query_params.get('page_size', 100))
        page = int(request.query_params.get('page', 1))
        offset = (page - 1) * page_size
        
        # Filtros
        lotacoes = TblLotacao.objects.filter(id_lotacao_versao=versao)
        
        # Filtro apenas válidos/inválidos
        valido = request.query_params.get('valido', None)
        if valido == 'true':
            lotacoes = lotacoes.filter(flg_valido=True)
        elif valido == 'false':
            lotacoes = lotacoes.filter(flg_valido=False)
        
        # CPF
        cpf = request.query_params.get('cpf', None)
        if cpf:
            lotacoes = lotacoes.filter(str_cpf__icontains=cpf)
        
        total = lotacoes.count()
        lotacoes = lotacoes.select_related(
            'id_orgao_lotacao',
            'id_unidade_lotacao'
        )[offset:offset+page_size]
        
        serializer = TblLotacaoSerializer(lotacoes, many=True)
        
        return Response({
            'total': total,
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def inconsistencias(self, request, pk=None):
        """
        GET /api/carga_org_lot/lotacoes/{id}/inconsistencias/
        
        Lista inconsistências encontradas na lotação.
        """
        versao = self.get_object()
        
        inconsistencias = TblLotacaoInconsistencia.objects.filter(
            id_lotacao__id_lotacao_versao=versao
        ).select_related('id_lotacao').order_by('-dat_registro')
        
        data = inconsistencias.values(
            'id_inconsistencia',
            'str_tipo',
            'str_detalhe',
            'dat_registro',
            'id_lotacao__str_cpf',
            'id_lotacao__id_orgao_lotacao__str_sigla'
        )
        
        return Response({
            'total': inconsistencias.count(),
            'inconsistencias': list(data)
        })
    
    @action(detail=True, methods=['get'])
    def estatisticas(self, request, pk=None):
        """
        GET /api/carga_org_lot/lotacoes/{id}/estatisticas/
        
        Estatísticas da versão de lotação.
        """
        versao = self.get_object()
        
        lotacoes = TblLotacao.objects.filter(id_lotacao_versao=versao)
        
        stats = {
            'total_registros': lotacoes.count(),
            'validos': lotacoes.filter(flg_valido=True).count(),
            'invalidos': lotacoes.filter(flg_valido=False).count(),
            'total_inconsistencias': TblLotacaoInconsistencia.objects.filter(
                id_lotacao__id_lotacao_versao=versao
            ).count(),
            'por_orgao': list(
                lotacoes.values('id_orgao_lotacao__str_sigla')
                .annotate(count=Count('id_lotacao'))
                .order_by('-count')[:10]
            )
        }
        
        return Response(stats)
