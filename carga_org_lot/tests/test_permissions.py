"""
Testes de permissões de Carga Org/Lot.
"""

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from accounts.models import User, Aplicacao, Role, UserRole
from carga_org_lot.permissions import IsCargaOrgLotUser


class IsCargaOrgLotUserPermissionTest(TestCase):
    """Testes da permissão IsCargaOrgLotUser"""
    
    @classmethod
    def setUpTestData(cls):
        """Cria dados de teste"""
        cls.app = Aplicacao.objects.create(
            codigointerno='CARGA_ORG_LOT',
            nomeaplicacao='Carga Org/Lot',
            baseurl='http://localhost:8000/carga_org_lot/',
            isshowinportal=True
        )
        
        cls.role = Role.objects.create(
            nomeperfil='Gestor Carga',
            codigoperfil='GESTOR_CARGA',
            aplicacao=cls.app
        )
        
        cls.user_with_permission = User.objects.create_user(
            email='gestor@example.com',
            name='Gestor User',
            password='testpass123'
        )
        
        UserRole.objects.create(
            user=cls.user_with_permission,
            role=cls.role,
            aplicacao=cls.app
        )
        
        cls.user_without_permission = User.objects.create_user(
            email='user@example.com',
            name='Regular User',
            password='testpass123'
        )
    
    def setUp(self):
        """Configura factory"""
        self.factory = APIRequestFactory()
        self.permission = IsCargaOrgLotUser()
    
    def test_permission_granted_with_role(self):
        """Testa permissão concedida"""
        request = self.factory.get('/api/v1/carga/')
        request.user = self.user_with_permission
        
        request.app_context = {
            'code': 'CARGA_ORG_LOT',
            'instance': self.app,
            'name': 'Carga Org/Lot'
        }
        
        has_permission = self.permission.has_permission(request, None)
        self.assertTrue(has_permission)
