"""Example: Refactored acoes_pngi ViewSets

This file shows how to refactor acoes_pngi ViewSets to use
the new IAM architecture. Copy these patterns to your actual
ViewSets.

IMPORTANT: This is EXAMPLE code. Adapt to your actual models.
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from core.iam.interfaces.permissions import RequireRole, HasAppPermission

# Assuming these imports exist in acoes_pngi
# from acoes_pngi.models import (
#     SituacaoAcao, TipoEntraveAlerta, Eixo, VigenciaPNGI,
#     TipoAnotacaoAlinhamento, Acoes, AcaoPrazo, AcaoDestaque,
#     AcaoAnotacaoAlinhamento, UsuarioResponsavel,
#     RelacaoAcaoUsuarioResponsavel
# )
# from acoes_pngi.serializers import (
#     SituacaoAcaoSerializer, TipoEntraveAlertaSerializer,
#     EixoSerializer, VigenciaPNGISerializer, ...
# )


# ============================================================================
# CONFIGURAÇÕES - NÍVEL 1 (Apenas GESTOR pode escrever)
# ============================================================================

class SituacaoAcaoViewSet(ModelViewSet):
    """
    ViewSet para SituacaoAcao
    
    Permissões:
    - Read: Todos (GESTOR, COORDENADOR, OPERADOR, CONSULTOR)
    - Write/Delete: Apenas GESTOR
    
    Substitui: IsGestorPNGI permission class
    """
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = ['GESTOR_PNGI']
    
    # queryset = SituacaoAcao.objects.all()
    # serializer_class = SituacaoAcaoSerializer
    
    def get_queryset(self):
        """Customize queryset if needed"""
        # Example: filter based on user's organization
        # if hasattr(self.request.user, 'organizacao'):
        #     return SituacaoAcao.objects.filter(...)
        return self.queryset


class TipoEntraveAlertaViewSet(ModelViewSet):
    """
    ViewSet para TipoEntraveAlerta
    
    Mesmas permissões que SituacaoAcao
    """
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = ['GESTOR_PNGI']
    
    # queryset = TipoEntraveAlerta.objects.all()
    # serializer_class = TipoEntraveAlertaSerializer


# ============================================================================
# CONFIGURAÇÕES - NÍVEL 2 (GESTOR e COORDENADOR podem escrever)
# ============================================================================

class EixoViewSet(ModelViewSet):
    """
    ViewSet para Eixo
    
    Permissões:
    - Read: Todos
    - Write/Delete: GESTOR e COORDENADOR
    
    Substitui: IsCoordernadorOrGestorPNGI permission class
    """
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = ['GESTOR_PNGI', 'COORDENADOR_PNGI']
    
    # queryset = Eixo.objects.all().order_by('stralias')
    # serializer_class = EixoSerializer
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Custom action: listar apenas eixos ativos"""
        # Example custom action
        # queryset = self.get_queryset().filter(ativo=True)
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
        return Response({'message': 'Custom action example'})


class VigenciaPNGIViewSet(ModelViewSet):
    """
    ViewSet para VigenciaPNGI
    
    Mesmas permissões que Eixo
    """
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = ['GESTOR_PNGI', 'COORDENADOR_PNGI']
    
    # queryset = VigenciaPNGI.objects.all().order_by('-datiniciovigencia')
    # serializer_class = VigenciaPNGISerializer
    
    @action(detail=False, methods=['get'])
    def vigente(self, request):
        """Retorna vigência ativa atual"""
        # queryset = self.get_queryset().filter(
        #     isvigenciaativa=True,
        #     datiniciovigencia__lte=date.today(),
        #     datfinalvigencia__gte=date.today()
        # ).first()
        # if queryset:
        #     serializer = self.get_serializer(queryset)
        #     return Response(serializer.data)
        # return Response({'detail': 'Nenhuma vigência ativa'}, status=404)
        return Response({'message': 'Vigencia ativa example'})


class TipoAnotacaoAlinhamentoViewSet(ModelViewSet):
    """
    ViewSet para TipoAnotacaoAlinhamento
    
    Mesmas permissões que Eixo
    """
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = ['GESTOR_PNGI', 'COORDENADOR_PNGI']
    
    # queryset = TipoAnotacaoAlinhamento.objects.all()
    # serializer_class = TipoAnotacaoAlinhamentoSerializer


# ============================================================================
# OPERAÇÕES (GESTOR, COORDENADOR e OPERADOR podem escrever)
# ============================================================================

