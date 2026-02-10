"""
Core Views - ViewSets para entidades principais/auxiliares.
Inclui: Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta.
"""

import logging
from django.db import transaction
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ...models import Eixo, SituacaoAcao, VigenciaPNGI, TipoEntraveAlerta
from ...serializers import (
    EixoSerializer, EixoListSerializer,
    SituacaoAcaoSerializer,
    VigenciaPNGISerializer, VigenciaPNGIListSerializer,
    TipoEntraveAlertaSerializer
)

logger = logging.getLogger(__name__)


class EixoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Eixos do PNGI.
    """
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaoeixo', 'stralias']
    ordering_fields = ['stralias', 'strdescricaoeixo', 'created_at']
    ordering = ['stralias']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EixoListSerializer
        return EixoSerializer
    
    @action(detail=False, methods=['get'])
    def list_light(self, request):
        """Endpoint otimizado para listagem rápida"""
        eixos = Eixo.objects.all().values('ideixo', 'strdescricaoeixo', 'stralias')
        return Response({
            'count': len(eixos),
            'results': list(eixos)
        })


class SituacaoAcaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Situações de Ações do PNGI.
    """
    queryset = SituacaoAcao.objects.all()
    serializer_class = SituacaoAcaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaosituacao']
    ordering_fields = ['strdescricaosituacao', 'created_at']
    ordering = ['strdescricaosituacao']


class VigenciaPNGIViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Vigências do PNGI.
    """
    queryset = VigenciaPNGI.objects.all()
    serializer_class = VigenciaPNGISerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaovigenciapngi']
    ordering_fields = ['datiniciovigencia', 'datfinalvigencia', 'created_at']
    ordering = ['-datiniciovigencia']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtro opcional por vigência ativa
        if self.request.query_params.get('isvigenciaativa'):
            queryset = queryset.filter(isvigenciaativa=True)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VigenciaPNGIListSerializer
        return VigenciaPNGISerializer
    
    @action(detail=False, methods=['get'])
    def vigencia_ativa(self, request):
        """Retorna a vigência atualmente ativa"""
        try:
            vigencia = VigenciaPNGI.objects.get(isvigenciaativa=True)
            serializer = self.get_serializer(vigencia)
            return Response(serializer.data)
        except VigenciaPNGI.DoesNotExist:
            return Response(
                {'detail': 'Nenhuma vigência ativa encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def vigente(self, request):
        """Retorna vigências vigentes no momento"""
        vigencias_ativas = [v for v in self.get_queryset() if v.esta_vigente]
        serializer = self.get_serializer(vigencias_ativas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        """Ativa uma vigência específica"""
        try:
            with transaction.atomic():
                # Desativa todas as vigências
                VigenciaPNGI.objects.update(isvigenciaativa=False)
                
                # Ativa a vigência selecionada
                vigencia = self.get_object()
                vigencia.isvigenciaativa = True
                vigencia.save()
                
                serializer = self.get_serializer(vigencia)
                
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
    """
    queryset = TipoEntraveAlerta.objects.all()
    serializer_class = TipoEntraveAlertaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['strdescricaotipoentravealerta']
    ordering_fields = ['strdescricaotipoentravealerta', 'created_at']
    ordering = ['strdescricaotipoentravealerta']
