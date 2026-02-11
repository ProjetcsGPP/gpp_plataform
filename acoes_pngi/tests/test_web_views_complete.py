"""acoes_pngi/tests/test_web_views_complete.py

Testes completos para Web Views - Ações PNGI

Testa as views REAIS definidas em acoes_pngi/views/web_views/core_web_views.py:
- CRUD de Eixos (List, Create, Update, Delete)
- CRUD de VigênciaPNGI (List, Create, Update, Delete)
- CRUD de SituaçãoAcao (List, Create, Update, Delete)

Todas as views usam apenas LoginRequiredMixin (sem permissões personalizadas).
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from datetime import date

from accounts.models import Aplicacao, Role, UserRole
from ..models import Eixo, SituacaoAcao, VigenciaPNGI

User = get_user_model()


class EixoCRUDWebViewTests(TestCase):
    """Testes completos de CRUD de Eixos"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup com usuário autenticado"""
        self.client = Client()
        
        # Criar aplicação e role
        self.app, _ = Aplicacao.objects.get_or_create(
            codigointerno='ACOES_PNGI',
            defaults={'nomeaplicacao': 'Ações PNGI'}
        )
        
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
        
        # Login
        self.client.login(email=self.user.email, password='test123')
        
        # Criar eixo para testes
        self.eixo = Eixo.objects.create(
            strdescricaoeixo='Eixo Teste',
            stralias='TESTE'
        )
    
    def test_eixo_list_requires_login(self):
        """Lista de eixos requer login"""
        self.client.logout()
        response = self.client.get('/acoes-pngi/eixos/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login', response.url)
    
    def test_eixo_list_authenticated(self):
        """Lista de eixos para usuário autenticado"""
        response = self.client.get('/acoes-pngi/eixos/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('eixos', response.context)
        self.assertEqual(list(response.context['eixos']), [self.eixo])
    
    def test_eixo_list_with_search(self):
        """Lista de eixos com busca"""
        Eixo.objects.create(strdescricaoeixo='Outro Eixo', stralias='OUTRO')
        
        response = self.client.get('/acoes-pngi/eixos/', {'search': 'Teste'})
        self.assertEqual(response.status_code, 200)
        eixos = list(response.context['eixos'])
        self.assertEqual(len(eixos), 1)
        self.assertEqual(eixos[0].strdescricaoeixo, 'Eixo Teste')
    
    def test_eixo_detail_authenticated(self):
        """Detalhes do eixo para usuário autenticado"""
        response = self.client.get(f'/acoes-pngi/eixos/{self.eixo.ideixo}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['eixo'], self.eixo)
    
    def test_eixo_create_get(self):
        """GET /eixos/novo/ renderiza formulário"""
        response = self.client.get('/acoes-pngi/eixos/novo/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acoes_pngi/eixo/form.html')
    
    def test_eixo_create_post_success(self):
        """POST com dados válidos cria eixo"""
        response = self.client.post('/acoes-pngi/eixos/novo/', {
            'strdescricaoeixo': 'Novo Eixo',
            'stralias': 'NOVO'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Eixo.objects.filter(stralias='NOVO').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('criado com sucesso' in str(m).lower() for m in messages))
    
    def test_eixo_create_post_duplicate_alias(self):
        """POST com alias duplicado falha"""
        response = self.client.post('/acoes-pngi/eixos/novo/', {
            'strdescricaoeixo': 'Eixo Duplicado',
            'stralias': 'TESTE'  # Já existe
        })
        
        # Form rejeita duplicata
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'stralias', None)  # Erro genérico de unicidade
    
    def test_eixo_update_get(self):
        """GET /eixos/{id}/editar/ renderiza formulário de edição"""
        response = self.client.get(f'/acoes-pngi/eixos/{self.eixo.ideixo}/editar/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['eixo'], self.eixo)
    
    def test_eixo_update_post_success(self):
        """POST update com dados válidos atualiza eixo"""
        response = self.client.post(f'/acoes-pngi/eixos/{self.eixo.ideixo}/editar/', {
            'strdescricaoeixo': 'Eixo Atualizado',
            'stralias': 'ATUAL'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.eixo.refresh_from_db()
        self.assertEqual(self.eixo.strdescricaoeixo, 'Eixo Atualizado')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('atualizado com sucesso' in str(m).lower() for m in messages))
    
    def test_eixo_delete_get(self):
        """GET /eixos/{id}/excluir/ renderiza confirmação"""
        response = self.client.get(f'/acoes-pngi/eixos/{self.eixo.ideixo}/excluir/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acoes_pngi/eixo/confirm_delete.html')
    
    def test_eixo_delete_post_success(self):
        """POST delete remove eixo do banco"""
        eixo_id = self.eixo.ideixo
        
        response = self.client.post(f'/acoes-pngi/eixos/{eixo_id}/excluir/', follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Eixo.objects.filter(ideixo=eixo_id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('excluído com sucesso' in str(m).lower() for m in messages))


class VigenciaCRUDWebViewTests(TestCase):
    """Testes completos de CRUD de Vigências"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup com usuário autenticado"""
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
    
    def test_vigencia_list_requires_login(self):
        """Lista de vigências requer login"""
        self.client.logout()
        response = self.client.get('/acoes-pngi/vigencias-pngi/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login', response.url)
    
    def test_vigencia_list_authenticated(self):
        """Lista de vigências para usuário autenticado"""
        response = self.client.get('/acoes-pngi/vigencias-pngi/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('vigencias', response.context)
        self.assertEqual(list(response.context['vigencias']), [self.vigencia])
    
    def test_vigencia_detail_authenticated(self):
        """Detalhes da vigência para usuário autenticado"""
        response = self.client.get(f'/acoes-pngi/vigencias-pngi/{self.vigencia.idvigenciapngi}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['vigencia'], self.vigencia)
    
    def test_vigencia_create_get(self):
        """GET /vigencias-pngi/novo/ renderiza formulário"""
        response = self.client.get('/acoes-pngi/vigencias-pngi/novo/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acoes_pngi/vigenciapngi/form.html')
    
    def test_vigencia_create_post_success(self):
        """POST com dados válidos cria vigência"""
        response = self.client.post('/acoes-pngi/vigencias-pngi/novo/', {
            'strdescricaovigenciapngi': 'PNGI 2027',
            'datiniciovigencia': '2027-01-01',
            'datfinalvigencia': '2027-12-31',
            'isvigenciaativa': 'false'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(VigenciaPNGI.objects.filter(strdescricaovigenciapngi='PNGI 2027').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('criada com sucesso' in str(m).lower() for m in messages))
    
    def test_vigencia_update_get(self):
        """GET /vigencias-pngi/{id}/editar/ renderiza formulário de edição"""
        response = self.client.get(f'/acoes-pngi/vigencias-pngi/{self.vigencia.idvigenciapngi}/editar/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_vigencia_update_post_success(self):
        """POST update com dados válidos atualiza vigência"""
        response = self.client.post(f'/acoes-pngi/vigencias-pngi/{self.vigencia.idvigenciapngi}/editar/', {
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
    
    def test_vigencia_delete_get(self):
        """GET /vigencias-pngi/{id}/excluir/ renderiza confirmação"""
        response = self.client.get(f'/acoes-pngi/vigencias-pngi/{self.vigencia.idvigenciapngi}/excluir/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acoes_pngi/vigenciapngi/confirm_delete.html')
    
    def test_vigencia_delete_post_success(self):
        """POST delete remove vigência do banco"""
        vigencia_id = self.vigencia.idvigenciapngi
        
        response = self.client.post(f'/acoes-pngi/vigencias-pngi/{vigencia_id}/excluir/', follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(VigenciaPNGI.objects.filter(idvigenciapngi=vigencia_id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('excluída com sucesso' in str(m).lower() for m in messages))


class SituacaoAcaoCRUDWebViewTests(TestCase):
    """Testes completos de CRUD de Situações de Ação"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        """Setup com usuário autenticado"""
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
        
        # Campo correto: strdescricaosituacao
        self.situacao = SituacaoAcao.objects.create(strdescricaosituacao='Situação Teste')
    
    def test_situacao_list_requires_login(self):
        """Lista de situações requer login"""
        self.client.logout()
        response = self.client.get('/acoes-pngi/situacoes-acao/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login', response.url)
    
    def test_situacao_list_authenticated(self):
        """Lista de situações para usuário autenticado"""
        response = self.client.get('/acoes-pngi/situacoes-acao/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('situacoes', response.context)
        self.assertEqual(list(response.context['situacoes']), [self.situacao])
    
    def test_situacao_detail_authenticated(self):
        """Detalhes da situação para usuário autenticado"""
        response = self.client.get(f'/acoes-pngi/situacoes-acao/{self.situacao.idsituacaoacao}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['situacao'], self.situacao)
    
    def test_situacao_create_get(self):
        """GET /situacoes-acao/novo/ renderiza formulário"""
        response = self.client.get('/acoes-pngi/situacoes-acao/novo/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acoes_pngi/situacaoacao/form.html')
    
    def test_situacao_create_post_success(self):
        """POST com dados válidos cria situação"""
        response = self.client.post('/acoes-pngi/situacoes-acao/novo/', {
            'strdescricaosituacao': 'Nova Situação'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SituacaoAcao.objects.filter(strdescricaosituacao='Nova Situação').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('criada com sucesso' in str(m).lower() for m in messages))
    
    def test_situacao_update_get(self):
        """GET /situacoes-acao/{id}/editar/ renderiza formulário de edição"""
        response = self.client.get(f'/acoes-pngi/situacoes-acao/{self.situacao.idsituacaoacao}/editar/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_situacao_update_post_success(self):
        """POST update com dados válidos atualiza situação"""
        response = self.client.post(f'/acoes-pngi/situacoes-acao/{self.situacao.idsituacaoacao}/editar/', {
            'strdescricaosituacao': 'Situação Atualizada'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.situacao.refresh_from_db()
        self.assertEqual(self.situacao.strdescricaosituacao, 'Situação Atualizada')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('atualizada com sucesso' in str(m).lower() for m in messages))
    
    def test_situacao_delete_get(self):
        """GET /situacoes-acao/{id}/excluir/ renderiza confirmação"""
        response = self.client.get(f'/acoes-pngi/situacoes-acao/{self.situacao.idsituacaoacao}/excluir/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acoes_pngi/situacaoacao/confirm_delete.html')
    
    def test_situacao_delete_post_success(self):
        """POST delete remove situação do banco"""
        situacao_id = self.situacao.idsituacaoacao
        
        response = self.client.post(f'/acoes-pngi/situacoes-acao/{situacao_id}/excluir/', follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(SituacaoAcao.objects.filter(idsituacaoacao=situacao_id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('excluída com sucesso' in str(m).lower() for m in messages))
