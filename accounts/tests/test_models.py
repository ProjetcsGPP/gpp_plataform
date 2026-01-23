"""
Testes dos modelos de Accounts.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import User, Aplicacao, Role, UserRole, Attribute


class UserModelTest(TestCase):
    """Testes do modelo User"""
    
    def test_create_user(self):
        """Testa criação de usuário"""
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.name, 'Test User')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
    
    def test_create_superuser(self):
        """Testa criação de superusuário"""
        admin = User.objects.create_superuser(
            email='admin@example.com',
            name='Admin User',
            password='adminpass123'
        )
        
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
    
    def test_email_normalization(self):
        """Testa normalização de email"""
        user = User.objects.create_user(
            email='TEST@EXAMPLE.COM',
            name='Test User',
            password='testpass123'
        )
        
        self.assertEqual(user.email, 'test@example.com')
    
    def test_user_str(self):
        """Testa string representation"""
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        
        self.assertEqual(str(user), 'Test User')


class AplicacaoModelTest(TestCase):
    """Testes do modelo Aplicacao"""
    
    def test_create_aplicacao(self):
        """Testa criação de aplicação"""
        app = Aplicacao.objects.create(
            codigointerno='TEST_APP',
            nomeaplicacao='Test Application',
            baseurl='http://localhost:8000/test/',
            isshowinportal=True
        )
        
        self.assertEqual(app.codigointerno, 'TEST_APP')
        self.assertEqual(app.nomeaplicacao, 'Test Application')
        self.assertTrue(app.isshowinportal)
    
    def test_unique_codigo_interno(self):
        """Testa unicidade do código interno"""
        Aplicacao.objects.create(
            codigointerno='TEST_APP',
            nomeaplicacao='First App',
            baseurl='http://localhost:8000/first/',
            isshowinportal=True
        )
        
        with self.assertRaises(Exception):
            Aplicacao.objects.create(
                codigointerno='TEST_APP',
                nomeaplicacao='Second App',
                baseurl='http://localhost:8000/second/',
                isshowinportal=True
            )


class RoleModelTest(TestCase):
    """Testes do modelo Role"""
    
    @classmethod
    def setUpTestData(cls):
        """Cria aplicação de teste"""
        cls.app = Aplicacao.objects.create(
            codigointerno='TEST_APP',
            nomeaplicacao='Test Application',
            baseurl='http://localhost:8000/test/',
            isshowinportal=True
        )
    
    def test_create_role(self):
        """Testa criação de role"""
        role = Role.objects.create(
            nomeperfil='Gestor',
            codigoperfil='GESTOR',
            aplicacao=self.app
        )
        
        self.assertEqual(role.nomeperfil, 'Gestor')
        self.assertEqual(role.codigoperfil, 'GESTOR')
        self.assertEqual(role.aplicacao, self.app)


class UserRoleModelTest(TestCase):
    """Testes do modelo UserRole"""
    
    @classmethod
    def setUpTestData(cls):
        """Cria dados de teste"""
        cls.app = Aplicacao.objects.create(
            codigointerno='TEST_APP',
            nomeaplicacao='Test Application',
            baseurl='http://localhost:8000/test/',
            isshowinportal=True
        )
        
        cls.role = Role.objects.create(
            nomeperfil='Gestor',
            codigoperfil='GESTOR',
            aplicacao=cls.app
        )
        
        cls.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
    
    def test_create_user_role(self):
        """Testa atribuição de role a usuário"""
        user_role = UserRole.objects.create(
            user=self.user,
            role=self.role,
            aplicacao=self.app
        )
        
        self.assertEqual(user_role.user, self.user)
        self.assertEqual(user_role.role, self.role)
        self.assertEqual(user_role.aplicacao, self.app)


class AttributeModelTest(TestCase):
    """Testes do modelo Attribute"""
    
    @classmethod
    def setUpTestData(cls):
        """Cria dados de teste"""
        cls.app = Aplicacao.objects.create(
            codigointerno='TEST_APP',
            nomeaplicacao='Test Application',
            baseurl='http://localhost:8000/test/',
            isshowinportal=True
        )
        
        cls.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
    
    def test_create_attribute(self):
        """Testa criação de atributo"""
        attr = Attribute.objects.create(
            user=self.user,
            aplicacao=self.app,
            key='max_uploads',
            value='10'
        )
        
        self.assertEqual(attr.user, self.user)
        self.assertEqual(attr.aplicacao, self.app)
        self.assertEqual(attr.key, 'max_uploads')
        self.assertEqual(attr.value, '10')
