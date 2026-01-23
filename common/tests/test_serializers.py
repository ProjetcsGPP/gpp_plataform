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
        # Aplicações
        cls.app_acoes = Aplicacao.objects.create(
            codigointerno='ACOES_PNGI',
            nomeaplicacao='Gestão de Ações PNGI',
            baseurl='http://localhost:8000/acoes-pngi/',
            isshowinportal=True
        )
        
        cls.app_carga = Aplicacao.objects.create(
            codigointerno='CARGA_ORG_LOT',
            nomeaplicacao='Carga Org/Lot',
            baseurl='http://localhost:8000/carga_org_lot/',
            isshowinportal=True
        )
        
        # Roles
        cls.role_gestor_acoes = Role.objects.create(
            nomeperfil='Gestor PNGI',
            codigoperfil='GESTOR_PNGI',
            aplicacao=cls.app_acoes
        )
        
        cls.role_gestor_carga = Role.objects.create(
            nomeperfil='Gestor Carga',
            codigoperfil='GESTOR_CARGA',
            aplicacao=cls.app_carga
        )
        
        # Usuário
        cls.user = User.objects.create_user(
            email='multiapp@example.com',
            name='Multi App User',
            password='testpass123'
        )
        
        # UserRoles
        UserRole.objects.create(
            user=cls.user,
            role=cls.role_gestor_acoes,
            aplicacao=cls.app_acoes
        )
        
        UserRole.objects.create(
            user=cls.user,
            role=cls.role_gestor_carga,
            aplicacao=cls.app_carga
        )
        
        # Atributos
        Attribute.objects.create(
            user=cls.user,
            aplicacao=cls.app_acoes,
            key='can_upload',
            value='true'
        )
        
        Attribute.objects.create(
            user=cls.user,
            aplicacao=cls.app_carga,
            key='max_patriarcas',
            value='10'
        )
    
    def setUp(self):
        """Configura factory e middleware"""
        self.factory = RequestFactory()
        self.middleware = AppContextMiddleware(dummy_get_response)
    
    def test_serializer_filters_by_acoes_pngi(self):
        """Testa que serializer filtra roles/attrs por ACOES_PNGI"""
        # Cria request para Ações PNGI
        request = self.factory.get('/api/v1/acoes_pngi/users/')
        self.middleware(request)
        
        # Serializa usuário
        serializer = UserSerializer(self.user, context={'request': request})
        data = serializer.data
        
        # Verifica roles
        self.assertEqual(len(data['roles']), 1)
        self.assertEqual(data['roles'][0]['code'], 'GESTOR_PNGI')
        
        # Verifica atributos
        self.assertIn('can_upload', data['attributes'])
        self.assertEqual(data['attributes']['can_upload'], 'true')
        self.assertNotIn('max_patriarcas', data['attributes'])
    
    def test_serializer_filters_by_carga_org_lot(self):
        """Testa que serializer filtra roles/attrs por CARGA_ORG_LOT"""
        # Cria request para Carga Org/Lot
        request = self.factory.get('/api/v1/carga/')
        self.middleware(request)
        
        # Serializa usuário
        serializer = UserSerializer(self.user, context={'request': request})
        data = serializer.data
        
        # Verifica roles
        self.assertEqual(len(data['roles']), 1)
        self.assertEqual(data['roles'][0]['code'], 'GESTOR_CARGA')
        
        # Verifica atributos
        self.assertIn('max_patriarcas', data['attributes'])
        self.assertEqual(data['attributes']['max_patriarcas'], '10')
        self.assertNotIn('can_upload', data['attributes'])
    
    def test_serializer_fallback_to_manual_app_code(self):
        """Testa fallback para app_code manual quando middleware não disponível"""
        # Request sem passar pelo middleware
        request = self.factory.get('/test/')
        
        # Passa app_code manualmente no context
        serializer = UserSerializer(
            self.user,
            context={'request': request, 'app_code': 'ACOES_PNGI'}
        )
        data = serializer.data
        
        # Deve usar o app_code manual
        self.assertEqual(len(data['roles']), 1)
        self.assertEqual(data['roles'][0]['code'], 'GESTOR_PNGI')
    
    def test_create_serializer_uses_app_context(self):
        """Testa que UserCreateSerializer usa app_context"""
        # Cria request para Ações PNGI
        request = self.factory.post('/api/v1/acoes_pngi/users/sync/')
        self.middleware(request)
        
        # Dados do novo usuário
        data = {
            'email': 'novo@example.com',
            'name': 'Novo Usuário',
            'roles': ['GESTOR_PNGI'],
            'attributes': {'test_attr': 'test_value'}
        }
        
        # Cria usuário
        serializer = UserCreateSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        
        # Verifica que foi criado com roles/attrs da aplicação correta
        user_role = UserRole.objects.filter(
            user=user,
            aplicacao=self.app_acoes
        ).first()
        
        self.assertIsNotNone(user_role)
        self.assertEqual(user_role.role.codigoperfil, 'GESTOR_PNGI')
        
        # Verifica atributo
        attr = Attribute.objects.filter(
            user=user,
            aplicacao=self.app_acoes,
            key='test_attr'
        ).first()
        
        self.assertIsNotNone(attr)
        self.assertEqual(attr.value, 'test_value')
