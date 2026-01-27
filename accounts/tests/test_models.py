# accounts/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from ..models import Aplicacao, Role, UserRole, Attribute

User = get_user_model()


class UserModelTest(TestCase):
    """Testes para modelo User"""
    
    databases = {'default'}
    
    def test_create_user(self):
        """Testa criação de usuário"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Testa criação de superusuário"""
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
    
    def test_email_unique(self):
        """Testa que email deve ser único"""
        User.objects.create_user(
            email='test@example.com',
            password='pass1'
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='test@example.com',
                password='pass2'
            )
    
    def test_user_str(self):
        """Testa representação string"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass'
        )
        self.assertEqual(str(user), 'test@example.com')


class AplicacaoModelTest(TestCase):
    """Testes para modelo Aplicacao"""
    
    databases = {'default'}
    
    def test_create_aplicacao(self):
        """Testa criação de aplicação"""
        app = Aplicacao.objects.create(
            codigointerno='TEST_APP',
            nomeaplicacao='Aplicação de Teste',
            isshowinportal=True
        )
        self.assertEqual(app.codigointerno, 'TEST_APP')
        self.assertEqual(app.nomeaplicacao, 'Aplicação de Teste')
        self.assertTrue(app.isshowinportal)
    
    def test_codigo_unique(self):
        """Testa que codigointerno deve ser único"""
        Aplicacao.objects.create(
            codigointerno='TEST',
            nomeaplicacao='App 1'
        )
        with self.assertRaises(IntegrityError):
            Aplicacao.objects.create(
                codigointerno='TEST',
                nomeaplicacao='App 2'
            )
    
    def test_aplicacao_str(self):
        """Testa representação string"""
        app = Aplicacao.objects.create(
            codigointerno='MY_APP',
            nomeaplicacao='Minha Aplicação'
        )
        self.assertEqual(str(app), 'MY_APP - Minha Aplicação')


class RoleModelTest(TestCase):
    """Testes para modelo Role"""
    
    databases = {'default'}
    
    def setUp(self):
        self.app = Aplicacao.objects.create(
            codigointerno='TEST_APP',
            nomeaplicacao='Test'
        )
    
    def test_create_role(self):
        """Testa criação de role"""
        role = Role.objects.create(
            aplicacao=self.app,
            nomeperfil='Administrador',
            codigoperfil='ADMIN'
        )
        self.assertEqual(role.nomeperfil, 'Administrador')
        self.assertEqual(role.codigoperfil, 'ADMIN')
        self.assertEqual(role.aplicacao, self.app)
    
    def test_role_unique_per_app(self):
        """Testa que role deve ser única por aplicação"""
        Role.objects.create(
            aplicacao=self.app,
            nomeperfil='Admin',
            codigoperfil='ADMIN'
        )
        with self.assertRaises(IntegrityError):
            Role.objects.create(
                aplicacao=self.app,
                nomeperfil='Administrador',
                codigoperfil='ADMIN'
            )


class UserRoleModelTest(TestCase):
    """Testes para modelo UserRole (RBAC)"""
    
    databases = {'default'}
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass'
        )
        self.app = Aplicacao.objects.create(
            codigointerno='TEST_APP',
            nomeaplicacao='Test'
        )
        self.role = Role.objects.create(
            aplicacao=self.app,
            nomeperfil='Gestor',
            codigoperfil='GESTOR'
        )
    
    def test_assign_role_to_user(self):
        """Testa atribuição de role a usuário"""
        user_role = UserRole.objects.create(
            user=self.user,
            aplicacao=self.app,
            role=self.role
        )
        self.assertEqual(user_role.user, self.user)
        self.assertEqual(user_role.aplicacao, self.app)
        self.assertEqual(user_role.role, self.role)
    
    def test_user_role_unique(self):
        """Testa que combinação user+app+role deve ser única"""
        UserRole.objects.create(
            user=self.user,
            aplicacao=self.app,
            role=self.role
        )
        with self.assertRaises(IntegrityError):
            UserRole.objects.create(
                user=self.user,
                aplicacao=self.app,
                role=self.role
            )


class AttributeModelTest(TestCase):
    """Testes para modelo Attribute (ABAC)"""
    
    databases = {'default'}
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass'
        )
        self.app = Aplicacao.objects.create(
            codigointerno='TEST_APP',
            nomeaplicacao='Test'
        )
    
    def test_create_attribute(self):
        """Testa criação de atributo"""
        attr = Attribute.objects.create(
            user=self.user,
            aplicacao=self.app,
            key='can_upload',
            value='true'
        )
        self.assertEqual(attr.user, self.user)
        self.assertEqual(attr.aplicacao, self.app)
        self.assertEqual(attr.key, 'can_upload')
        self.assertEqual(attr.value, 'true')
    
    def test_attribute_unique(self):
        """Testa que combinação user+app+key deve ser única"""
        Attribute.objects.create(
            user=self.user,
            aplicacao=self.app,
            key='can_upload',
            value='true'
        )
        with self.assertRaises(IntegrityError):
            Attribute.objects.create(
                user=self.user,
                aplicacao=self.app,
                key='can_upload',
                value='false'
            )
