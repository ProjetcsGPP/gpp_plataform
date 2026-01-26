# carga_org_lot/tests/test_permissions.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory

from accounts.models import UserRole
from carga_org_lot.permissions import IsCargaOrgLotUser
from . import BaseDataTestCase

User = get_user_model()


class IsCargaOrgLotUserPermissionTest(BaseDataTestCase):
    """Testes para a permissão IsCargaOrgLotUser"""
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        # A aplicação e role já existem via BaseDataTestCase
        # Só precisamos criar usuários e associar roles
        
        # Criar usuário com permissão
        cls.user_with_permission = User.objects.create_user(
            name='user_carga',
            email='user@example.com',
            password='testpass123'
        )
        
        # Associar role ao usuário (usando objetos que já existem)
        UserRole.objects.create(
            user=cls.user_with_permission,
            role=cls.role_gestor,  # Vem do BaseDataTestCase
            aplicacao=cls.aplicacao_carga  # Vem do BaseDataTestCase
        )
        
        # Criar usuário sem permissão
        cls.user_without_permission = User.objects.create_user(
            name='user_no_perm',
            email='noperm@example.com',
            password='testpass123'
        )
        
        cls.factory = APIRequestFactory()
        cls.permission = IsCargaOrgLotUser()

    def test_user_with_permission_has_access(self):
        """Usuário com role GESTOR_CARGA deve ter acesso"""
        request = self.factory.get('/')
        request.user = self.user_with_permission
        
        self.assertTrue(
            self.permission.has_permission(request, None),
            "Usuário com permissão deveria ter acesso"
        )

    def test_user_without_permission_denied(self):
        """Usuário sem role GESTOR_CARGA não deve ter acesso"""
        request = self.factory.get('/')
        request.user = self.user_without_permission
        
        self.assertFalse(
            self.permission.has_permission(request, None),
            "Usuário sem permissão não deveria ter acesso"
        )

    def test_unauthenticated_user_denied(self):
        """Usuário não autenticado não deve ter acesso"""
        request = self.factory.get('/')
        request.user = AnonymousUser()
        
        self.assertFalse(
            self.permission.has_permission(request, None),
            "Usuário anônimo não deveria ter acesso"
        )
