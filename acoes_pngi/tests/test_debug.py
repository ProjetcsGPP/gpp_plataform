# acoes_pngi/tests/test_debug.py

from django.test import TransactionTestCase
from django.db import connection
from accounts.models import User, Aplicacao, Role, UserRole

class DebugDatabaseTest(TransactionTestCase):
    """Teste especial para debugar criação de dados"""
    
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
        
        # 2. Criar aplicação
        print("\n📦 CRIANDO APLICAÇÃO...")
        app = Aplicacao.objects.create(
            codigointerno='ACOESPNGI',
            nomeaplicacao='Ações PNGI',
            base_url='http://localhost:8000/acoes-pngi',
            isshowinportal=True
        )
        print(f"   ✅ Aplicação criada: ID={app.idaplicacao}")
        
        # 3. Criar role
        print("\n👤 CRIANDO ROLE...")
        role = Role.objects.create(
            nomeperfil='Gestor PNGI',
            codigoperfil='GESTORPNGI',
            aplicacao=app
        )
        print(f"   ✅ Role criada: ID={role.id}")
        
        # 4. Criar usuário
        print("\n🧑 CRIANDO USUÁRIO...")
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        print(f"   ✅ Usuário criado:")
        print(f"      - ID: {user.id}")
        print(f"      - Email: {user.email}")
        print(f"      - Nome: {user.name}")
        print(f"      - Status: {user.idstatususuario}")
        print(f"      - Tipo: {user.idtipousuario}")
        print(f"      - Classificação: {user.idclassificacaousuario}")
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
        print(f"   Usuários: {User.objects.count()}")
        print(f"   Aplicações: {Aplicacao.objects.count()}")
        print(f"   Roles: {Role.objects.count()}")
        print(f"   UserRoles: {UserRole.objects.count()}")
        
        # 7. Mostrar SQL executado
        print("\n🗄️ QUERIES SQL EXECUTADAS:")
        for i, query in enumerate(connection.queries[-10:], 1):
            print(f"\n   Query {i}:")
            print(f"   {query['sql'][:200]}...")
            print(f"   Tempo: {query['time']}s")
        
        print("\n" + "="*70)
        print("✅ INSPEÇÃO CONCLUÍDA")
        print("="*70 + "\n")
        
        # Assertions para o teste passar
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, 'test@example.com')
