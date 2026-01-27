# acoes_pngi/tests/test_debug.py

from django.test import TestCase
from accounts.models import User, Aplicacao, Role, UserRole


class DebugDatabaseTest(TestCase):
    """Teste especial para debugar criação de dados"""
    
    databases = {'default'}
    
    def test_inspect_user_creation(self):
        """Inspeciona criação de usuário passo a passo"""
        
        print("\n" + "="*70)
        print("🔍 INICIANDO INSPEÇÃO DE CRIAÇÃO DE USUÁRIO")
        print("="*70)
        
        # 1. Verificar estado inicial
        print("\n📊 ESTADO INICIAL:")
        print(f"   Usuários: {User.objects.count()}")
        print(f"   Aplicações: {Aplicacao.objects.count()}")
        print(f"   Roles: {Role.objects.count()}")
        
        # 2. Criar aplicação usando get_or_create
        print("\n📦 CRIANDO APLICAÇÃO...")
        app, created = Aplicacao.objects.get_or_create(
            codigointerno='ACOESPNGI_TEST',
            defaults={
                'nomeaplicacao': 'Ações PNGI Test',
                'isshowinportal': True
            }
        )
        print(f"   ✅ Aplicação {'criada' if created else 'já existe'}: ID={app.idaplicacao}")
        
        # 3. Criar role
        print("\n👤 CRIANDO ROLE...")
        role, created = Role.objects.get_or_create(
            codigoperfil='GESTORPNGI_TEST',
            aplicacao=app,
            defaults={'nomeperfil': 'Gestor PNGI Test'}
        )
        print(f"   ✅ Role {'criada' if created else 'já existe'}: ID={role.id}")
        
        # 4. Criar usuário
        print("\n🧑 CRIANDO USUÁRIO...")
        user = User.objects.create_user(
            email='test_debug@example.com',
            name='Test User Debug',
            password='testpass123'
        )
        print(f"   ✅ Usuário criado:")
        print(f"      - ID: {user.id}")
        print(f"      - Email: {user.email}")
        print(f"      - Nome: {user.name}")
        print(f"      - Active: {user.is_active}")
        print(f"      - Staff: {user.is_staff}")
        
        # 5. Associar role ao usuário
        print("\n🔗 ASSOCIANDO ROLE AO USUÁRIO...")
        user_role = UserRole.objects.create(
            user=user,
            aplicacao=app,
            role=role
        )
        print(f"   ✅ UserRole criado: ID={user_role.id}")
        
        # 6. Verificar estado final
        print("\n📊 ESTADO FINAL:")
        print(f"   Usuários criados neste teste: 1")
        print(f"   UserRoles criados neste teste: {UserRole.objects.filter(user=user).count()}")
        
        print("\n" + "="*70)
        print("✅ INSPEÇÃO CONCLUÍDA")
        print("="*70 + "\n")
        
        # Assertions para o teste passar
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test_debug@example.com')
        self.assertEqual(UserRole.objects.filter(user=user).count(), 1)
