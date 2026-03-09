"""
API ViewSet para Patriarca

REFATORADO: Implementa HasModelPermission do AuthorizationService
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.services.authorization_service import HasModelPermission

from ...models import LotacaoVersao, OrganogramaVersao, Patriarca
from ...serializers import (
    LotacaoVersaoSerializer,
    OrganogramaVersaoSerializer,
    PatriarcaSerializer,
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

    ✅ PERMISSÃO: HasModelPermission com patriarca
    """

    queryset = Patriarca.objects.select_related(
        "id_status_progresso", "id_usuario_criacao"
    ).all()
    serializer_class = PatriarcaSerializer
    permission_classes = [HasModelPermission]
    permission_model = "patriarca"

    def get_queryset(self):
        """Permite filtros via query params"""
        queryset = super().get_queryset()

        # Filtro por sigla
        sigla = self.request.query_params.get("sigla", None)
        if sigla:
            queryset = queryset.filter(str_sigla_patriarca__icontains=sigla)

        # Filtro por status
        status_id = self.request.query_params.get("status", None)
        if status_id:
            queryset = queryset.filter(id_status_progresso_id=status_id)

        return queryset

    @action(detail=True, methods=["get"])
    def organogramas(self, request, pk=None):
        """
        GET /api/carga_org_lot/patriarcas/{id}/organogramas/

        Lista organogramas do patriarca.
        """
        patriarca = self.get_object()
        organogramas = OrganogramaVersao.objects.filter(
            id_patriarca=patriarca
        ).order_by("-dat_processamento")

        serializer = OrganogramaVersaoSerializer(organogramas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def lotacoes(self, request, pk=None):
        """
        GET /api/carga_org_lot/patriarcas/{id}/lotacoes/

        Lista versões de lotação do patriarca.
        """
        patriarca = self.get_object()
        lotacoes = LotacaoVersao.objects.filter(id_patriarca=patriarca).order_by(
            "-dat_processamento"
        )

        serializer = LotacaoVersaoSerializer(lotacoes, many=True)
        return Response(serializer.data)