class AcoesViewSet(ModelViewSet):
    """
    ViewSet para Acoes
    
    Permissões:
    - Read: Todos
    - Write/Delete: GESTOR, COORDENADOR e OPERADOR
    
    Substitui: IsCoordernadorGestorOrOperadorPNGI permission class
    """
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO'
    ]
    
    # queryset = Acoes.objects.select_related(
    #     'ideixo', 'idsituacaoacao', 'idvigenciapngi', 'idtipoentravealerta'
    # ).all()
    # serializer_class = AcoesSerializer
    
    def get_queryset(self):
        """Filter by query params"""
        queryset = self.queryset
        
        # Example: filter by eixo
        # eixo_id = self.request.query_params.get('eixo', None)
        # if eixo_id:
        #     queryset = queryset.filter(ideixo_id=eixo_id)
        
        # Example: filter by situacao
        # situacao = self.request.query_params.get('situacao', None)
        # if situacao:
        #     queryset = queryset.filter(idsituacaoacao__strdescricaosituacao=situacao)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def em_atraso(self, request):
        """Ações em atraso"""
        # Example: custom filtering
        # from datetime import date
        # queryset = self.get_queryset().filter(
        #     datdataentrega__lt=date.today(),
        #     idsituacaoacao__strdescricaosituacao__in=['Em Andamento', 'Pendente']
        # )
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
        return Response({'message': 'Acoes em atraso example'})
    
    @action(detail=True, methods=['post'])
    def adicionar_prazo(self, request, pk=None):
        """Adicionar prazo a uma ação"""
        # acao = self.get_object()
        # prazo_serializer = AcaoPrazoSerializer(data=request.data)
        # if prazo_serializer.is_valid():
        #     prazo_serializer.save(idacao=acao)
        #     return Response(prazo_serializer.data, status=201)
        # return Response(prazo_serializer.errors, status=400)
        return Response({'message': 'Prazo adicionado'})


class AcaoPrazoViewSet(ModelViewSet):
    """ViewSet para AcaoPrazo"""
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO'
    ]
    
    # queryset = AcaoPrazo.objects.select_related('idacao').all()
    # serializer_class = AcaoPrazoSerializer


class AcaoDestaqueViewSet(ModelViewSet):
    """ViewSet para AcaoDestaque"""
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO'
    ]
    
    # queryset = AcaoDestaque.objects.select_related('idacao').all()
    # serializer_class = AcaoDestaqueSerializer


class AcaoAnotacaoAlinhamentoViewSet(ModelViewSet):
    """ViewSet para AcaoAnotacaoAlinhamento"""
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO'
    ]
    
    # queryset = AcaoAnotacaoAlinhamento.objects.select_related(
    #     'idacao', 'idtipoanotacaoalinhamento'
    # ).all()
    # serializer_class = AcaoAnotacaoAlinhamentoSerializer


class UsuarioResponsavelViewSet(ModelViewSet):
    """ViewSet para UsuarioResponsavel"""
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO'
    ]
    
    # queryset = UsuarioResponsavel.objects.select_related('idusuario').all()
    # serializer_class = UsuarioResponsavelSerializer


class RelacaoAcaoUsuarioResponsavelViewSet(ModelViewSet):
    """ViewSet para RelacaoAcaoUsuarioResponsavel"""
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO'
    ]
    
    # queryset = RelacaoAcaoUsuarioResponsavel.objects.select_related(
    #     'idacao', 'idusuarioresponsavel'
    # ).all()
    # serializer_class = RelacaoAcaoUsuarioResponsavelSerializer


# ============================================================================
# ALTERNATIVE: Using HasAppPermission (Django Permission-Based)
# ============================================================================

class EixoViewSetAlternative(ModelViewSet):
    """
    Alternative implementation using HasAppPermission
    
    This automatically maps HTTP methods to Django permissions:
    - GET → view_eixo
    - POST → add_eixo
    - PUT/PATCH → change_eixo
    - DELETE → delete_eixo
    
    Requires that RolePermission mappings are properly configured
    in the database linking roles to these permissions.
    """
    permission_classes = [HasAppPermission]
    app_code = 'ACOES_PNGI'
    
    # queryset = Eixo.objects.all().order_by('stralias')
    # serializer_class = EixoSerializer


# ============================================================================
# GESTÃO DE USUÁRIOS (Apenas GESTOR)
# ============================================================================

class UserManagementViewSet(ModelViewSet):
    """
    ViewSet para gestão de usuários e roles
    
    Permissões:
    - Read: Todos (para ver lista de usuários)
    - Write/Delete: Apenas GESTOR
    
    Substitui: IsGestorPNGIOnly permission class
    """
    permission_classes = [RequireRole]
    app_code = 'ACOES_PNGI'
    required_roles_read = [
        'GESTOR_PNGI',
        'COORDENADOR_PNGI',
        'OPERADOR_ACAO',
        'CONSULTOR_PNGI'
    ]
    required_roles_write = ['GESTOR_PNGI']
    
    # from core.iam.models import User
    # queryset = User.objects.filter(is_active=True)
    # from core.iam.serializers import UserDetailSerializer
    # serializer_class = UserDetailSerializer
    
    @action(detail=True, methods=['post'])
    def assign_role(self, request, pk=None):
        """Atribuir role a um usuário"""
        # Only GESTOR can do this (enforced by required_roles_write)
        # user = self.get_object()
        # role_id = request.data.get('role_id')
        # app_code = request.data.get('app_code', 'ACOES_PNGI')
        # 
        # from core.iam.models import UserRole, Role, Aplicacao
        # role = Role.objects.get(id=role_id)
        # app = Aplicacao.objects.get(codigointerno=app_code)
        # 
        # UserRole.objects.get_or_create(
        #     user=user,
        #     aplicacao=app,
        #     role=role
        # )
        # 
        # return Response({'status': 'Role assigned'})
        return Response({'message': 'Role assignment example'})
