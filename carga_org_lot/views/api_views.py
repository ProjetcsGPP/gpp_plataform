# carga_org_lot/views/api_views.py
"""
API Views para Carga Org/Lot.
Endpoints RESTful para gerenciar cargas de organogramas e lotações.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Prefetch

from ..models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblOrgaoUnidade,
    TblOrganogramaJson,
    TblLotacaoVersao,
    TblLotacao,
    TblLotacaoJsonOrgao,
    TblLotacaoInconsistencia,
    TblTokenEnvioCarga,
    TblCargaPatriarca,
    TblDetalheStatusCarga,
    TblStatusProgresso,
    TblStatusTokenEnvioCarga,
    TblStatusCarga,
    TblTipoCarga,
)
from ..serializers import (
    TblPatriarcaSerializer,
    TblOrganogramaVersaoSerializer,
    TblOrgaoUnidadeSerializer,
    TblLotacaoVersaoSerializer,
    TblLotacaoSerializer,
    TblTokenEnvioCargaSerializer,
    TblCargaPatriarcaSerializer,
)
from accounts.models import UserRole


# ============================================
# VIEWS DE ESTATÍSTICAS E DASHBOARD
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    GET /api/carga_org_lot/dashboard/
    
    Retorna estatísticas gerais do sistema de carga.
    """
    app_code = request.app_context.get('code', 'CARGA_ORG_LOT')
    
    # Verifica acesso
    has_access = UserRole.objects.filter(
        user=request.user,
        aplicacao__codigointerno=app_code
    ).exists()
    
    if not has_access:
        return Response(
            {'detail': 'Acesso negado'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Estatísticas gerais
    stats = {
        'patriarcas': {
            'total': TblPatriarca.objects.count(),
            'por_status': list(
                TblPatriarca.objects.values('id_status_progresso__str_descricao')
                .annotate(count=Count('id_patriarca'))
            )
        },
        'organogramas': {
            'total': TblOrganogramaVersao.objects.count(),
            'ativos': TblOrganogramaVersao.objects.filter(flg_ativo=True).count(),
            'processados': TblOrganogramaVersao.objects.filter(
                str_status_processamento='PROCESSADO'
            ).count(),
        },
        'lotacoes': {
            'total': TblLotacao.objects.count(),
            'validas': TblLotacao.objects.filter(flg_valido=True).count(),
            'invalidas': TblLotacao.objects.filter(flg_valido=False).count(),
        },
        'cargas': {
            'total': TblCargaPatriarca.objects.count(),
            'por_status': list(
                TblCargaPatriarca.objects.values('id_status_carga__str_descricao')
                .annotate(count=Count('id_carga_patriarca'))
            ),
            'por_tipo': list(
                TblCargaPatriarca.objects.values('id_tipo_carga__str_descricao')
                .annotate(count=Count('id_carga_patriarca'))
            )
        }
    }
    
    return Response(stats)


# ============================================
# VIEWSET: PATRIARCAS
# ============================================

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


# ============================================
# VIEWSET: ORGANOGRAMAS
# ============================================

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


# ============================================
# VIEWSET: LOTAÇÕES
# ============================================

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


# ============================================
# VIEWSET: CARGAS
# ============================================

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


# ============================================
# ENDPOINTS DE UPLOAD
# ============================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_organograma(request):
    """
    POST /api/carga_org_lot/upload/organograma/
    
    Faz upload de arquivo de organograma (Excel/CSV).
    
    Body (multipart/form-data):
        - file: arquivo
        - patriarca_id: ID do patriarca
    """
    # TODO: Implementar lógica de upload e processamento
    
    return Response({
        'message': 'Upload de organograma em desenvolvimento'
    }, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_lotacao(request):
    """
    POST /api/carga_org_lot/upload/lotacao/
    
    Faz upload de arquivo de lotação (Excel/CSV).
    
    Body (multipart/form-data):
        - file: arquivo
        - patriarca_id: ID do patriarca
        - organograma_versao_id: ID da versão do organograma
    """
    # TODO: Implementar lógica de upload e processamento
    
    return Response({
        'message': 'Upload de lotação em desenvolvimento'
    }, status=status.HTTP_501_NOT_IMPLEMENTED)


# ============================================
# ENDPOINTS DE CONSULTA RÁPIDA
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_orgao(request):
    """
    GET /api/carga_org_lot/search/orgao/?q=termo&patriarca_id=1
    
    Busca órgãos por sigla ou nome.
    """
    query = request.query_params.get('q', '')
    patriarca_id = request.query_params.get('patriarca_id', None)
    
    if len(query) < 2:
        return Response({'results': []})
    
    orgaos = TblOrgaoUnidade.objects.filter(
        Q(str_sigla__icontains=query) | Q(str_nome__icontains=query),
        flg_ativo=True
    )
    
    if patriarca_id:
        orgaos = orgaos.filter(id_patriarca_id=patriarca_id)
    
    orgaos = orgaos.select_related('id_patriarca')[:20]
    
    results = [
        {
            'id': o.id_orgao_unidade,
            'sigla': o.str_sigla,
            'nome': o.str_nome,
            'patriarca': o.id_patriarca.str_sigla_patriarca,
            'nivel': o.int_nivel_hierarquia
        }
        for o in orgaos
    ]
    
    return Response({'results': results})
