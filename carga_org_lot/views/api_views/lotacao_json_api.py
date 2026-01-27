"""
API ViewSet para JSON de Lotação por Órgão
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.utils import timezone

from ...models import (
    TblLotacaoJsonOrgao,
    TblLotacao,
    TblOrgaoUnidade,
)
from ...serializers import TblLotacaoJsonOrgaoSerializer


class LotacaoJsonOrgaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar JSON de Lotação por Órgão.
    
    Gerencia os JSONs formatados por órgão para envio à API externa.
    Cada JSON contém as lotações de servidores de um órgão específico.
    
    list:    GET /api/carga_org_lot/lotacao-json-orgao/
    create:  POST /api/carga_org_lot/lotacao-json-orgao/
    retrieve: GET /api/carga_org_lot/lotacao-json-orgao/{id}/
    update:   PUT /api/carga_org_lot/lotacao-json-orgao/{id}/
    partial_update: PATCH /api/carga_org_lot/lotacao-json-orgao/{id}/
    destroy:  DELETE /api/carga_org_lot/lotacao-json-orgao/{id}/
    """
    queryset = TblLotacaoJsonOrgao.objects.select_related(
        'id_lotacao_versao',
        'id_organograma_versao',
        'id_patriarca',
        'id_orgao_lotacao'
    ).all()
    serializer_class = TblLotacaoJsonOrgaoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtros via query params"""
        queryset = super().get_queryset()
        
        # Filtro por versão de lotação
        lotacao_versao_id = self.request.query_params.get('lotacao_versao', None)
        if lotacao_versao_id:
            queryset = queryset.filter(id_lotacao_versao_id=lotacao_versao_id)
        
        # Filtro por patriarca
        patriarca_id = self.request.query_params.get('patriarca', None)
        if patriarca_id:
            queryset = queryset.filter(id_patriarca_id=patriarca_id)
        
        # Filtro por órgão
        orgao_id = self.request.query_params.get('orgao', None)
        if orgao_id:
            queryset = queryset.filter(id_orgao_lotacao_id=orgao_id)
        
        # Filtro por status de envio
        status_envio = self.request.query_params.get('status_envio', None)
        if status_envio:
            queryset = queryset.filter(str_status_envio=status_envio)
        
        # Filtro apenas não enviados
        nao_enviados = self.request.query_params.get('nao_enviados', None)
        if nao_enviados == 'true':
            queryset = queryset.filter(dat_envio_api__isnull=True)
        
        return queryset.order_by('-dat_criacao')
    
    @action(detail=True, methods=['get'])
    def conteudo(self, request, pk=None):
        """
        GET /api/carga_org_lot/lotacao-json-orgao/{id}/conteudo/
        
        Retorna o conteúdo JSON completo formatado.
        """
        json_orgao = self.get_object()
        
        return Response({
            'id': json_orgao.id_lotacao_json_orgao,
            'orgao': {
                'id': json_orgao.id_orgao_lotacao.id_orgao_unidade,
                'sigla': json_orgao.id_orgao_lotacao.str_sigla,
                'nome': json_orgao.id_orgao_lotacao.str_nome
            },
            'patriarca': json_orgao.id_patriarca.str_sigla_patriarca,
            'lotacao_versao_id': json_orgao.id_lotacao_versao_id,
            'organograma_versao_id': json_orgao.id_organograma_versao_id,
            'conteudo': json_orgao.js_conteudo,
            'data_criacao': json_orgao.dat_criacao,
            'data_envio': json_orgao.dat_envio_api,
            'status_envio': json_orgao.str_status_envio,
            'mensagem_retorno': json_orgao.str_mensagem_retorno
        })
    
    @action(detail=True, methods=['post'])
    def regenerar(self, request, pk=None):
        """
        POST /api/carga_org_lot/lotacao-json-orgao/{id}/regenerar/
        
        Regenera o JSON a partir dos dados atuais de lotação do banco.
        """
        json_orgao = self.get_object()
        
        # Buscar lotações válidas do órgão
        lotacoes = TblLotacao.objects.filter(
            id_lotacao_versao=json_orgao.id_lotacao_versao,
            id_orgao_lotacao=json_orgao.id_orgao_lotacao,
            flg_valido=True
        ).select_related(
            'id_orgao_lotacao',
            'id_unidade_lotacao'
        )
        
        # Construir JSON
        servidores = []
        for lotacao in lotacoes:
            servidor = {
                'cpf': lotacao.str_cpf,
                'orgao': {
                    'sigla': lotacao.id_orgao_lotacao.str_sigla,
                    'nome': lotacao.id_orgao_lotacao.str_nome
                },
                'cargo': lotacao.str_cargo_normalizado or lotacao.str_cargo_original,
                'data_referencia': lotacao.dat_referencia.isoformat() if lotacao.dat_referencia else None
            }
            
            if lotacao.id_unidade_lotacao:
                servidor['unidade'] = {
                    'sigla': lotacao.id_unidade_lotacao.str_sigla,
                    'nome': lotacao.id_unidade_lotacao.str_nome
                }
            
            servidores.append(servidor)
        
        novo_conteudo = {
            'orgao': {
                'id': json_orgao.id_orgao_lotacao.id_orgao_unidade,
                'sigla': json_orgao.id_orgao_lotacao.str_sigla,
                'nome': json_orgao.id_orgao_lotacao.str_nome
            },
            'patriarca': json_orgao.id_patriarca.str_sigla_patriarca,
            'total_servidores': len(servidores),
            'servidores': servidores,
            'data_geracao': timezone.now().isoformat()
        }
        
        # Atualizar registro
        json_orgao.js_conteudo = novo_conteudo
        json_orgao.save()
        
        return Response({
            'message': 'JSON regenerado com sucesso',
            'total_servidores': len(servidores)
        })
    
    @action(detail=True, methods=['post'])
    def enviar_api(self, request, pk=None):
        """
        POST /api/carga_org_lot/lotacao-json-orgao/{id}/enviar_api/
        
        Envia o JSON para a API externa.
        
        Body (opcional):
            - force: true/false (força reenvio mesmo se já foi enviado)
        """
        json_orgao = self.get_object()
        force = request.data.get('force', False)
        
        # Verifica se já foi enviado
        if json_orgao.dat_envio_api and not force:
            return Response(
                {
                    'error': 'JSON já foi enviado. Use force=true para reenviar.',
                    'data_envio': json_orgao.dat_envio_api,
                    'status': json_orgao.str_status_envio
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Implementar integração com API externa
        # Por enquanto, simula envio
        
        json_orgao.dat_envio_api = timezone.now()
        json_orgao.str_status_envio = 'PENDENTE'  # Deve ser atualizado após resposta da API
        json_orgao.str_mensagem_retorno = 'Envio em desenvolvimento'
        json_orgao.save()
        
        return Response({
            'message': 'Envio para API em desenvolvimento',
            'data_envio': json_orgao.dat_envio_api
        }, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """
        GET /api/carga_org_lot/lotacao-json-orgao/estatisticas/
        
        Estatísticas gerais dos JSONs de lotação.
        """
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'enviados': queryset.filter(dat_envio_api__isnull=False).count(),
            'nao_enviados': queryset.filter(dat_envio_api__isnull=True).count(),
            'por_status': list(
                queryset.values('str_status_envio')
                .annotate(count=Count('id_lotacao_json_orgao'))
                .order_by('-count')
            ),
            'por_orgao': list(
                queryset.values(
                    'id_orgao_lotacao__str_sigla',
                    'id_orgao_lotacao__str_nome'
                )
                .annotate(count=Count('id_lotacao_json_orgao'))
                .order_by('-count')[:10]
            )
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['post'])
    def gerar_em_lote(self, request):
        """
        POST /api/carga_org_lot/lotacao-json-orgao/gerar_em_lote/
        
        Gera JSONs para todos os órgãos de uma versão de lotação.
        
        Body:
            - lotacao_versao_id: ID da versão de lotação
            - sobrescrever: true/false (sobrescreve JSONs existentes)
        """
        lotacao_versao_id = request.data.get('lotacao_versao_id')
        sobrescrever = request.data.get('sobrescrever', False)
        
        if not lotacao_versao_id:
            return Response(
                {'error': 'lotacao_versao_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Implementar geração em lote
        # 1. Buscar todos os órgãos com lotações na versão
        # 2. Para cada órgão, gerar/atualizar JSON
        # 3. Retornar relatório
        
        return Response({
            'message': 'Geração em lote em desenvolvimento'
        }, status=status.HTTP_501_NOT_IMPLEMENTED)
