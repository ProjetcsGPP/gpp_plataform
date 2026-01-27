"""
Testes dos serializers com app_context.
"""

from django.test import TestCase, RequestFactory
from accounts.models import User, Aplicacao, Role, UserRole, Attribute
from common.serializers import UserSerializer, UserCreateSerializer
from common.middleware.app_context import AppContextMiddleware


def dummy_get_response(request):
    from django.http import HttpResponse
    return HttpResponse("OK")


class UserSerializerWithAppContextTest(TestCase):
    """
    Testes do UserSerializer usando app_context do middleware.
    """
    
@classmethod
def setUpTestData(cls):
    """Cria dados de teste"""
    
    Aplicacao.objects.filter(codigointerno__in=['ACOES_PNGI', 'PORTAL', 'CARGA_ORG_LOT']).delete()
    
    
    cls.app_acoes, _ = Aplicacao.objects.get_or_create(
        codigointerno='ACOES_PNGI',
        defaults={
            'nomeaplicacao': 'Gestão de Ações PNGI',
            'base_url': 'http://localhost:8000/acoes-pngi/',
            'isshowinportal': True
        }
    )
    
    cls.app_carga, _ = Aplicacao.objects.get_or_create(
        codigointerno='CARGA_ORG_LOT',
        defaults={
            'nomeaplicacao': 'Carga Organograma/Lotação',
            'base_url': 'http://localhost:8000/carga_org_lot/',
            'isshowinportal': True
        }
    )
    
    # Roles - CORRIGIDO
    cls.role_gestor_acoes, _ = Role.objects.get_or_create(
        nomeperfil='Gestor PNGI',
        codigoperfil='GESTOR_PNGI',
        aplicacao_id=cls.app_acoes.idaplicacao  # ← CORRIGIDO: app_acoes em vez de app_carga
    )

    cls.role_gestor_carga, _ = Role.objects.get_or_create(
        nomeperfil='Gestor Carga',
        codigoperfil='GESTOR_CARGA',
        aplicacao_id=cls.app_carga.idaplicacao
    )
    
    # Usuário
    cls.user = User.objects.create_user(
        email='multiapp@example.com',
        name='Multi App User',
        password='testpass123'
    )
    
    # UserRoles - CORRIGIDO
    UserRole.objects.create(
        user=cls.user,
        role=cls.role_gestor_acoes,
        aplicacao_id=cls.app_acoes.idaplicacao  # ← CORRIGIDO: app_acoes em vez de app_carga
    )
    
    UserRole.objects.create(
        user=cls.user,
        role=cls.role_gestor_carga,
        aplicacao_id=cls.app_carga.idaplicacao
    )
    
    # Atributos - CORRIGIDO
    Attribute.objects.create(
        user=cls.user,
        aplicacao_id=cls.app_acoes.idaplicacao,  # ← CORRIGIDO: app_acoes
        key='can_upload',
        value='true'
    )
    
    Attribute.objects.create(
        user=cls.user,
        aplicacao_id=cls.app_carga.idaplicacao,
        key='max_patriarcas',
        value='10'
    )
