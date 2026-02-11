"""acoes_pngi/tests/test_web_views_complete.py

Testes completos para Web Views - Ações PNGI

Cobre todas as linhas não testadas de web_views.py:
- Login completo com validações
- Dashboard com estatísticas
- CRUD de Eixos com validações
- CRUD de Vigências com validações de data
- Tratamento de erros e edge cases
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from datetime import date, timedelta

from accounts.models import Aplicacao, Role, UserRole
from ..models import Eixo, SituacaoAcao, VigenciaPNGI

User = get_user_model()


class LoginWebViewTests(TestCase):
    """Testes completos do login do Ações PNGI"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup inicial"""
        self.client = Client()
        
        # Criar aplicação (usar get_or_create para evitar IntegrityError)
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        # Criar role (usar get_or_create para evitar IntegrityError)
        self.role, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='GESTOR_PNGI',
            defaults={'nomeperfil': 'Gestor Ações PNGI'}
        )
        
        # Criar usuário ativo com acesso
        self.user = User.objects.create_user(
            email='gestor@seger.es.gov.br',
            name='Gestor Test',
            password='testpass123',
            is_active=True
        )
        UserRole.objects.create(
            user=self.user,
            aplicacao=self.app,
            role=self.role
        )
        
        # Criar usuário inativo
        self.user_inactive = User.objects.create_user(
            email='inactive@seger.es.gov.br',
            name='User Inactive',
            password='testpass123',
            is_active=False
        )
        
        # Criar usuário sem acesso à aplicação
        self.user_no_access = User.objects.create_user(
            email='noaccess@seger.es.gov.br',
            name='User No Access',
            password='testpass123',
            is_active=True
        )
    
    def test_login_get_renders_template(self):
        """GET /login renderiza template de login"""
        response = self.client.get('/acoes-pngi/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acoes_pngi/login.html')
    
    def test_login_authenticated_user_with_access_redirects_to_dashboard(self):
        """Usuário já autenticado com acesso é redirecionado ao dashboard"""
        self.client.login(email=self.user.email, password='testpass123')
        
        response = self.client.get('/acoes-pngi/login/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.url)
    
    def test_login_authenticated_user_without_access_logs_out(self):
        """Usuário autenticado SEM acesso é deslogado"""
        self.client.login(email=self.user_no_access.email, password='testpass123')
        
        response = self.client.get('/acoes-pngi/login/')
        
        # Deve fazer logout e exibir mensagem de erro
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('não tem permissão' in str(m) for m in messages))
    
    def test_login_post_empty_fields(self):
        """POST com campos vazios exibe erro"""
        response = self.client.post('/acoes-pngi/login/', {
            'email': '',
            'password': ''
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('preencha todos os campos' in str(m).lower() for m in messages))
    
    def test_login_post_user_not_found(self):
        """POST com email não cadastrado exibe erro"""
        response = self.client.post('/acoes-pngi/login/', {
            'email': 'naoexiste@seger.es.gov.br',
            'password': 'senhaqualquer'
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('não encontrado' in str(m).lower() for m in messages))
    
    def test_login_post_inactive_user(self):
        """POST com usuário inativo exibe erro"""
        response = self.client.post('/acoes-pngi/login/', {
            'email': self.user_inactive.email,
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('inativo' in str(m).lower() for m in messages))
    
    def test_login_post_wrong_password(self):
        """POST com senha incorreta exibe erro"""
        response = self.client.post('/acoes-pngi/login/', {
            'email': self.user.email,
            'password': 'senhaerrada'
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('senha incorreta' in str(m).lower() for m in messages))
    
    def test_login_post_user_without_app_access(self):
        """POST com usuário sem acesso à aplicação exibe erro"""
        response = self.client.post('/acoes-pngi/login/', {
            'email': self.user_no_access.email,
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('não tem permissão' in str(m).lower() for m in messages))
    
    def test_login_post_successful(self):
        """POST com credenciais válidas e acesso faz login com sucesso"""
        response = self.client.post('/acoes-pngi/login/', {
            'email': self.user.email,
            'password': 'testpass123'
        }, follow=True)
        
        # Deve redirecionar para dashboard
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('bem-vindo' in str(m).lower() for m in messages))
    
    def test_login_app_not_found_error(self):
        """POST quando aplicação não existe no banco exibe erro"""
        # Deletar aplicação temporariamente
        Aplicacao.objects.filter(codigointerno='ACOES_PNGI').delete()
        
        response = self.client.post('/acoes-pngi/login/', {
            'email': self.user.email,
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('aplicação não encontrada' in str(m).lower() for m in messages))


class DashboardWebViewTests(TestCase):
    """Testes completos do dashboard"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup inicial"""
        self.client = Client()
        
        # Criar aplicação (usar get_or_create)
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        # Criar role (usar get_or_create)
        self.role, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='COORDENADOR_PNGI',
            defaults={'nomeperfil': 'Coordenador PNGI'}
        )
        
        # Criar usuário
        self.user = User.objects.create_user(
            email='coord@seger.es.gov.br',
            name='Coordenador',
            password='testpass123'
        )
        UserRole.objects.create(
            user=self.user,
            aplicacao=self.app,
            role=self.role
        )
        
        # Criar dados
        self.eixo1 = Eixo.objects.create(strdescricaoeixo='Eixo 1', stralias='E1')
        self.eixo2 = Eixo.objects.create(strdescricaoeixo='Eixo 2', stralias='E2')
        self.eixo3 = Eixo.objects.create(strdescricaoeixo='Eixo 3', stralias='E3')
        
        self.situacao1 = SituacaoAcao.objects.create(strdescricaosituacaoacao='Situação 1')
        self.situacao2 = SituacaoAcao.objects.create(strdescricaosituacaoacao='Situação 2')
        
        self.vigencia_ativa = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),
            datfinalvigencia=date(2026, 12, 31),
            isvigenciaativa=True
        )
        
        self.vigencia_inativa = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2025',
            datiniciovigencia=date(2025, 1, 1),
            datfinalvigencia=date(2025, 12, 31),
            isvigenciaativa=False
        )
    
    def test_dashboard_requires_login(self):
        """Dashboard requer login"""
        response = self.client.get('/acoes-pngi/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
    
    def test_dashboard_shows_stats_with_permissions(self):
        """Dashboard mostra estatísticas quando usuário tem permissões"""
        self.client.login(email=self.user.email, password='testpass123')
        
        response = self.client.get('/acoes-pngi/dashboard/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('stats', response.context)
        
        # Verifica estatísticas
        stats = response.context['stats']
        self.assertEqual(stats.get('total_eixos'), 3)
        self.assertEqual(stats.get('total_situacoes'), 2)
        self.assertEqual(stats.get('total_vigencias'), 2)
        self.assertEqual(stats.get('vigencias_ativas'), 1)
    
    def test_dashboard_shows_ultimos_eixos(self):
        """Dashboard mostra últimos 5 eixos"""
        self.client.login(email=self.user.email, password='testpass123')
        
        response = self.client.get('/acoes-pngi/dashboard/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('ultimos_eixos', response.context)
        self.assertLessEqual(len(response.context['ultimos_eixos']), 5)
    
    def test_dashboard_shows_vigencia_atual(self):
        """Dashboard mostra vigência ativa"""
        self.client.login(email=self.user.email, password='testpass123')
        
        response = self.client.get('/acoes-pngi/dashboard/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('vigencia_atual', response.context)
        self.assertEqual(response.context['vigencia_atual'].idvigenciapngi, self.vigencia_ativa.idvigenciapngi)
    
    def test_dashboard_shows_user_role(self):
        """Dashboard mostra role do usuário"""
        self.client.login(email=self.user.email, password='testpass123')
        
        response = self.client.get('/acoes-pngi/dashboard/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('role', response.context)
        self.assertIn('role_display', response.context)
        self.assertEqual(response.context['role_display'], 'Coordenador PNGI')


class LogoutWebViewTests(TestCase):
    """Testes do logout"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        self.client = Client()
        
        app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        role, _ = Role.objects.get_or_create(
            aplicacao=app,
            codigoperfil='GESTOR',
            defaults={'nomeperfil': 'Gestor'}
        )
        
        user = User.objects.create_user(
            email='user@test.com',
            password='test123'
        )
        
        UserRole.objects.create(user=user, aplicacao=app, role=role)
        
        self.client.login(email='user@test.com', password='test123')
    
    def test_logout_success(self):
        """Logout desloga usuário e redireciona"""
        response = self.client.get('/acoes-pngi/logout/')
        
        self.assertEqual(response.status_code, 302)
        # Pode redirecionar para /login ou /accounts/select-role
        self.assertTrue('/login' in response.url or '/accounts/select-role' in response.url)
        
        # Verificar mensagem
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('logout' in str(m).lower() for m in messages))


class EixoCRUDWebViewTests(TestCase):
    """Testes completos de CRUD de Eixos"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup com permissões"""
        self.client = Client()
        
        # Criar aplicação (usar get_or_create)
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        # Criar role (usar get_or_create)
        self.role, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='COORDENADOR_PNGI',
            defaults={'nomeperfil': 'Coordenador'}
        )
        
        # Criar usuário
        self.user = User.objects.create_user(
            email='coord@test.com',
            password='test123'
        )
        UserRole.objects.create(user=self.user, aplicacao=self.app, role=self.role)
        
        self.client.login(email=self.user.email, password='test123')
        
        # Criar eixo para testes
        self.eixo = Eixo.objects.create(
            strdescricaoeixo='Eixo Teste',
            stralias='TESTE'
        )
    
    def test_eixo_list(self):
        """Lista de eixos"""
        response = self.client.get('/acoes-pngi/eixos/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('eixos', response.context)
    
    def test_eixo_create_get(self):
        """GET /eixos/create/ renderiza formulário"""
        response = self.client.get('/acoes-pngi/eixos/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acoes_pngi/eixos/form.html')
    
    def test_eixo_create_post_empty_fields(self):
        """POST com campos vazios exibe erro"""
        response = self.client.post('/acoes-pngi/eixos/create/', {
            'strdescricaoeixo': '',
            'stralias': ''
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('obrigatórios' in str(m).lower() for m in messages))
    
    def test_eixo_create_post_alias_too_long(self):
        """POST com alias maior que 5 caracteres exibe erro"""
        response = self.client.post('/acoes-pngi/eixos/create/', {
            'strdescricaoeixo': 'Eixo Novo',
            'stralias': 'TOOLONG'
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('máximo 5' in str(m) for m in messages))
    
    def test_eixo_create_post_success(self):
        """POST com dados válidos cria eixo"""
        response = self.client.post('/acoes-pngi/eixos/create/', {
            'strdescricaoeixo': 'Novo Eixo',
            'stralias': 'NOVO'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Eixo.objects.filter(stralias='NOVO').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('criado com sucesso' in str(m).lower() for m in messages))
    
    def test_eixo_create_post_database_error(self):
        """POST com erro de banco (alias duplicado) exibe erro"""
        # Tentar criar com alias já existente
        response = self.client.post('/acoes-pngi/eixos/create/', {
            'strdescricaoeixo': 'Eixo Duplicado',
            'stralias': 'TESTE'  # Já existe
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('erro' in str(m).lower() for m in messages))
    
    def test_eixo_update_get(self):
        """GET /eixos/{id}/update/ renderiza formulário de edição"""
        response = self.client.get(f'/acoes-pngi/eixos/{self.eixo.ideixo}/update/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('eixo', response.context)
    
    def test_eixo_update_not_found(self):
        """Update de eixo inexistente redireciona com erro"""
        response = self.client.get('/acoes-pngi/eixos/99999/update/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('não encontrado' in str(m).lower() for m in messages))
    
    def test_eixo_update_post_empty_fields(self):
        """POST update com campos vazios exibe erro"""
        response = self.client.post(f'/acoes-pngi/eixos/{self.eixo.ideixo}/update/', {
            'strdescricaoeixo': '',
            'stralias': ''
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('obrigatórios' in str(m).lower() for m in messages))
    
    def test_eixo_update_post_alias_too_long(self):
        """POST update com alias muito longo exibe erro"""
        response = self.client.post(f'/acoes-pngi/eixos/{self.eixo.ideixo}/update/', {
            'strdescricaoeixo': 'Atualizado',
            'stralias': 'MUITOLONGO'
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('máximo 5' in str(m) for m in messages))
    
    def test_eixo_update_post_success(self):
        """POST update com dados válidos atualiza eixo"""
        response = self.client.post(f'/acoes-pngi/eixos/{self.eixo.ideixo}/update/', {
            'strdescricaoeixo': 'Eixo Atualizado',
            'stralias': 'ATUAL'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.eixo.refresh_from_db()
        self.assertEqual(self.eixo.strdescricaoeixo, 'Eixo Atualizado')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('atualizado com sucesso' in str(m).lower() for m in messages))
    
    def test_eixo_delete_success(self):
        """DELETE de eixo remove do banco"""
        eixo_id = self.eixo.ideixo
        
        response = self.client.post(f'/acoes-pngi/eixos/{eixo_id}/delete/', follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Eixo.objects.filter(ideixo=eixo_id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('deletado com sucesso' in str(m).lower() for m in messages))
    
    def test_eixo_delete_not_found(self):
        """DELETE de eixo inexistente exibe erro"""
        response = self.client.post('/acoes-pngi/eixos/99999/delete/', follow=True)
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('não encontrado' in str(m).lower() for m in messages))


class VigenciaCRUDWebViewTests(TestCase):
    """Testes completos de CRUD de Vigências"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup com permissões"""
        self.client = Client()
        
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
        self.role, _ = Role.objects.get_or_create(
            aplicacao=self.app,
            codigoperfil='COORDENADOR_PNGI',
            defaults={'nomeperfil': 'Coordenador'}
        )
        
        self.user = User.objects.create_user(
            email='coord@test.com',
            password='test123'
        )
        UserRole.objects.create(user=self.user, aplicacao=self.app, role=self.role)
        
        self.client.login(email=self.user.email, password='test123')
        
        self.vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),
            datfinalvigencia=date(2026, 12, 31),
            isvigenciaativa=False
        )
    
    def test_vigencia_list(self):
        """Lista de vigências"""
        response = self.client.get('/acoes-pngi/vigencias/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('vigencias', response.context)
    
    def test_vigencia_create_get(self):
        """GET /vigencias/create/ renderiza formulário"""
        response = self.client.get('/acoes-pngi/vigencias/create/')
        self.assertEqual(response.status_code, 200)
    
    def test_vigencia_create_post_empty_fields(self):
        """POST com campos vazios exibe erro"""
        response = self.client.post('/acoes-pngi/vigencias/create/', {
            'strdescricaovigenciapngi': '',
            'datiniciovigencia': '',
            'datfinalvigencia': '',
            'isvigenciaativa': 'false'
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('obrigatórios' in str(m).lower() for m in messages))
    
    def test_vigencia_create_post_invalid_date_format(self):
        """POST com formato de data inválido exibe erro"""
        response = self.client.post('/acoes-pngi/vigencias/create/', {
            'strdescricaovigenciapngi': 'PNGI 2027',
            'datiniciovigencia': 'data-invalida',
            'datfinalvigencia': '2027-12-31',
            'isvigenciaativa': 'false'
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('formato de data' in str(m).lower() for m in messages))
    
    def test_vigencia_create_post_end_before_start(self):
        """POST com data fim antes da data início exibe erro"""
        response = self.client.post('/acoes-pngi/vigencias/create/', {
            'strdescricaovigenciapngi': 'PNGI 2027',
            'datiniciovigencia': '2027-12-31',
            'datfinalvigencia': '2027-01-01',
            'isvigenciaativa': 'false'
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('posterior' in str(m).lower() for m in messages))
    
    def test_vigencia_create_post_success(self):
        """POST com dados válidos cria vigência"""
        response = self.client.post('/acoes-pngi/vigencias/create/', {
            'strdescricaovigenciapngi': 'PNGI 2027',
            'datiniciovigencia': '2027-01-01',
            'datfinalvigencia': '2027-12-31',
            'isvigenciaativa': 'false'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(VigenciaPNGI.objects.filter(strdescricaovigenciapngi='PNGI 2027').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('criada com sucesso' in str(m).lower() for m in messages))
    
    def test_vigencia_create_post_active_deactivates_others(self):
        """POST criando vigência ativa desativa as outras"""
        # Criar vigência ativa
        vigencia_ativa = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='Ativa Anterior',
            datiniciovigencia=date(2025, 1, 1),
            datfinalvigencia=date(2025, 12, 31),
            isvigenciaativa=True
        )
        
        response = self.client.post('/acoes-pngi/vigencias/create/', {
            'strdescricaovigenciapngi': 'Nova Ativa',
            'datiniciovigencia': '2028-01-01',
            'datfinalvigencia': '2028-12-31',
            'isvigenciaativa': 'true'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        vigencia_ativa.refresh_from_db()
        self.assertFalse(vigencia_ativa.isvigenciaativa)
    
    def test_vigencia_update_not_found(self):
        """Update de vigência inexistente redireciona com erro"""
        response = self.client.get('/acoes-pngi/vigencias/99999/update/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('não encontrada' in str(m).lower() for m in messages))
    
    def test_vigencia_update_post_success(self):
        """POST update com dados válidos atualiza vigência"""
        response = self.client.post(f'/acoes-pngi/vigencias/{self.vigencia.idvigenciapngi}/update/', {
            'strdescricaovigenciapngi': 'PNGI 2026 Atualizado',
            'datiniciovigencia': '2026-01-01',
            'datfinalvigencia': '2026-12-31',
            'isvigenciaativa': 'false'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.vigencia.refresh_from_db()
        self.assertEqual(self.vigencia.strdescricaovigenciapngi, 'PNGI 2026 Atualizado')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('atualizada com sucesso' in str(m).lower() for m in messages))
    
    def test_vigencia_update_activate_deactivates_others(self):
        """Update ativando vigência desativa as outras"""
        vigencia_ativa = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='Outra Ativa',
            datiniciovigencia=date(2025, 1, 1),
            datfinalvigencia=date(2025, 12, 31),
            isvigenciaativa=True
        )
        
        response = self.client.post(f'/acoes-pngi/vigencias/{self.vigencia.idvigenciapngi}/update/', {
            'strdescricaovigenciapngi': 'PNGI 2026',
            'datiniciovigencia': '2026-01-01',
            'datfinalvigencia': '2026-12-31',
            'isvigenciaativa': 'true'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        vigencia_ativa.refresh_from_db()
        self.assertFalse(vigencia_ativa.isvigenciaativa)
        self.vigencia.refresh_from_db()
        self.assertTrue(self.vigencia.isvigenciaativa)
    
    def test_vigencia_delete_success(self):
        """DELETE de vigência remove do banco"""
        vigencia_id = self.vigencia.idvigenciapngi
        
        response = self.client.post(f'/acoes-pngi/vigencias/{vigencia_id}/delete/', follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(VigenciaPNGI.objects.filter(idvigenciapngi=vigencia_id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('deletada com sucesso' in str(m).lower() for m in messages))
    
    def test_vigencia_delete_not_found(self):
        """DELETE de vigência inexistente exibe erro"""
        response = self.client.post('/acoes-pngi/vigencias/99999/delete/', follow=True)
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('não encontrada' in str(m).lower() for m in messages))
