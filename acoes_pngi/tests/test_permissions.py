"""
Testes para o sistema automatizado de permissões do acoes_pngi.
"""
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.core.cache import cache

from accounts.models import Aplicacao, Role, RolePermission, UserRole
from acoes_pngi.context_processors import acoes_permissions
from acoes_pngi.utils.permissions import (
    get_user_app_permissions,
    user_can_manage_model,
    get_model_permissions,
    clear_user_permissions_cache,
)

User = get_user_model()


class AcoesPermissionsTestCase(TestCase):
    """Testes para o sistema de permissões automatizado."""

    def setUp(self):
        """Configurar ambiente de teste."""
        print("\n" + "="*80)
        print("🛠️  Configurando ambiente de teste...")
        print("="*80)
        
        # Limpar cache antes de cada teste
        cache.clear()
        print("✅ Cache limpo")
        
        # Usar get_or_create para evitar conflitos com dados do __init__.py
        self.app, created = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        print(f"✅ Aplicação: {self.app.nomeaplicacao} ({'criada' if created else 'existente'})")
        
        # Criar roles com o campo correto: aplicacao (não idaplicacao)
        self.admin_role, created = Role.objects.get_or_create(
            nomeperfil='Admin PNGI',
            codigoperfil='ADMIN_PNGI',
            defaults={'aplicacao': self.app}
        )
        print(f"✅ Role Admin: {self.admin_role.nomeperfil} ({'criada' if created else 'existente'})")
        
        self.viewer_role, created = Role.objects.get_or_create(
            nomeperfil='Viewer PNGI',
            codigoperfil='VIEWER_PNGI',
            defaults={'aplicacao': self.app}
        )
        print(f"✅ Role Viewer: {self.viewer_role.nomeperfil} ({'criada' if created else 'existente'})")
        
        # Criar usuários (sem username, só email)
        self.admin_user = User.objects.create_user(
            email='admin@pngi.gov.br',
            password='admin123',
            name='Admin PNGI Test'
        )
        print(f"✅ Usuário Admin criado: {self.admin_user.email}")
        
        self.viewer_user = User.objects.create_user(
            email='viewer@pngi.gov.br',
            password='viewer123',
            name='Viewer PNGI Test'
        )
        print(f"✅ Usuário Viewer criado: {self.viewer_user.email}")
        
        # Criar UserRole para vincular usuários aos roles
        UserRole.objects.create(
            user=self.admin_user,
            aplicacao=self.app,
            role=self.admin_role
        )
        print(f"   → {self.admin_user.name} vinculado ao role {self.admin_role.nomeperfil}")
        
        UserRole.objects.create(
            user=self.viewer_user,
            aplicacao=self.app,
            role=self.viewer_role
        )
        print(f"   → {self.viewer_user.name} vinculado ao role {self.viewer_role.nomeperfil}")
        
        # Criar permissões para o app acoes_pngi
        from acoes_pngi.models import Eixo, SituacaoAcao
        
        print("\n🔑 Configurando permissões...")
        
        # Obter content types
        eixo_ct = ContentType.objects.get_for_model(Eixo)
        situacao_ct = ContentType.objects.get_for_model(SituacaoAcao)
        
        # Permissões para Eixo
        self.perm_add_eixo = Permission.objects.get(
            content_type=eixo_ct,
            codename='add_eixo'
        )
        self.perm_change_eixo = Permission.objects.get(
            content_type=eixo_ct,
            codename='change_eixo'
        )
        self.perm_delete_eixo = Permission.objects.get(
            content_type=eixo_ct,
            codename='delete_eixo'
        )
        self.perm_view_eixo = Permission.objects.get(
            content_type=eixo_ct,
            codename='view_eixo'
        )
        
        # Permissões para SituacaoAcao
        self.perm_view_situacao = Permission.objects.get(
            content_type=situacao_ct,
            codename='view_situacaoacao'
        )
        
        # Associar todas as permissões ao Admin
        print(f"\n   Admin Role ({self.admin_role.nomeperfil}):")
        for perm in [self.perm_add_eixo, self.perm_change_eixo, self.perm_delete_eixo, self.perm_view_eixo]:
            RolePermission.objects.get_or_create(
                role=self.admin_role,
                permission=perm
            )
            print(f"      ✅ {perm.codename}")
        
        # Associar apenas view ao Viewer
        print(f"\n   Viewer Role ({self.viewer_role.nomeperfil}):")
        for perm in [self.perm_view_eixo, self.perm_view_situacao]:
            RolePermission.objects.get_or_create(
                role=self.viewer_role,
                permission=perm
            )
            print(f"      ✅ {perm.codename}")
        
        # Factory para criar requests
        self.factory = RequestFactory()
        print("\n✅ Ambiente configurado com sucesso!")
    
    def tearDown(self):
        """Limpar cache após cada teste."""
        cache.clear()
        print("🧹 Cache limpo após teste")
    
    def test_admin_has_all_permissions(self):
        """
        TESTE 1: Admin deve ter todas as permissões.
        """
        print("\n" + "="*80)
        print("🧪 TESTE 1: Verificando permissões do Admin")
        print("="*80)
        
        request = self.factory.get('/')
        request.user = self.admin_user
        print(f"👤 Usuário: {self.admin_user.name} ({self.admin_user.email})")
        print(f"🎭 Role: {self.admin_role.nomeperfil}")
        
        print("\n🔍 Executando context processor...")
        context = acoes_permissions(request)
        
        print("\n📊 Permissões retornadas pelo context:")
        permissions = {
            'can_add_eixo': context['can_add_eixo'],
            'can_change_eixo': context['can_change_eixo'],
            'can_delete_eixo': context['can_delete_eixo'],
            'can_view_eixo': context['can_view_eixo'],
            'can_manage_eixo': context['can_manage_eixo'],
        }
        
        for perm, value in permissions.items():
            icon = "✅" if value else "❌"
            print(f"   {icon} {perm}: {value}")
        
        print("\n✅ Asserting: Admin deve ter TODAS as permissões")
        self.assertTrue(context['can_add_eixo'])
        self.assertTrue(context['can_change_eixo'])
        self.assertTrue(context['can_delete_eixo'])
        self.assertTrue(context['can_view_eixo'])
        self.assertTrue(context['can_manage_eixo'])  # Agregada
        print("✅ TESTE PASSOU!")
    
    def test_viewer_has_limited_permissions(self):
        """
        TESTE 2: Viewer deve ter apenas permissão de visualização.
        """
        print("\n" + "="*80)
        print("👁️  TESTE 2: Verificando permissões do Viewer (limitadas)")
        print("="*80)
        
        request = self.factory.get('/')
        request.user = self.viewer_user
        print(f"👤 Usuário: {self.viewer_user.name} ({self.viewer_user.email})")
        print(f"🎭 Role: {self.viewer_role.nomeperfil}")
        
        print("\n🔍 Executando context processor...")
        context = acoes_permissions(request)
        
        print("\n📊 Permissões retornadas pelo context:")
        permissions = {
            'can_add_eixo': context['can_add_eixo'],
            'can_change_eixo': context['can_change_eixo'],
            'can_delete_eixo': context['can_delete_eixo'],
            'can_view_eixo': context['can_view_eixo'],
            'can_manage_eixo': context['can_manage_eixo'],
        }
        
        for perm, value in permissions.items():
            icon = "✅" if value else "❌"
            expected = "(esperado)" if perm == 'can_view_eixo' else "(esperado: False)"
            print(f"   {icon} {perm}: {value} {expected}")
        
        print("\n✅ Asserting: Viewer deve ter APENAS view")
        self.assertFalse(context['can_add_eixo'])
        self.assertFalse(context['can_change_eixo'])
        self.assertFalse(context['can_delete_eixo'])
        self.assertTrue(context['can_view_eixo'])
        self.assertFalse(context['can_manage_eixo'])  # Agregada
        print("✅ TESTE PASSOU!")
    
    def test_unauthenticated_user_no_permissions(self):
        """
        TESTE 3: Usuário não autenticado não deve ter permissões.
        """
        print("\n" + "="*80)
        print("🚫 TESTE 3: Verificando usuário não autenticado (sem permissões)")
        print("="*80)
        
        from django.contrib.auth.models import AnonymousUser
        
        request = self.factory.get('/')
        request.user = AnonymousUser()
        print("👤 Usuário: Anônimo (não autenticado)")
        
        print("\n🔍 Executando context processor...")
        context = acoes_permissions(request)
        
        print("\n📊 Permissões retornadas pelo context:")
        permissions = {
            'can_add_eixo': context['can_add_eixo'],
            'can_change_eixo': context['can_change_eixo'],
            'can_delete_eixo': context['can_delete_eixo'],
            'can_view_eixo': context['can_view_eixo'],
        }
        
        for perm, value in permissions.items():
            icon = "❌"
            print(f"   {icon} {perm}: {value} (esperado: False)")
        
        print("\n✅ Asserting: Anônimo não deve ter NENHUMA permissão")
        self.assertFalse(context['can_add_eixo'])
        self.assertFalse(context['can_change_eixo'])
        self.assertFalse(context['can_delete_eixo'])
        self.assertFalse(context['can_view_eixo'])
        print("✅ TESTE PASSOU!")
    
    def test_get_user_app_permissions(self):
        """
        TESTE 4: Testar função helper de permissões.
        """
        print("\n" + "="*80)
        print("🛠️  TESTE 4: Testando helper get_user_app_permissions()")
        print("="*80)
        
        print(f"👤 Usuário: {self.admin_user.name}")
        print("\n🔍 Chamando get_user_app_permissions()...")
        
        perms = get_user_app_permissions(self.admin_user)
        
        print(f"\n📊 Permissões retornadas (total: {len(perms)}):")
        expected_perms = ['add_eixo', 'change_eixo', 'delete_eixo', 'view_eixo']
        
        for perm in expected_perms:
            has_perm = perm in perms
            icon = "✅" if has_perm else "❌"
            print(f"   {icon} {perm}: {'presente' if has_perm else 'ausente'}")
        
        print("\n✅ Asserting: Admin deve ter permissões de eixo")
        self.assertIn('add_eixo', perms)
        self.assertIn('change_eixo', perms)
        self.assertIn('delete_eixo', perms)
        self.assertIn('view_eixo', perms)
        print("✅ TESTE PASSOU!")
    
    def test_user_can_manage_model(self):
        """
        TESTE 5: Testar verificação de gerenciamento de modelo.
        """
        print("\n" + "="*80)
        print("📊 TESTE 5: Testando user_can_manage_model()")
        print("="*80)
        
        print(f"\n👤 Admin: {self.admin_user.name}")
        print("🔍 Verificando se pode gerenciar 'eixo'...")
        admin_can_manage = user_can_manage_model(self.admin_user, 'eixo')
        icon = "✅" if admin_can_manage else "❌"
        print(f"   {icon} Admin pode gerenciar: {admin_can_manage}")
        
        print(f"\n👤 Viewer: {self.viewer_user.name}")
        print("🔍 Verificando se pode gerenciar 'eixo'...")
        viewer_can_manage = user_can_manage_model(self.viewer_user, 'eixo')
        icon = "❌"
        print(f"   {icon} Viewer pode gerenciar: {viewer_can_manage} (esperado: False)")
        
        print("\n✅ Asserting: Admin SIM, Viewer NÃO")
        self.assertTrue(admin_can_manage)
        self.assertFalse(viewer_can_manage)
        print("✅ TESTE PASSOU!")
    
    def test_get_model_permissions(self):
        """
        TESTE 6: Testar obtenção de permissões de modelo.
        """
        print("\n" + "="*80)
        print("📊 TESTE 6: Testando get_model_permissions()")
        print("="*80)
        
        print(f"\n👤 Admin: {self.admin_user.name}")
        print("🔍 Obtendo permissões do modelo 'eixo'...")
        perms = get_model_permissions(self.admin_user, 'eixo')
        
        print("\n📊 Permissões do Admin:")
        for key, value in perms.items():
            icon = "✅" if value else "❌"
            print(f"   {icon} {key}: {value}")
        
        print(f"\n👤 Viewer: {self.viewer_user.name}")
        print("🔍 Obtendo permissões do modelo 'eixo'...")
        viewer_perms = get_model_permissions(self.viewer_user, 'eixo')
        
        print("\n📊 Permissões do Viewer:")
        for key, value in viewer_perms.items():
            icon = "✅" if value else "❌"
            expected = "(esperado)" if key == 'can_view' else "(esperado: False)"
            print(f"   {icon} {key}: {value} {expected}")
        
        print("\n✅ Asserting: Admin tem todas, Viewer só view")
        self.assertTrue(perms['can_add'])
        self.assertTrue(perms['can_change'])
        self.assertTrue(perms['can_delete'])
        self.assertTrue(perms['can_view'])
        
        self.assertFalse(viewer_perms['can_add'])
        self.assertTrue(viewer_perms['can_view'])
        print("✅ TESTE PASSOU!")
    
    def test_permissions_caching(self):
        """
        TESTE 7: Testar cache de permissões.
        """
        print("\n" + "="*80)
        print("🗄️  TESTE 7: Testando cache de permissões")
        print("="*80)
        
        print(f"👤 Usuário: {self.admin_user.name}")
        
        print("\n1️⃣ Primeira chamada (deve buscar do BD e cachear)...")
        perms1 = get_user_app_permissions(self.admin_user)
        print(f"   ✅ Permissões obtidas: {len(perms1)} permissões")
        
        print("\n2️⃣ Segunda chamada (deve vir do cache)...")
        perms2 = get_user_app_permissions(self.admin_user)
        print(f"   ✅ Permissões obtidas: {len(perms2)} permissões")
        
        print("\n🔍 Verificando cache...")
        cache_key = f'user_permissions_{self.admin_user.id}'
        cached_perms = cache.get(cache_key)
        
        if cached_perms:
            print(f"   ✅ Cache ATIVO: {len(cached_perms)} permissões em cache")
        else:
            print("   ❌ Cache VAZIO (erro!)")
        
        print("\n✅ Asserting: Permissões iguais e cache ativo")
        self.assertEqual(perms1, perms2)
        self.assertIsNotNone(cached_perms)
        print("✅ TESTE PASSOU!")
    
    def test_clear_permissions_cache(self):
        """
        TESTE 8: Testar limpeza de cache.
        """
        print("\n" + "="*80)
        print("🧹 TESTE 8: Testando limpeza de cache")
        print("="*80)
        
        print(f"👤 Usuário: {self.admin_user.name}")
        
        print("\n1️⃣ Cacheando permissões...")
        get_user_app_permissions(self.admin_user)
        
        cache_key = f'user_permissions_{self.admin_user.id}'
        cached_before = cache.get(cache_key)
        
        if cached_before:
            print(f"   ✅ Cache ATIVO: {len(cached_before)} permissões")
        
        print("\n2️⃣ Limpando cache...")
        clear_user_permissions_cache(self.admin_user)
        print("   🧹 clear_user_permissions_cache() executado")
        
        print("\n3️⃣ Verificando se cache foi limpo...")
        cached_after = cache.get(cache_key)
        
        if cached_after is None:
            print("   ✅ Cache LIMPO com sucesso!")
        else:
            print(f"   ❌ Cache ainda existe: {cached_after}")
        
        print("\n✅ Asserting: Cache antes existia, depois não")
        self.assertIsNotNone(cached_before)
        self.assertIsNone(cached_after)
        print("✅ TESTE PASSOU!")
        print("\n" + "="*80 + "\n")
