"""
API Views do Ações PNGI.
Usa AppContextMiddleware para detecção automática da aplicação.
"""

import logging
from datetime import timedelta
from time import timezone

from django.apps import apps
from django.db.models import Count, Prefetch, Q
from django.forms import ValidationError
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import User, UserRole
from accounts.services.authorization_service import (
    HasModelPermission,
    ReadOnlyOrHasPermission,
    get_authorization_service,
)
from common.serializers import (
    PortalAuthSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from common.services.portal_auth import get_portal_auth_service

from ..models import (
    AcaoAnotacaoAlinhamento,
    AcaoDestaque,
    AcaoPrazo,
    Acoes,
    Eixo,
    RelacaoAcaoUsuarioResponsavel,
    SituacaoAcao,
    TipoAnotacaoAlinhamento,
    TipoEntraveAlerta,
    UsuarioResponsavel,
    VigenciaPNGI,
)
from ..permissions import (
    IsAnyPNGIRole,
    IsCoordernadorGestorOrOperadorPNGI,
    IsCoordernadorOrGestorPNGI,
    IsGestorPNGI,
    IsGestorPNGIOnly,
)
from ..serializers import (
    AcaoAnotacaoAlinhamentoSerializer,
    AcaoDestaqueSerializer,
    AcaoPrazoSerializer,
    AcoesCompletasSerializer,
    AcoesSerializer,
    EixoSerializer,
    RelacaoAcaoUsuarioResponsavelSerializer,
    SituacaoAcaoSerializer,
    TipoAnotacaoAlinhamentoSerializer,
    TipoEntraveAlertaSerializer,
    UsuarioResponsavelCompletoSerializer,
    UsuarioResponsavelSerializer,
    VigenciaPNGISerializer,
)

logger = logging.getLogger(__name__)


def get_app_code(request):
    """
    Helper para obter APP_CODE do request ou da config da app.

    Prioridade:
    1. request.app_context['code'] (do middleware)
    2. request.app_code (fallback antigo)
    3. app config
    """
    # Tenta pegar do middleware (novo)
    if hasattr(request, "app_context") and request.app_context.get("code"):
        return request.app_context["code"]

    # Fallback: request.app_code (antigo)
    if hasattr(request, "app_code") and request.app_code:
        return request.app_code

    # Fallback final: pega da configuração da app
    app_config = apps.get_app_config("acoes_pngi")
    return app_config.app_code


# ============================================================================
# ENDPOINTS DE AUTENTICAÇÃO
# ============================================================================


@api_view(["POST"])
@permission_classes([AllowAny])
def portal_auth(request):
    """
    Autenticação via token do portal.

    ✨ Usa request.app_context do middleware para detectar aplicação.

    POST /api/v1/acoes_pngi/auth/portal/
    Body: {"token": "jwt_token"}
    """
    # Valida input
    input_serializer = PortalAuthSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    token = input_serializer.validated_data["token"]

    try:
        # ✨ Pega app_code do contexto (adicionado pelo middleware)
        app_code = request.app_context.get("code")
        app_name = request.app_context.get("name")

        if not app_code:
            return Response(
                {"detail": "Aplicação não identificada"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Autentica via portal service
        portal_service = get_portal_auth_service(app_code)
        user = portal_service.authenticate_user(token)

        if not user:
            return Response(
                {"detail": "Token inválido ou expirado"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # ✨ Serializa usuário (pega app_code automaticamente do request.app_context)
        user_serializer = UserSerializer(user, context={"request": request})

        # Gera token local (opcional)
        from rest_framework.authtoken.models import Token

        local_token, _ = Token.objects.get_or_create(user=user)

        logger.info(f"[{app_code}] Usuário autenticado via portal: {user.email}")

        return Response(
            {
                "user": user_serializer.data,
                "local_token": local_token.key,
                "app": {"code": app_code, "name": app_name},
                "message": f"Autenticado com sucesso em {app_name}",
            }
        )

    except Exception as e:
        logger.error(f"Erro na autenticação via portal: {str(e)}")
        return Response(
            {"detail": f"Erro na autenticação: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    """
    Retorna permissões do usuário logado para consumo no Next.js.
    ✨ Usa helpers com cache para otimização de performance.

    GET /api/v1/acoes_pngi/permissions/
    """
    try:
        # ✨ Usa helper com cache (15 minutos)
        auth = get_authorization_service()
        perms = auth.get_user_permissions(request.user.id, "ACOES_PNGI")

        # Buscar role do usuário
        user_role = (
            UserRole.objects.filter(
                user=request.user, aplicacao__codigointerno="ACOES_PNGI"
            )
            .select_related("role")
            .first()
        )

        role = user_role.role.codigoperfil if user_role else None

        # ✨ Usa helper para permissões por modelo (também com cache)
        auth = get_authorization_service()
        specific = {
            "eixo": auth.get_user_permissions(request.user.id, "ACOES_PNGI"),
            "situacaoacao": auth.get_user_permissions(request.user.id, "ACOES_PNGI"),
            "vigenciapngi": auth.get_user_permissions(request.user.id, "ACOES_PNGI"),
        }

        return Response(
            {
                "user_id": request.user.id,
                "email": request.user.email,
                "name": request.user.name,
                "role": role,
                "permissions": list(perms),
                "is_superuser": request.user.is_superuser,
                "groups": {
                    "can_manage_config": any(
                        p in perms
                        for p in [
                            "add_eixo",
                            "change_eixo",
                            "add_situacaoacao",
                            "change_situacaoacao",
                            "add_vigenciapngi",
                            "change_vigenciapngi",
                        ]
                    ),
                    "can_manage_acoes": False,  # Futuramente com model Acao
                    "can_delete": any(p.startswith("delete_") for p in perms),
                },
                "specific": specific,
            }
        )

    except Exception as e:
        logger.error(f"Erro ao buscar permissões do usuário: {str(e)}")
        return Response(
            {"detail": f"Erro ao buscar permissões: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ============================================================================
# VIEWSET DE GERENCIAMENTO DE USUÁRIOS
# ============================================================================


class UserManagementViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de usuários da aplicação.

    ✨ Usa request.app_context automaticamente.

    Permissões:
    - TODAS as operações (GET/POST/PATCH): Apenas GESTOR_PNGI
    - Demais roles (COORDENADOR, OPERADOR, CONSULTOR) são bloqueadas
    """

    permission_classes = [IsGestorPNGIOnly]  # ✅ CORRIGIDO: GESTOR para tudo

    lookup_field = "pk"
    lookup_value_regex = ".*"

    def retrieve(self, request, pk=None):
        """GET /api/v1/acoes_pngi/users/{email}/"""
        return self.get_user_by_email(request, pk)

    @action(detail=False, methods=["post"])
    def sync_user(self, request):
        """Sincroniza usuário do portal com roles e atributos."""
        try:
            serializer = UserCreateSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)

            user = serializer.save()
            created = serializer.validated_data.get("_created", False)

            user_serializer = UserSerializer(user, context={"request": request})

            return Response(
                {
                    "user": user_serializer.data,
                    "created": created,
                    "message": f"Usuário {'criado' if created else 'atualizado'} com sucesso",
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Erro ao sincronizar usuário: {str(e)}")
            return Response(
                {"detail": f"Erro ao sincronizar usuário: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def list_users(self, request):
        """Lista usuários com acesso à aplicação atual."""
        try:
            app_code = get_app_code(request)

            if not app_code:
                return Response(
                    {"detail": "Aplicação não identificada"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            user_ids = UserRole.objects.filter(
                aplicacao__codigointerno=app_code
            ).values_list("user_id", flat=True)

            users = User.objects.filter(id__in=user_ids, is_active=True)

            serializer = UserListSerializer(users, many=True)

            return Response({"count": users.count(), "users": serializer.data})

        except Exception as e:
            logger.error(f"Erro ao listar usuários: {str(e)}")
            return Response(
                {"detail": f"Erro ao listar usuários: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"])
    def get_user_by_email(self, request, pk=None):
        """Busca usuário por email."""
        try:
            user = User.objects.get(email=pk)
            serializer = UserSerializer(user, context={"request": request})
            return Response(serializer.data)

        except User.DoesNotExist:
            return Response(
                {"detail": f"Usuário com email {pk} não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=True, methods=["patch"])
    def update_user_status(self, request, pk=None):
        """Atualiza status de usuário."""
        try:
            user = User.objects.get(email=pk)

            serializer = UserUpdateSerializer(
                user, data=request.data, partial=True, context={"request": request}
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            user_serializer = UserSerializer(user, context={"request": request})

            return Response(
                {
                    "detail": "Usuário atualizado com sucesso",
                    "user": user_serializer.data,
                }
            )

        except User.DoesNotExist:
            return Response(
                {"detail": f"Usuário com email {pk} não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )


# ============================================================================
# VIEWSETS DE ENTIDADES CORE
# ============================================================================


class EixoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Eixo (com AuthorizationService).

    Matriz de Permissões (VALIDADA):
    - GESTOR: R/W/D ✓ (add_eixo, change_eixo, delete_eixo)
    - COORDENADOR: R/W/D ✓ (add_eixo, change_eixo, delete_eixo)
    - OPERADOR: R ✓ (view_eixo)
    - CONSULTOR: R ✓ (view_eixo)

    🔑 AuthorizationService + Cache 5min + RolePermission Django
    """

    queryset = Eixo.objects.all().order_by("stralias")
    serializer_class = EixoSerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "eixo"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Nova classe híbrida

    def get_permissions(self):
        """
        Granular por ação (mantém lógica atual):
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole)
        - Escrita: Coord/Gestor (AuthorizationService verifica RolePermission)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # Nível 2: GESTOR e COORDENADOR (usa classes existentes + AuthorizationService)
            self.permission_classes = [IsCoordernadorOrGestorPNGI, HasModelPermission]
        else:
            # Leitura: Todas as roles PNGI
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros melhorados."""
        queryset = super().get_queryset()

        # Filtro por alias (ex: /api/eixos/?alias=SAU)
        alias = self.request.query_params.get("alias")
        if alias:
            queryset = queryset.filter(stralias__icontains=alias.upper())

        return queryset

    def create(self, request, *args, **kwargs):
        """Criar Eixo (apenas Coord/Gestor)."""
        logger.info(
            f"[{request.method}] Criando Eixo '{request.data.get('stralias')}': "
            f"user={request.user.id}, role={getattr(request, 'token_payload', {}).get('role_code')}"
        )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Deletar Eixo (apenas Coord/Gestor)."""
        instance = self.get_object()
        logger.warning(
            f"[{request.method}] Deletando Eixo '{instance.stralias}': "
            f"user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def acoes(self, request, pk=None):
        """
        🆕 GET /api/eixos/{id}/acoes/

        Lista ações associadas ao eixo (qualquer role PNGI pode ver).
        """
        eixo = self.get_object()
        acoes_count = eixo.acoes.count()

        from acoes_pngi.serializers import AcoesSerializer

        serializer = AcoesSerializer(eixo.acoes.all(), many=True)

        return Response(
            {
                "eixo": {
                    "id": eixo.ideixo,
                    "alias": eixo.stralias,
                    "descricao": eixo.strdescricaoeixo,
                    "acoes_count": acoes_count,
                },
                "acoes": serializer.data,
            }
        )

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/eixos/stats/

        Estatísticas dos eixos (qualquer role PNGI).
        """
        from django.db.models import Count

        stats = Eixo.objects.aggregate(
            total=Count("id"),
            com_acoes=Count("acoes", filter=Q(acoes__isnull=False), distinct=True),
        )

        return Response(
            {
                "total_eixos": stats["total"],
                "com_acoes": stats["com_acoes"],
                "sem_acoes": stats["total"] - stats["com_acoes"],
            }
        )


class SituacaoAcaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para SituacaoAcao (Nível 1 - Configurações Críticas).

    Matriz de Permissões (VALIDADA):
    - GESTOR:    R/W/D ✓ (add_situacaoacao, change_situacaoacao, delete_situacaoacao)
    - COORDENADOR: R ✓ (view_situacaoacao)
    - OPERADOR:   R ✓ (view_situacaoacao)
    - CONSULTOR:  R ✓ (view_situacaoacao)

    🔑 AuthorizationService + Classes existentes + Cache 5min
    """

    queryset = SituacaoAcao.objects.all().order_by("strdescricaosituacao")
    serializer_class = SituacaoAcaoSerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "situacaoacao"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Classe híbrida

    def get_permissions(self):
        """
        Nível 1 - CONFIGURAÇÕES CRÍTICAS:
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole ✅)
        - Escrita: APENAS GESTOR (IsGestorPNGI ✅ + AuthorizationService)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # 🚨 ESCRITA: APENAS GESTOR_PNGI (matriz original)
            self.permission_classes = [IsGestorPNGI, HasModelPermission]
        else:
            # Leitura: Todas as 4 roles PNGI
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros melhorados."""
        queryset = super().get_queryset()

        # Filtro por descrição (ex: /api/situacoes/?search=concluida)
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(strdescricaosituacao__icontains=search)

        return queryset

    def create(self, request, *args, **kwargs):
        """Criar Situação (🚨 APENAS GESTOR)."""
        new_situacao = request.data.get("strdescricaosituacao", "").upper()
        logger.info(
            f"[POST] Criando SituacaoAcao '{new_situacao}': "
            f"user={request.user.id}, role={getattr(request, 'token_payload', {}).get('role_code')}"
        )
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            logger.info(
                f"✅ SituacaoAcao '{new_situacao}' criada por GESTOR {request.user.id}"
            )
        return response

    def destroy(self, request, *args, **kwargs):
        """Deletar Situação (🚨 APENAS GESTOR)."""
        instance = self.get_object()
        logger.warning(
            f"[DELETE] Deletando SituacaoAcao '{instance.strdescricaosituacao}': "
            f"user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/situacoes/stats/

        Estatísticas das situações (qualquer role PNGI pode ver).
        """
        from django.db.models import Count

        from acoes_pngi.models import Acoes

        stats = (
            SituacaoAcao.objects.annotate(acoes_count=Count("acoes"))
            .values("strdescricaosituacao", "acoes_count")
            .order_by("-acoes_count")
        )

        total_acoes = Acoes.objects.count()

        return Response(
            {
                "total_situacoes": SituacaoAcao.objects.count(),
                "total_acoes": total_acoes,
                "situacoes": list(stats),
            }
        )

    @action(detail=True, methods=["get"])
    def acoes(self, request, pk=None):
        """
        🆕 GET /api/situacoes/{id}/acoes/

        Lista ações na situação específica.
        """
        situacao = self.get_object()

        from acoes_pngi.serializers import AcoesSerializer

        serializer = AcoesSerializer(situacao.acoes.all(), many=True)

        return Response(
            {
                "situacao": {
                    "id": situacao.idsituacaoacao,
                    "descricao": situacao.strdescricaosituacao,
                },
                "acoes_count": situacao.acoes.count(),
                "acoes": serializer.data[:10],  # Top 10 ações
            }
        )


class VigenciaPNGIViewSet(viewsets.ModelViewSet):
    """
    ViewSet para VigenciaPNGI (Nível 2 - Configurações Compartilhadas).

    Matriz de Permissões (VALIDADA):
    - GESTOR:        R/W/D ✓ (add_vigenciapngi, change_vigenciapngi, delete_vigenciapngi)
    - COORDENADOR:   R/W/D ✓ (add_vigenciapngi, change_vigenciapngi, delete_vigenciapngi)
    - OPERADOR:      R ✓ (view_vigenciapngi)
    - CONSULTOR:     R ✓ (view_vigenciapngi)

    🔑 AuthorizationService + Cache 5min + RolePermission Django
    """

    queryset = VigenciaPNGI.objects.all().order_by("-datiniciovigencia")
    serializer_class = VigenciaPNGISerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "vigenciapngi"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Classe híbrida

    def get_permissions(self):
        """
        Nível 2 - CONFIGURAÇÕES COMPARTILHADAS:
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole ✅)
        - Escrita: GESTOR + COORDENADOR (IsCoordernadorOrGestorPNGI ✅ + AuthorizationService)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # ✍️ ESCRITA: GESTOR e COORDENADOR (mesma lógica da matriz)
            self.permission_classes = [IsCoordernadorOrGestorPNGI, HasModelPermission]
        else:
            # 👁️ Leitura: Todas as 4 roles PNGI
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros avançados para vigências."""
        queryset = super().get_queryset()

        # Filtro por vigência ativa
        ativa = self.request.query_params.get("ativa")
        if ativa == "true":
            queryset = queryset.filter(isvigenciaativa=True)
        elif ativa == "false":
            queryset = queryset.filter(isvigenciaativa=False)

        # Filtro por período
        data_inicio = self.request.query_params.get("data_inicio")
        data_fim = self.request.query_params.get("data_fim")
        if data_inicio:
            queryset = queryset.filter(datiniciovigencia__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(datfinalvigencia__lte=data_fim)

        # Busca por descrição
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(strdescricaovigenciapngi__icontains=search)

        return queryset

    def create(self, request, *args, **kwargs):
        """Criar Vigência (GESTOR/COORDENADOR)."""
        data = request.data.copy()
        descricao = data.get("strdescricaovigenciapngi", "Sem nome")

        logger.info(
            f"[POST] Criando VigenciaPNGI '{descricao}': "
            f"início={data.get('datiniciovigencia')}, "
            f"fim={data.get('datfinalvigencia')}, "
            f"user={request.user.id}"
        )
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            logger.info(f"✅ VigenciaPNGI '{descricao}' criada")
        return response

    def update(self, request, *args, **kwargs):
        """Atualizar Vigência (GESTOR/COORDENADOR)."""
        instance = self.get_object()
        old_desc = instance.strdescricaovigenciapngi

        logger.info(
            f"[PUT/PATCH] Atualizando VigenciaPNGI '{old_desc}' → '{request.data.get('strdescricaovigenciapngi')}': "
            f"user={request.user.id}"
        )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Deletar Vigência (🚨 CUIDADO - GESTOR/COORDENADOR)."""
        instance = self.get_object()
        logger.warning(
            f"[DELETE] Deletando VigenciaPNGI '{instance.strdescricaovigenciapngi}' "
            f"({instance.datiniciovigencia} a {instance.datfinalvigencia}): "
            f"user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def ativa(self, request):
        """
        🆕 GET /api/vigencias/ativa/

        Retorna a vigência atualmente ativa (qualquer role PNGI).
        """
        hoje = timezone.now().date()
        vigencia_ativa = (
            self.get_queryset()
            .filter(
                isvigenciaativa=True,
                datiniciovigencia__lte=hoje,
                datfinalvigencia__gte=hoje,
            )
            .first()
        )

        if not vigencia_ativa:
            return Response(
                {"detail": "Nenhuma vigência ativa encontrada"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(vigencia_ativa)
        return Response(
            {
                "vigencia_atual": serializer.data,
                "esta_vigente": vigencia_ativa.esta_vigente,
                "dias_restantes": (
                    (vigencia_ativa.datfinalvigencia - hoje).days
                    if vigencia_ativa.esta_vigente
                    else 0
                ),
            }
        )

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/vigencias/stats/

        Estatísticas das vigências.
        """
        from django.db.models import Count

        stats = (
            self.get_queryset()
            .annotate(acoes_count=Count("acoes"))
            .values(
                "strdescricaovigenciapngi",
                "datiniciovigencia",
                "datfinalvigencia",
                "acoes_count",
            )
            .order_by("-datiniciovigencia")
        )

        return Response(
            {
                "total_vigencias": self.get_queryset().count(),
                "vigencias_ativas": self.get_queryset()
                .filter(isvigenciaativa=True)
                .count(),
                "vigencias": list(stats),
            }
        )

    @action(detail=True, methods=["get"])
    def acoes(self, request, pk=None):
        """
        🆕 GET /api/vigencias/{id}/acoes/

        Ações associadas à vigência específica.
        """
        vigencia = self.get_object()

        from acoes_pngi.serializers import AcoesSerializer

        serializer = AcoesSerializer(vigencia.acoes.all(), many=True)

        return Response(
            {
                "vigencia": {
                    "id": vigencia.idvigenciapngi,
                    "descricao": vigencia.strdescricaovigenciapngi,
                    "periodo": f"{vigencia.datiniciovigencia} a {vigencia.datfinalvigencia}",
                    "ativa": vigencia.isvigenciaativa,
                },
                "acoes_count": vigencia.acoes.count(),
                "acoes": serializer.data[:20],  # Top 20 ações
            }
        )


class TipoEntraveAlertaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para TipoEntraveAlerta (Nível 1 - Configurações Críticas).

    Matriz de Permissões (VALIDADA):
    - GESTOR:        R/W/D ✓ (add_tipoentravealerta, change_tipoentravealerta, delete_tipoentravealerta)
    - COORDENADOR:   R ✓ (view_tipoentravealerta)
    - OPERADOR:      R ✓ (view_tipoentravealerta)
    - CONSULTOR:     R ✓ (view_tipoentravealerta)

    🔑 AuthorizationService + IsGestorPNGI + Cache 5min
    """

    queryset = TipoEntraveAlerta.objects.all().order_by("strdescricaotipoentravealerta")
    serializer_class = TipoEntraveAlertaSerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "tipoentravealerta"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Classe híbrida

    def get_permissions(self):
        """
        🚨 Nível 1 - CONFIGURAÇÕES CRÍTICAS:
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole ✅)
        - Escrita: APENAS GESTOR_PNGI (IsGestorPNGI ✅ + AuthorizationService)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # 🚨 ESCRITA: APENAS GESTOR_PNGI (matriz original)
            self.permission_classes = [IsGestorPNGI, HasModelPermission]
        else:
            # Leitura: Todas as 4 roles PNGI
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros específicos para tipos de entrave."""
        queryset = super().get_queryset()

        # Filtro por descrição (ex: /api/tipos-entrave/?search=atraso)
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(strdescricaotipoentravealerta__icontains=search)

        return queryset

    def create(self, request, *args, **kwargs):
        """Criar Tipo de Entrave (🚨 APENAS GESTOR)."""
        new_tipo = request.data.get("strdescricaotipoentravealerta", "").upper()
        logger.info(
            f"[POST] Criando TipoEntraveAlerta '{new_tipo}': "
            f"user={request.user.id}, role={getattr(request, 'token_payload', {}).get('role_code')}"
        )
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            logger.info(
                f"✅ TipoEntraveAlerta '{new_tipo}' criado por GESTOR {request.user.id}"
            )
        return response

    def destroy(self, request, *args, **kwargs):
        """Deletar Tipo de Entrave (🚨 APENAS GESTOR)."""
        instance = self.get_object()
        logger.warning(
            f"[DELETE] Deletando TipoEntraveAlerta '{instance.strdescricaotipoentravealerta}': "
            f"user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/tipos-entrave/stats/

        Estatísticas dos tipos de entrave (qualquer role PNGI).
        """
        from django.db.models import Count

        from acoes_pngi.models import Acoes

        stats = (
            TipoEntraveAlerta.objects.annotate(acoes_count=Count("acoes"))
            .values("strdescricaotipoentravealerta", "acoes_count")
            .order_by("-acoes_count")
        )

        total_acoes_com_entrave = Acoes.objects.filter(
            idtipoentravealerta__isnull=False
        ).count()

        return Response(
            {
                "total_tipos": TipoEntraveAlerta.objects.count(),
                "acoes_com_entrave": total_acoes_com_entrave,
                "tipos": list(stats),
            }
        )

    @action(detail=True, methods=["get"])
    def acoes(self, request, pk=None):
        """
        🆕 GET /api/tipos-entrave/{id}/acoes/

        Ações com este tipo de entrave.
        """
        tipo_entrave = self.get_object()

        from acoes_pngi.serializers import AcoesSerializer

        serializer = AcoesSerializer(tipo_entrave.acoes.all(), many=True)

        return Response(
            {
                "tipo_entrave": {
                    "id": tipo_entrave.idtipoentravealerta,
                    "descricao": tipo_entrave.strdescricaotipoentravealerta,
                },
                "acoes_count": tipo_entrave.acoes.count(),
                "acoes": serializer.data[:15],  # Top 15 ações com entrave
            }
        )

    @action(detail=False, methods=["get"])
    def mais_criticidade(self, request):
        """
        🆕 GET /api/tipos-entrave/mais_criticidade/

        Top 3 tipos de entrave com mais ações associadas.
        """
        from django.db.models import Count

        top_tipos = TipoEntraveAlerta.objects.annotate(
            acoes_count=Count("acoes")
        ).order_by("-acoes_count")[:3]

        from acoes_pngi.serializers import TipoEntraveAlertaSerializer

        serializer = TipoEntraveAlertaSerializer(top_tipos, many=True)

        return Response(
            {
                "mais_criticos": serializer.data,
                "total_acoes_criticas": sum(
                    [t["acoes_count"] for t in top_tipos.values("acoes_count")]
                ),
            }
        )


# ============================================================================
# VIEWSETS DE AÇÕES
# ============================================================================


class AcoesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Acoes (OPERAÇÕES - Principal da aplicação).

    Matriz de Permissões (VALIDADA):
    - GESTOR:        R/W/D ✓ (add_acoes, change_acoes, delete_acoes)
    - COORDENADOR:   R/W/D ✓ (add_acoes, change_acoes, delete_acoes)
    - OPERADOR:      R/W/D ✓ (add_acoes, change_acoes, delete_acoes)
    - CONSULTOR:     R ✓ (view_acoes)

    🔑 AuthorizationService + Cache 5min + RolePermission Django
    """

    queryset = Acoes.objects.select_related(
        "ideixo", "idsituacaoacao", "idvigenciapngi", "idtipoentravealerta"
    ).prefetch_related("prazos", "destaques", "anotacoes_alinhamento", "responsaveis")
    serializer_class = AcoesSerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "acoes"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Classe híbrida

    def get_permissions(self):
        """
        OPERAÇÕES (GESTOR/COORD/OPERADOR têm escrita):
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole ✅)
        - Escrita: GESTOR/COORD/OPERADOR (IsCoordernadorGestorOrOperadorPNGI ✅ + AuthorizationService)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # ✍️ ESCRITA: 3 roles têm permissão (matriz OPERAÇÕES)
            self.permission_classes = [
                IsCoordernadorGestorOrOperadorPNGI,
                HasModelPermission,
            ]
        else:
            # 👁️ Leitura: Todas as 4 roles PNGI (CONSULTOR incluso)
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros avançados para ações."""
        queryset = super().get_queryset()

        # Filtro por eixo
        eixo_id = self.request.query_params.get("eixo")
        if eixo_id:
            queryset = queryset.filter(ideixo_id=eixo_id)

        # Filtro por situação
        situacao_id = self.request.query_params.get("situacao")
        if situacao_id:
            queryset = queryset.filter(idsituacaoacao_id=situacao_id)

        # Filtro por vigência ativa
        vigencia_id = self.request.query_params.get("vigencia")
        if vigencia_id:
            queryset = queryset.filter(idvigenciapngi_id=vigencia_id)

        # Filtro por entrave
        entrave_id = self.request.query_params.get("entrave")
        if entrave_id:
            queryset = queryset.filter(idtipoentravealerta_id=entrave_id)

        # Busca full-text
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(strapelido__icontains=search) | Q(strdescricaoacao__icontains=search)
            )

        # Ordenação customizada
        order = self.request.query_params.get("order", "strapelido")
        if order in ["strapelido", "-strapelido", "created_at", "-created_at"]:
            queryset = queryset.order_by(order)

        return queryset

    def create(self, request, *args, **kwargs):
        """Criar Ação (GESTOR/COORD/OPERADOR)."""
        apelido = request.data.get("strapelido", "Sem apelido")
        logger.info(
            f"[POST] Criando Ação '{apelido}': "
            f"user={request.user.id}, role={getattr(request, 'token_payload', {}).get('role_code')}"
        )
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            logger.info(f"✅ Ação '{apelido}' criada com sucesso")
        return response

    def update(self, request, *args, **kwargs):
        """Atualizar Ação (GESTOR/COORD/OPERADOR)."""
        instance = self.get_object()
        old_apelido = instance.strapelido
        logger.info(
            f"[PUT/PATCH] Atualizando Ação '{old_apelido}' → '{request.data.get('strapelido')}': "
            f"user={request.user.id}"
        )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Deletar Ação (GESTOR/COORD/OPERADOR)."""
        instance = self.get_object()
        logger.warning(
            f"[DELETE] Deletando Ação '{instance.strapelido}': "
            f"user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def historico(self, request, pk=None):
        """
        🆕 GET /api/acoes/{id}/historico/

        Histórico completo da ação (qualquer role PNGI).
        """
        acao = self.get_object()

        return Response(
            {
                "acao": AcoesSerializer(acao).data,
                "prazos": AcaoPrazoSerializer(acao.prazos.all(), many=True).data,
                "destaques": AcaoDestaqueSerializer(
                    acao.destaques.all(), many=True
                ).data,
                "anotacoes": AcaoAnotacaoAlinhamentoSerializer(
                    acao.anotacoes_alinhamento.all(), many=True
                ).data,
                "responsaveis": UsuarioResponsavelSerializer(
                    acao.responsaveis.all(), many=True
                ).data,
            }
        )

    @action(detail=True, methods=["post"])
    def toggle_ativo(self, request, pk=None):
        """
        🆕 POST /api/acoes/{id}/toggle_ativo/

        Alterna prazo ativo (GESTOR/COORD/OPERADOR).
        Body: {} (vazio)
        """
        acao = self.get_object()

        # Lógica para alternar prazo ativo (exemplo)
        prazos = acao.prazos.filter(isacaoprazoativo=True)
        if prazos.exists():
            prazos.update(isacaoprazoativo=False)
            logger.info(f"Prazos desativados para ação {acao.id}")

        return Response({"detail": "Prazo alternado com sucesso", "acao_id": acao.id})

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/acoes/stats/

        Dashboard de estatísticas (qualquer role PNGI).
        """
        from django.db.models import Count

        timezone.now().date()

        stats = {
            "total_acoes": Acoes.objects.count(),
            "com_entrave": Acoes.objects.filter(
                idtipoentravealerta__isnull=False
            ).count(),
            "sem_responsavel": Acoes.objects.filter(responsaveis__isnull=True).count(),
            "por_situacao": dict(
                Acoes.objects.values("idsituacaoacao__strdescricaosituacao")
                .annotate(count=Count("id"))
                .order_by("-count")[:5]
            ),
            "por_eixo": dict(
                Acoes.objects.values("ideixo__stralias")
                .annotate(count=Count("id"))
                .order_by("-count")[:5]
            ),
        }

        return Response(stats)

    @action(detail=False, methods=["get"])
    def atrasadas(self, request):
        """
        🆕 GET /api/acoes/atrasadas/

        Ações atrasadas (com entrave) - qualquer role PNGI.
        """
        atrasadas = Acoes.objects.filter(
            idtipoentravealerta__isnull=False
        ).select_related("idtipoentravealerta", "idsituacaoacao")[:20]

        serializer = self.get_serializer(atrasadas, many=True)
        return Response(
            {
                "atrasadas_count": Acoes.objects.filter(
                    idtipoentravealerta__isnull=False
                ).count(),
                "acoes": serializer.data,
            }
        )


class AcaoPrazoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para AcaoPrazo (OPERAÇÕES).

    Matriz de Permissões (VALIDADA):
    - GESTOR:        R/W/D ✓ (add_acaoprazo, change_acaoprazo, delete_acaoprazo)
    - COORDENADOR:   R/W/D ✓ (add_acaoprazo, change_acaoprazo, delete_acaoprazo)
    - OPERADOR:      R/W/D ✓ (add_acaoprazo, change_acaoprazo, delete_acaoprazo)
    - CONSULTOR:     R ✓ (view_acaoprazo)

    🔑 AuthorizationService + Cache 5min + Restrição única ativa por ação
    """

    queryset = AcaoPrazo.objects.select_related("idacao__ideixo").order_by(
        "-isacaoprazoativo", "-created_at"
    )
    serializer_class = AcaoPrazoSerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "acaoprazo"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Classe híbrida

    def get_permissions(self):
        """
        OPERAÇÕES (GESTOR/COORD/OPERADOR têm escrita):
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole ✅)
        - Escrita: GESTOR/COORD/OPERADOR (IsCoordernadorGestorOrOperadorPNGI ✅ + AuthorizationService)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # ✍️ ESCRITA: 3 roles têm permissão (matriz OPERAÇÕES)
            self.permission_classes = [
                IsCoordernadorGestorOrOperadorPNGI,
                HasModelPermission,
            ]
        else:
            # 👁️ Leitura: Todas as 4 roles PNGI (CONSULTOR incluso)
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros avançados para prazos."""
        queryset = super().get_queryset()

        # Filtro por ação específica
        acao_id = self.request.query_params.get("acao")
        if acao_id:
            queryset = queryset.filter(idacao_id=acao_id)

        # Filtro apenas prazos ativos
        apenas_ativos = self.request.query_params.get("ativos")
        if apenas_ativos == "true":
            queryset = queryset.filter(isacaoprazoativo=True)
        elif apenas_ativos == "false":
            queryset = queryset.filter(isacaoprazoativo=False)

        # Busca por prazo
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(strprazo__icontains=search)

        return queryset

    def perform_create(self, serializer):
        """Validação customizada na criação (1 ativo por ação)."""
        acao_id = self.request.data.get("idacao")
        is_ativo = self.request.data.get("isacaoprazoativo", True)

        if is_ativo:
            # 🚨 REGRA: Apenas 1 prazo ativo por ação
            existing = AcaoPrazo.objects.filter(
                idacao_id=acao_id, isacaoprazoativo=True
            ).exclude(pk=serializer.instance.pk if serializer.instance else None)

            if existing.exists():
                raise ValidationError(
                    {
                        "isacaoprazoativo": "Já existe um prazo ativo para esta ação. Desative-o primeiro."
                    }
                )

        super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        """Criar Prazo (GESTOR/COORD/OPERADOR)."""
        acao_id = request.data.get("idacao")
        prazo = request.data.get("strprazo", "Sem prazo")
        is_ativo = request.data.get("isacaoprazoativo", True)

        logger.info(
            f"[POST] Criando AcaoPrazo '{prazo}' (ativo={is_ativo}) para ação {acao_id}: "
            f"user={request.user.id}"
        )
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            logger.info(f"✅ AcaoPrazo '{prazo}' criado")
        return response

    def update(self, request, *args, **kwargs):
        """Alternar Prazo Ativo (GESTOR/COORD/OPERADOR)."""
        instance = self.get_object()
        old_ativo = instance.isacaoprazoativo
        new_ativo = request.data.get("isacaoprazoativo", old_ativo)

        # Validação de apenas 1 ativo por ação
        if new_ativo and new_ativo != old_ativo:
            acao_id = instance.idacao_id
            existing = AcaoPrazo.objects.filter(
                idacao_id=acao_id, isacaoprazoativo=True
            ).exclude(pk=instance.pk)

            if existing.exists():
                logger.warning(f"Tentativa de ativar 2º prazo ativo na ação {acao_id}")
                return Response(
                    {"detail": "Já existe um prazo ativo para esta ação."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        logger.info(
            f"[PATCH] Atualizando AcaoPrazo {instance.id} ativo={old_ativo}→{new_ativo}: "
            f"user={request.user.id}"
        )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Deletar Prazo (GESTOR/COORD/OPERADOR)."""
        instance = self.get_object()
        era_ativo = instance.isacaoprazoativo
        logger.warning(
            f"[DELETE] Deletando AcaoPrazo '{instance.strprazo}' (ativo={era_ativo}): "
            f"user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def acao(self, request, pk=None):
        """
        🆕 GET /api/prazos/{id}/acao/

        Detalhes da ação associada (qualquer role PNGI).
        """
        prazo = self.get_object()
        from acoes_pngi.serializers import AcoesSerializer

        serializer = AcoesSerializer(prazo.idacao)

        return Response(
            {"prazo": AcaoPrazoSerializer(prazo).data, "acao": serializer.data}
        )

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/prazos/stats/

        Estatísticas dos prazos (qualquer role PNGI).
        """
        from django.db.models import Count

        stats = {
            "total_prazos": AcaoPrazo.objects.count(),
            "prazos_ativos": AcaoPrazo.objects.filter(isacaoprazoativo=True).count(),
            "acoes_sem_prazo_ativo": Acoes.objects.filter(
                prazos__isacaoprazoativo=False
            )
            .distinct()
            .count(),
            "por_acao": dict(
                AcaoPrazo.objects.filter(isacaoprazoativo=True)
                .values("idacao__strapelido")
                .annotate(count=Count("id"))
                .order_by("-count")[:10]
            ),
        }

        return Response(stats)

    @action(detail=False, methods=["patch"])
    def ativar_proximo(self, request):
        """
        🆕 PATCH /api/prazos/ativar_proximo/

        Ativa próximo prazo não-ativo de uma ação específica.
        Body: {"acao_id": 123}
        """
        acao_id = request.data.get("acao_id")
        if not acao_id:
            return Response({"detail": "acao_id é obrigatório"}, status=400)

        # Buscar próximo prazo não-ativo
        proximo_prazo = (
            AcaoPrazo.objects.filter(idacao_id=acao_id, isacaoprazoativo=False)
            .order_by("created_at")
            .first()
        )

        if not proximo_prazo:
            return Response(
                {"detail": "Nenhum prazo disponível para ativar"}, status=404
            )

        # Desativar atual
        AcaoPrazo.objects.filter(idacao_id=acao_id, isacaoprazoativo=True).update(
            isacaoprazoativo=False
        )

        # Ativar próximo
        proximo_prazo.isacaoprazoativo = True
        proximo_prazo.save()

        logger.info(f"Prazo {proximo_prazo.id} ativado para ação {acao_id}")

        return Response(
            {
                "detail": "Próximo prazo ativado",
                "prazo": AcaoPrazoSerializer(proximo_prazo).data,
            }
        )


class AcaoDestaqueViewSet(viewsets.ModelViewSet):
    """
    ViewSet para AcaoDestaque (OPERAÇÕES).

    Matriz de Permissões (VALIDADA):
    - GESTOR:        R/W/D ✓ (add_acaodestaque, change_acaodestaque, delete_acaodestaque)
    - COORDENADOR:   R/W/D ✓ (add_acaodestaque, change_acaodestaque, delete_acaodestaque)
    - OPERADOR:      R/W/D ✓ (add_acaodestaque, change_acaodestaque, delete_acaodestaque)
    - CONSULTOR:     R ✓ (view_acaodestaque)

    🔑 AuthorizationService + Cache 5min + Destaques por data
    """

    queryset = AcaoDestaque.objects.select_related(
        "idacao__ideixo", "idacao__idsituacaoacao"
    ).order_by("-datdatadestaque")
    serializer_class = AcaoDestaqueSerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "acaodestaque"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Classe híbrida

    def get_permissions(self):
        """
        OPERAÇÕES (GESTOR/COORD/OPERADOR têm escrita):
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole ✅)
        - Escrita: GESTOR/COORD/OPERADOR (IsCoordernadorGestorOrOperadorPNGI ✅ + AuthorizationService)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # ✍️ ESCRITA: 3 roles têm permissão (matriz OPERAÇÕES)
            self.permission_classes = [
                IsCoordernadorGestorOrOperadorPNGI,
                HasModelPermission,
            ]
        else:
            # 👁️ Leitura: Todas as 4 roles PNGI (CONSULTOR incluso)
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros específicos para destaques."""
        queryset = super().get_queryset()

        # Filtro por ação específica
        acao_id = self.request.query_params.get("acao")
        if acao_id:
            queryset = queryset.filter(idacao_id=acao_id)

        # Filtro por data (hoje, semana, mês)
        data_filtro = self.request.query_params.get("data")
        hoje = timezone.now().date()

        if data_filtro == "hoje":
            queryset = queryset.filter(datdestaque__date=hoje)
        elif data_filtro == "semana":
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            queryset = queryset.filter(datdestaque__date__gte=inicio_semana)
        elif data_filtro == "mes":
            inicio_mes = hoje.replace(day=1)
            queryset = queryset.filter(datdestaque__date__gte=inicio_mes)

        # Busca por observação
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(strobservacaodestaque__icontains=search)

        return queryset

    def create(self, request, *args, **kwargs):
        """Criar Destaque (GESTOR/COORD/OPERADOR)."""
        acao_id = request.data.get("idacao")
        obs = request.data.get("strobservacaodestaque", "")[:100]

        logger.info(
            f"[POST] Criando AcaoDestaque para ação {acao_id}: "
            f"'{obs}', user={request.user.id}"
        )
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            logger.info(f"✅ AcaoDestaque criado para ação {acao_id}")
        return response

    def destroy(self, request, *args, **kwargs):
        """Deletar Destaque (GESTOR/COORD/OPERADOR)."""
        instance = self.get_object()
        logger.warning(
            f"[DELETE] Deletando AcaoDestaque '{instance.strobservacaodestaque[:50]}...' "
            f"da ação {instance.idacao_id}: user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def acao(self, request, pk=None):
        """
        🆕 GET /api/destaques/{id}/acao/

        Detalhes da ação destacada (qualquer role PNGI).
        """
        destaque = self.get_object()
        from acoes_pngi.serializers import AcoesSerializer

        serializer = AcoesSerializer(destaque.idacao)

        return Response(
            {"destaque": AcaoDestaqueSerializer(destaque).data, "acao": serializer.data}
        )

    @action(detail=False, methods=["get"])
    def hoje(self, request):
        """
        🆕 GET /api/destaques/hoje/

        Destaques de hoje (qualquer role PNGI).
        """
        hoje = timezone.now().date()
        destaques_hoje = self.get_queryset().filter(datdestaque__date=hoje)

        serializer = self.get_serializer(destaques_hoje, many=True)
        return Response(
            {
                "data": hoje.strftime("%Y-%m-%d"),
                "total_hoje": destaques_hoje.count(),
                "destaques": serializer.data,
            }
        )

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/destaques/stats/

        Estatísticas dos destaques (qualquer role PNGI).
        """
        from django.db.models import Count

        hoje = timezone.now().date()

        stats = {
            "total_destaques": AcaoDestaque.objects.count(),
            "hoje": AcaoDestaque.objects.filter(datdestaque__date=hoje).count(),
            "semana": AcaoDestaque.objects.filter(
                datdestaque__date__gte=hoje - timedelta(days=7)
            ).count(),
            "top_acoes": dict(
                AcaoDestaque.objects.values("idacao__strapelido")
                .annotate(count=Count("id"))
                .order_by("-count")[:5]
            ),
        }

        return Response(stats)

    @action(detail=False, methods=["get"])
    def por_acao(self, request):
        """
        🆕 GET /api/destaques/por_acao/?acao=123
        ou GET /api/destaques/por_acao/?limit=5

        Destaques por ação (paginado).
        """
        limit = int(self.request.query_params.get("limit", 10))
        acoes_com_destaques = (
            AcaoDestaque.objects.values("idacao", "idacao__strapelido")
            .annotate(count=Count("id"))
            .order_by("-count")[:limit]
        )

        return Response({"acoes_com_mais_destaques": list(acoes_com_destaques)})


# ============================================================================
# VIEWSETS DE ALINHAMENTO
# ============================================================================


class TipoAnotacaoAlinhamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para TipoAnotacaoAlinhamento (Nível 2 - Configurações Compartilhadas).

    Matriz de Permissões (VALIDADA):
    - GESTOR:        R/W/D ✓ (add_tipoanotacaoalinhamento, change_tipoanotacaoalinhamento, delete_tipoanotacaoalinhamento)
    - COORDENADOR:   R/W/D ✓ (add_tipoanotacaoalinhamento, change_tipoanotacaoalinhamento, delete_tipoanotacaoalinhamento)
    - OPERADOR:      R ✓ (view_tipoanotacaoalinhamento)
    - CONSULTOR:     R ✓ (view_tipoanotacaoalinhamento)

    🔑 AuthorizationService + Cache 5min + Integração com anotações
    """

    queryset = TipoAnotacaoAlinhamento.objects.all().order_by(
        "strdescricaotipoanotacaoalinhamento"
    )
    serializer_class = TipoAnotacaoAlinhamentoSerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "tipoanotacaoalinhamento"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Classe híbrida

    def get_permissions(self):
        """
        Nível 2 - CONFIGURAÇÕES COMPARTILHADAS:
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole ✅)
        - Escrita: GESTOR + COORDENADOR (IsCoordernadorOrGestorPNGI ✅ + AuthorizationService)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # ✍️ ESCRITA: GESTOR e COORDENADOR (mesma lógica Eixo/Vigencia)
            self.permission_classes = [IsCoordernadorOrGestorPNGI, HasModelPermission]
        else:
            # 👁️ Leitura: Todas as 4 roles PNGI
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros específicos para tipos de anotação."""
        queryset = super().get_queryset()

        # Filtro por descrição
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                strdescricaotipoanotacaoalinhamento__icontains=search
            )

        return queryset

    def create(self, request, *args, **kwargs):
        """Criar Tipo de Anotação (GESTOR/COORDENADOR)."""
        new_tipo = request.data.get("strdescricaotipoanotacaoalinhamento", "").upper()
        obs_trunc = new_tipo[:50]  # ✅ Correção Pylance

        logger.info(
            f"[POST] Criando TipoAnotacaoAlinhamento '{new_tipo}': "
            f"user={request.user.id}, role={getattr(request, 'token_payload', {}).get('role_code')}"
        )
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            logger.info(f"✅ TipoAnotacaoAlinhamento '{obs_trunc}' criado")
        return response

    def destroy(self, request, *args, **kwargs):
        """Deletar Tipo de Anotação (GESTOR/COORDENADOR)."""
        instance = self.get_object()
        obs_trunc = instance.strdescricaotipoanotacaoalinhamento[
            :50
        ]  # ✅ Correção Pylance

        logger.warning(
            f"[DELETE] Deletando TipoAnotacaoAlinhamento '{obs_trunc}...': "
            f"user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/tipos-anotacao/stats/

        Estatísticas dos tipos de anotação (qualquer role PNGI).
        """
        from django.db.models import Count

        from acoes_pngi.models import AcaoAnotacaoAlinhamento

        stats = (
            TipoAnotacaoAlinhamento.objects.annotate(
                anotacoes_count=Count("acaoanotacaoalinhamento")
            )
            .values("strdescricaotipoanotacaoalinhamento", "anotacoes_count")
            .order_by("-anotacoes_count")
        )

        total_anotacoes = AcaoAnotacaoAlinhamento.objects.count()

        return Response(
            {
                "total_tipos": TipoAnotacaoAlinhamento.objects.count(),
                "total_anotacoes": total_anotacoes,
                "tipos": list(stats),
            }
        )

    @action(detail=True, methods=["get"])
    def anotacoes(self, request, pk=None):
        """
        🆕 GET /api/tipos-anotacao/{id}/anotacoes/

        Anotações deste tipo (qualquer role PNGI).
        """
        tipo_anotacao = self.get_object()

        from acoes_pngi.serializers import AcaoAnotacaoAlinhamentoSerializer

        serializer = AcaoAnotacaoAlinhamentoSerializer(
            tipo_anotacao.acaoanotacaoalinhamento.all(), many=True
        )

        return Response(
            {
                "tipo_anotacao": {
                    "id": tipo_anotacao.idtipoanotacaoalinhamento,
                    "descricao": tipo_anotacao.strdescricaotipoanotacaoalinhamento,
                },
                "anotacoes_count": tipo_anotacao.acaoanotacaoalinhamento.count(),
                "anotacoes": serializer.data[:20],  # Top 20 anotações
            }
        )

    @action(detail=False, methods=["get"])
    def mais_usados(self, request):
        """
        🆕 GET /api/tipos-anotacao/mais_usados/?limit=5

        Top tipos de anotação mais utilizados.
        """
        limit = int(self.request.query_params.get("limit", 5))

        from django.db.models import Count

        top_tipos = TipoAnotacaoAlinhamento.objects.annotate(
            count=Count("acaoanotacaoalinhamento")
        ).order_by("-count")[:limit]

        serializer = self.get_serializer(top_tipos, many=True)

        return Response(
            {
                "mais_usados": serializer.data,
                "total_anotacoes": sum([t.anotacoes_count for t in top_tipos]),
            }
        )


class AcaoAnotacaoAlinhamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para AcaoAnotacaoAlinhamento (OPERAÇÕES).

    Matriz de Permissões (VALIDADA):
    - GESTOR:        R/W/D ✓ (add_acaoanotacaoalinhamento, change_acaoanotacaoalinhamento, delete_acaoanotacaoalinhamento)
    - COORDENADOR:   R/W/D ✓ (add_acaoanotacaoalinhamento, change_acaoanotacaoalinhamento, delete_acaoanotacaoalinhamento)
    - OPERADOR:      R/W/D ✓ (add_acaoanotacaoalinhamento, change_acaoanotacaoalinhamento, delete_acaoanotacaoalinhamento)
    - CONSULTOR:     R ✓ (view_acaoanotacaoalinhamento)

    🔑 AuthorizationService + Cache 5min + Anotações por ação/tipo
    """

    queryset = AcaoAnotacaoAlinhamento.objects.select_related(
        "idacao__ideixo", "idacao__idsituacaoacao", "idtipoanotacaoalinhamento"
    ).order_by("-created_at")
    serializer_class = AcaoAnotacaoAlinhamentoSerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "acaoanotacaoalinhamento"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Classe híbrida

    def get_permissions(self):
        """
        OPERAÇÕES (GESTOR/COORD/OPERADOR têm escrita):
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole ✅)
        - Escrita: GESTOR/COORD/OPERADOR (IsCoordernadorGestorOrOperadorPNGI ✅ + AuthorizationService)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # ✍️ ESCRITA: 3 roles têm permissão (matriz OPERAÇÕES)
            self.permission_classes = [
                IsCoordernadorGestorOrOperadorPNGI,
                HasModelPermission,
            ]
        else:
            # 👁️ Leitura: Todas as 4 roles PNGI (CONSULTOR incluso)
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros avançados para anotações."""
        queryset = super().get_queryset()

        # Filtro por ação específica
        acao_id = self.request.query_params.get("acao")
        if acao_id:
            queryset = queryset.filter(idacao_id=acao_id)

        # Filtro por tipo de anotação
        tipo_id = self.request.query_params.get("tipo")
        if tipo_id:
            queryset = queryset.filter(idtipoanotacaoalinhamento_id=tipo_id)

        # Filtro por texto
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(stranotacaoalinhamento__icontains=search)

        # Recentes (últimos 30 dias)
        recentes = self.request.query_params.get("recentes")
        if recentes == "true":
            desde = timezone.now() - timedelta(days=30)
            queryset = queryset.filter(created_at__gte=desde)

        return queryset

    def create(self, request, *args, **kwargs):
        """Criar Anotação (GESTOR/COORD/OPERADOR)."""
        acao_id = request.data.get("idacao")
        tipo_id = request.data.get("idtipoanotacaoalinhamento")
        texto = request.data.get("stranotacaoalinhamento", "")
        obs_trunc = texto[:80]  # ✅ Correção Pylance

        logger.info(
            f"[POST] Criando AcaoAnotacao para ação {acao_id}, tipo {tipo_id}: "
            f"'{obs_trunc}', user={request.user.id}"
        )
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            logger.info(f"✅ AcaoAnotacaoAlinhamento criado para ação {acao_id}")
        return response

    def destroy(self, request, *args, **kwargs):
        """Deletar Anotação (GESTOR/COORD/OPERADOR)."""
        instance = self.get_object()
        obs_trunc = instance.stranotacaoalinhamento[:50]  # ✅ Correção Pylance

        logger.warning(
            f"[DELETE] Deletando AcaoAnotacaoAlinhamento '{obs_trunc}...' "
            f"da ação {instance.idacao_id}: user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def acao(self, request, pk=None):
        """
        🆕 GET /api/anotacoes/{id}/acao/

        Detalhes da ação anotada (qualquer role PNGI).
        """
        anotacao = self.get_object()
        from acoes_pngi.serializers import AcoesSerializer

        serializer = AcoesSerializer(anotacao.idacao)

        return Response(
            {
                "anotacao": AcaoAnotacaoAlinhamentoSerializer(anotacao).data,
                "acao": serializer.data,
                "tipo": TipoAnotacaoAlinhamentoSerializer(
                    anotacao.idtipoanotacaoalinhamento
                ).data,
            }
        )

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/anotacoes/stats/

        Estatísticas das anotações (qualquer role PNGI).
        """
        from django.db.models import Count

        stats = {
            "total_anotacoes": AcaoAnotacaoAlinhamento.objects.count(),
            "por_tipo": dict(
                AcaoAnotacaoAlinhamento.objects.values(
                    "idtipoanotacaoalinhamento__strdescricaotipoanotacaoalinhamento"
                )
                .annotate(count=Count("id"))
                .order_by("-count")
            ),
            "por_acao": dict(
                AcaoAnotacaoAlinhamento.objects.values("idacao__strapelido")
                .annotate(count=Count("id"))
                .order_by("-count")[:10]
            ),
            "recentes_30d": AcaoAnotacaoAlinhamento.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=30)
            ).count(),
        }

        return Response(stats)

    @action(detail=False, methods=["get"])
    def por_acao(self, request):
        """
        🆕 GET /api/anotacoes/por_acao/?acao=123&limit=20

        Anotações de uma ação específica.
        """
        acao_id = self.request.query_params.get("acao")
        limit = int(self.request.query_params.get("limit", 20))

        if acao_id:
            anotacoes = self.get_queryset().filter(idacao_id=acao_id)[:limit]
        else:
            # Top ações com mais anotações
            anotacoes = self.get_queryset().order_by("-created_at")[:limit]

        serializer = self.get_serializer(anotacoes, many=True)
        return Response(serializer.data)


# ============================================================================
# VIEWSETS DE RESPONSÁVEIS
# ============================================================================


class UsuarioResponsavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para UsuarioResponsavel (OPERAÇÕES - Cross-schema public).

    Matriz de Permissões (VALIDADA):
    - GESTOR:        R/W/D ✓ (add_usuarioresponsavel, change_usuarioresponsavel, delete_usuarioresponsavel)
    - COORDENADOR:   R/W/D ✓ (add_usuarioresponsavel, change_usuarioresponsavel, delete_usuarioresponsavel)
    - OPERADOR:      R/W/D ✓ (add_usuarioresponsavel, change_usuarioresponsavel, delete_usuarioresponsavel)
    - CONSULTOR:     R ✓ (view_usuarioresponsavel)

    🔑 AuthorizationService + Integração IAM (schema public)
    """

    queryset = UsuarioResponsavel.objects.select_related("idusuario").order_by(
        "idusuario__name"
    )
    serializer_class = UsuarioResponsavelSerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "usuarioresponsavel"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Classe híbrida

    def get_permissions(self):
        """
        OPERAÇÕES (GESTOR/COORD/OPERADOR têm escrita):
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole ✅)
        - Escrita: GESTOR/COORD/OPERADOR (IsCoordernadorGestorOrOperadorPNGI ✅ + AuthorizationService)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # ✍️ ESCRITA: 3 roles têm permissão (matriz OPERAÇÕES)
            self.permission_classes = [
                IsCoordernadorGestorOrOperadorPNGI,
                HasModelPermission,
            ]
        else:
            # 👁️ Leitura: Todas as 4 roles PNGI (CONSULTOR incluso)
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros específicos para responsáveis."""
        queryset = super().get_queryset()

        # Filtro por nome do usuário
        nome = self.request.query_params.get("nome")
        if nome:
            queryset = queryset.filter(idusuario__name__icontains=nome)

        # Filtro por email
        email = self.request.query_params.get("email")
        if email:
            queryset = queryset.filter(idusuario__email__icontains=email)

        # Apenas ativos
        ativos = self.request.query_params.get("ativos")
        if ativos == "true":
            queryset = queryset.filter(idusuario__is_active=True)

        return queryset

    def create(self, request, *args, **kwargs):
        """Criar Responsável (GESTOR/COORD/OPERADOR)."""
        usuario_id = request.data.get("idusuario")
        nome_user = request.data.get("idusuario__name", "Desconhecido")[
            :30
        ]  # ✅ Pylance

        logger.info(
            f"[POST] Criando UsuarioResponsavel para usuário {usuario_id}: "
            f"'{nome_user}', user={request.user.id}"
        )
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            logger.info(f"✅ UsuarioResponsavel {usuario_id} criado")
        return response

    def destroy(self, request, *args, **kwargs):
        """Deletar Responsável (GESTOR/COORD/OPERADOR)."""
        instance = self.get_object()
        nome_trunc = instance.idusuario.name[:30]  # ✅ Pylance

        logger.warning(
            f"[DELETE] Deletando UsuarioResponsavel '{nome_trunc}': "
            f"user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def acoes(self, request, pk=None):
        """
        🆕 GET /api/responsaveis/{id}/acoes/

        Ações atribuídas ao responsável (qualquer role PNGI).
        """
        responsavel = self.get_object()

        from acoes_pngi.models import RelacaoAcaoUsuarioResponsavel
        from acoes_pngi.serializers import AcoesSerializer

        acoes = (
            RelacaoAcaoUsuarioResponsavel.objects.filter(
                idusuarioresponsavel=responsavel
            )
            .select_related("idacao")
            .values_list("idacao", flat=True)
        )

        acoes_qs = Acoes.objects.filter(id__in=acoes)
        serializer = AcoesSerializer(acoes_qs, many=True)

        return Response(
            {
                "responsavel": {
                    "id": responsavel.idusuarioresponsavel,
                    "usuario": {
                        "id": responsavel.idusuario.id,
                        "name": responsavel.idusuario.name,
                        "email": responsavel.idusuario.email,
                    },
                },
                "acoes_count": acoes_qs.count(),
                "acoes": serializer.data[:15],  # Top 15 ações
            }
        )

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/responsaveis/stats/

        Estatísticas dos responsáveis (qualquer role PNGI).
        """
        from django.db.models import Count

        from acoes_pngi.models import RelacaoAcaoUsuarioResponsavel

        stats = {
            "total_responsaveis": UsuarioResponsavel.objects.count(),
            "responsaveis_ativos": UsuarioResponsavel.objects.filter(
                idusuario__is_active=True
            ).count(),
            "com_acoes": dict(
                UsuarioResponsavel.objects.filter(
                    relacaoacaousuariorresponsavel__isnull=False
                )
                .annotate(acoes_count=Count("relacaoacaousuariorresponsavel"))
                .values("idusuario__name", "acoes_count")
                .order_by("-acoes_count")[:10]
            ),
            "acoes_por_responsavel": RelacaoAcaoUsuarioResponsavel.objects.values(
                "idusuarioresponsavel__idusuario__name"
            )
            .annotate(count=Count("id"))
            .count(),
        }

        return Response(stats)

    @action(detail=False, methods=["get"])
    def sobrecarregados(self, request):
        """
        🆕 GET /api/responsaveis/sobrecarregados/?limite=5

        Responsáveis com mais ações (alerta gestão).
        """
        limite = int(self.request.query_params.get("limite", 5))

        sobrecarregados = (
            UsuarioResponsavel.objects.filter(
                relacaoacaousuariorresponsavel__isnull=False
            )
            .annotate(acoes_count=Count("relacaoacaousuariorresponsavel"))
            .filter(acoes_count__gte=5)
            .order_by("-acoes_count")[:limite]
        )

        serializer = self.get_serializer(sobrecarregados, many=True)

        return Response(
            {
                "sobrecarregados": serializer.data,
                "limite_usado": limite,
                "total_sobrecarregados": UsuarioResponsavel.objects.annotate(
                    acoes_count=Count("relacaoacaousuariorresponsavel")
                )
                .filter(acoes_count__gte=5)
                .count(),
            }
        )


class RelacaoAcaoUsuarioResponsavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para RelacaoAcaoUsuarioResponsavel (OPERAÇÕES - FINAL).
    🎯 Many-to-Many: Ações ↔ Responsáveis

    Matriz de Permissões (VALIDADA 100%):
    - GESTOR:        R/W/D ✓ (add_relacaoacaousuariorresponsavel, change_*, delete_*)
    - COORDENADOR:   R/W/D ✓
    - OPERADOR:      R/W/D ✓
    - CONSULTOR:     R ✓ (view_relacaoacaousuariorresponsavel)

    🔑 AuthorizationService + Cache + Validação duplicatas
    ✅ MIGRAÇÃO 100% CONCLUÍDA!
    """

    queryset = RelacaoAcaoUsuarioResponsavel.objects.select_related(
        "idacao__ideixo", "idusuarioresponsavel__idusuario"
    ).order_by("idacao__strapelido")
    serializer_class = RelacaoAcaoUsuarioResponsavelSerializer

    # 🆕 LINHAS NOVAS (OBRIGATÓRIAS)
    permission_model = "relacaoacaousuariorresponsavel"  # ← Nome exato do modelo Django
    permission_classes = [ReadOnlyOrHasPermission]  # ← Classe híbrida

    def get_permissions(self):
        """
        OPERAÇÕES COMPLETAS (GESTOR/COORD/OPERADOR):
        - Leitura: Qualquer role PNGI (IsAnyPNGIRole ✅)
        - Escrita: GESTOR/COORD/OPERADOR (IsCoordernadorGestorOrOperadorPNGI ✅ + AuthorizationService)
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [
                IsCoordernadorGestorOrOperadorPNGI,
                HasModelPermission,
            ]
        else:
            self.permission_classes = [IsAnyPNGIRole, HasModelPermission]

        return super().get_permissions()

    def get_queryset(self):
        """Filtros avançados para relações ação-responsável."""
        queryset = super().get_queryset()

        # Filtro por ação
        acao_id = self.request.query_params.get("acao")
        if acao_id:
            queryset = queryset.filter(idacao_id=acao_id)

        # Filtro por responsável
        responsavel_id = self.request.query_params.get("responsavel")
        if responsavel_id:
            queryset = queryset.filter(idusuarioresponsavel_id=responsavel_id)

        # Apenas ações ativas
        acoes_ativas = self.request.query_params.get("acoes_ativas")
        if acoes_ativas == "true":
            queryset = queryset.filter(
                idacao__idsituacaoacao__strdescricaosituacao__in=[
                    "EM_ANDAMENTO",
                    "PLANEJADA",  # Ajuste conforme seus status
                ]
            )

        return queryset

    def create(self, request, *args, **kwargs):
        """Criar Relação Ação-Responsável (GESTOR/COORD/OPERADOR)."""
        acao_id = request.data.get("idacao")
        responsavel_id = request.data.get("idusuarioresponsavel")

        # 🚨 Evitar duplicatas
        if RelacaoAcaoUsuarioResponsavel.objects.filter(
            idacao_id=acao_id, idusuarioresponsavel_id=responsavel_id
        ).exists():
            return Response(
                {"detail": "Esta relação ação-responsável já existe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(
            f"[POST] Criando RelacaoAcaoUsuarioResponsavel: "
            f"ação={acao_id}, responsável={responsavel_id}, user={request.user.id}"
        )
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            logger.info(
                f"✅ Relação criada: ação {acao_id} ← responsável {responsavel_id}"
            )
        return response

    def destroy(self, request, *args, **kwargs):
        """Remover Responsável de Ação (GESTOR/COORD/OPERADOR)."""
        instance = self.get_object()
        logger.warning(
            f"[DELETE] Removendo responsável {instance.idusuarioresponsavel_id} "
            f"da ação {instance.idacao_id}: user={request.user.id}"
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        🆕 GET /api/relacoes/stats/

        Estatísticas das atribuições (qualquer role PNGI).
        🎯 Dashboard gestão de responsáveis
        """
        from django.db.models import Count

        stats = {
            "total_relacoes": RelacaoAcaoUsuarioResponsavel.objects.count(),
            "acoes_com_responsavel": Acoes.objects.filter(
                relacaoacaousuariorresponsavel__isnull=False
            )
            .distinct()
            .count(),
            "responsaveis_por_acao": dict(
                RelacaoAcaoUsuarioResponsavel.objects.values("idacao__strapelido")
                .annotate(count=Count("idusuarioresponsavel"))
                .order_by("-count")[:10]
            ),
            "acoes_por_responsavel": dict(
                RelacaoAcaoUsuarioResponsavel.objects.values(
                    "idusuarioresponsavel__idusuario__name"
                )
                .annotate(count=Count("idacao"))
                .order_by("-count")[:10]
            ),
            "acoes_sem_responsavel": Acoes.objects.filter(
                relacaoacaousuariorresponsavel__isnull=True
            ).count(),
        }

        return Response(stats)

    @action(detail=True, methods=["get"])
    def detalhes(self, request, pk=None):
        """
        🆕 GET /api/relacoes/{id}/detalhes/

        Detalhes completos da relação (qualquer role PNGI).
        """
        relacao = self.get_object()

        return Response(
            {
                "relacao": RelacaoAcaoUsuarioResponsavelSerializer(relacao).data,
                "acao": AcoesSerializer(relacao.idacao).data,
                "responsavel": UsuarioResponsavelSerializer(
                    relacao.idusuarioresponsavel
                ).data,
                "usuario_iam": {
                    "id": relacao.idusuarioresponsavel.idusuario.id,
                    "name": relacao.idusuarioresponsavel.idusuario.name,
                    "email": relacao.idusuarioresponsavel.idusuario.email,
                    "is_active": relacao.idusuarioresponsavel.idusuario.is_active,
                },
            }
        )

    @action(detail=False, methods=["get"])
    def sobrecarga(self, request):
        """
        🆕 GET /api/relacoes/sobrecarga/?limite=5

        Responsáveis sobrecarregados (>5 ações).
        """
        limite = int(self.request.query_params.get("limite", 5))

        sobrecarga = (
            RelacaoAcaoUsuarioResponsavel.objects.values(
                "idusuarioresponsavel__idusuario__name",
                "idusuarioresponsavel__idusuario__email",
            )
            .annotate(acoes_count=Count("idacao"))
            .filter(acoes_count__gt=5)
            .order_by("-acoes_count")[:limite]
        )

        return Response(
            {
                "sobrecarregados": list(sobrecarga),
                "limite": limite,
                "total_sobrecarregados": RelacaoAcaoUsuarioResponsavel.objects.values(
                    "idusuarioresponsavel"
                )
                .annotate(count=Count("idacao"))
                .filter(count__gt=5)
                .count(),
            }
        )


class AcoesCompletasAPIView(generics.ListAPIView):
    """
    🔗 API: Lista COMPLETA de ações com todas as relações aninhadas

    Query otimizada com prefetch_related para evitar N+1

    ?page=1&limit=20&vigencia=1&eixo=ABC&situacao=Ativa

    Retorna:
    {
        "count": 150,
        "results": [
            {
                "id": 1,
                "strapelido": "AÇÃ 001",
                "eixo": {...},
                "situacao": {...},
                "vigencia": {...},
                "responsaveis": [...],
                "prazo_ativo": {...},
                "ultimos_destaques": [...],
                "ultimas_anotacoes": [...]
            }
        ]
    }
    """

    serializer_class = AcoesCompletasSerializer
    permission_classes = [IsAuthenticated, HasModelPermission]
    permission_model = "acoes"  # ← AuthorizationService

    def get_queryset(self):
        """
        Query otimizada com filtros dinâmicos e todas as relações
        """
        queryset = (
            Acoes.objects.select_related(
                "ideixo", "idsituacaoacao", "idvigenciapngi", "idtipoentravealerta"
            )
            .prefetch_related(
                Prefetch(
                    "responsaveis",
                    queryset=RelacaoAcaoUsuarioResponsavel.objects.prefetch_related(
                        Prefetch("idusuarioresponsavel")
                    ),
                    to_attr="responsaveis_completos",
                ),
                Prefetch(
                    "prazos",
                    queryset=AcaoPrazo.objects.filter(isacaoprazoativo=True),
                    to_attr="prazo_ativo",
                ),
                Prefetch(
                    "destaques",
                    queryset=AcaoDestaque.objects.order_by("-datdatadestaque")[:3],
                    to_attr="ultimos_destaques",
                ),
                Prefetch(
                    "anotacoes_alinhamento",
                    queryset=AcaoAnotacaoAlinhamento.objects.select_related(
                        "idtipoanotacaoalinhamento"
                    ).order_by("-datdataanotacaoalinhamento")[:5],
                    to_attr="ultimas_anotacoes",
                ),
            )
            .filter(idvigenciapngi__isvigenciaativa=True)
        )

        # Filtros dinâmicos via query params
        eixo_id = self.request.query_params.get("eixo")
        if eixo_id:
            queryset = queryset.filter(ideixo_id=eixo_id)

        situacao_id = self.request.query_params.get("situacao")
        if situacao_id:
            queryset = queryset.filter(idsituacaoacao_id=situacao_id)

        return queryset.order_by("strapelido")


# API: Usuários por Ação Específica
class UsuariosPorAcaoAPIView(generics.ListAPIView):
    """
    GET /api/acoes-pngi/acoes/<id>/usuarios/

    Retorna todos os responsáveis de uma ação específica
    """

    serializer_class = UsuarioResponsavelCompletoSerializer
    permission_classes = [IsAuthenticated, HasModelPermission]
    permission_model = "relacaoacaousuarioresponsavel"

    def get_queryset(self):
        acao_id = self.kwargs["acao_id"]
        return UsuarioResponsavel.objects.filter(
            relacaoacaousuarioresponsavel__idacao_id=acao_id
        ).select_related("idusuario")
