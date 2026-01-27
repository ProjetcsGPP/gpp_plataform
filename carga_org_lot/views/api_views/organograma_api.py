"""
API ViewSet para Organograma
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ...models import (
    TblOrganogramaVersao,
    TblOrgaoUnidade,
    TblOrganogramaJson,
)
from ...serializers import (
    TblOrganogramaVersaoSerializer,
    TblOrgaoUnidadeSerializer,
)


class OrganogramaVersaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Versões de Organograma.
    
    list:    GET /api/carga_org_lot/organogramas/
    create:  POST /api/carga_org_lot/organogramas/
    retrieve: GET /api/carga_org_lot/organogramas/{id}/
    """
    queryset = TblOrganogramaVersao.objects.select_related('id_patriarca').all()
    serializer_class = TblOrganogramaVersaoSerializer
    permission_classes = [IsAuthenticated]
    
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
        
        return queryset.order_by('-dat_processamento')
    
    @action(detail=True, methods=['get'])
    def orgaos(self, request, pk=None):
        """
        GET /api/carga_org_lot/organogramas/{id}/orgaos/
        
        Lista órgãos/unidades do organograma (hierarquia completa).
        """
        organograma = self.get_object()
        orgaos = TblOrgaoUnidade.objects.filter(
            id_organograma_versao=organograma
        ).select_related('id_orgao_unidade_pai').order_by('str_numero_hierarquia')
        
        serializer = TblOrgaoUnidadeSerializer(orgaos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def hierarquia(self, request, pk=None):
        """
        GET /api/carga_org_lot/organogramas/{id}/hierarquia/
        
        Retorna estrutura hierárquica em árvore (JSON aninhado).
        """
        organograma = self.get_object()
        
        # Buscar órgãos raiz (sem pai)
        orgaos_raiz = TblOrgaoUnidade.objects.filter(
            id_organograma_versao=organograma,
            id_orgao_unidade_pai__isnull=True
        ).prefetch_related('tblorgaounidade_set')
        
        def build_tree(orgao):
            """Constrói árvore recursivamente"""
            children = TblOrgaoUnidade.objects.filter(id_orgao_unidade_pai=orgao)
            return {
                'id': orgao.id_orgao_unidade,
                'sigla': orgao.str_sigla,
                'nome': orgao.str_nome,
                'nivel': orgao.int_nivel_hierarquia,
                'filhos': [build_tree(child) for child in children]
            }
        
        hierarquia = [build_tree(orgao) for orgao in orgaos_raiz]
        
        return Response({
            'organograma_id': organograma.id_organograma_versao,
            'patriarca': organograma.id_patriarca.str_sigla_patriarca,
            'hierarquia': hierarquia
        })
    
    @action(detail=True, methods=['get'])
    def json_envio(self, request, pk=None):
        """
        GET /api/carga_org_lot/organogramas/{id}/json_envio/
        
        Retorna JSON formatado para envio à API externa.
        """
        organograma = self.get_object()
        
        try:
            json_org = TblOrganogramaJson.objects.get(id_organograma_versao=organograma)
            return Response({
                'conteudo': json_org.js_conteudo,
                'data_criacao': json_org.dat_criacao,
                'data_envio': json_org.dat_envio_api,
                'status_envio': json_org.str_status_envio,
                'mensagem_retorno': json_org.str_mensagem_retorno
            })
        except TblOrganogramaJson.DoesNotExist:
            return Response(
                {'detail': 'JSON de envio não encontrado para este organograma'},
                status=status.HTTP_404_NOT_FOUND
            )
