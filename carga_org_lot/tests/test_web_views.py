# carga_org_lot/tests/test_web_views.py
"""
Testes completos para Web Views do carga_org_lot.
Cobre autenticação, CRUD, filtros, paginação, permissões e AJAX.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
import json

from accounts.models import UserRole, Aplicacao, Role
from ..models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblOrgaoUnidade,
    TblLotacaoVersao,
    TblLotacao,
    TblLotacaoInconsistencia,
    TblCargaPatriarca,
    TblTokenEnvioCarga,
    TblStatusProgresso,
    TblStatusTokenEnvioCarga,
    TblStatusCarga,
    TblTipoCarga,
)

User = get_user_model()


class WebViewsBaseTest(TestCase):
    """Classe base com setup compartilhado"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    @classmethod
    def setUpTestData(cls):
        # Criar aplicação
        cls.aplicacao = Aplicacao.objects.create(
            codigointerno='CARGA_ORG_LOT',
            nomeaplicacao='Carga Org/Lot'
        )
        
        # Criar role
        cls.role_gestor = Role.objects.create(
            aplicacao=cls.aplicacao,
            nomeperfil='Gestor Carga',
            codigoperfil='GESTOR_CARGA'
        )
        
        # Criar usuário com permissão
        cls.user = User.objects.create_user(
            email='gestor@example.com',
            password='senha123',
            name='Gestor Teste'
        )
        
        UserRole.objects.create(
            user=cls.user,
            aplicacao=cls.aplicacao,
            role=cls.role_gestor
        )
        
        # Criar usuário sem permissão
        cls.user_sem_permissao = User.objects.create_user(
            email='sem_permissao@example.com',
            password='senha123',
            name='Sem Permissão'
        )
        
        # Criar dados de teste
        cls.status_progresso = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=1,
            defaults={'str_descricao': 'Em Progresso'}
        )[0]
        
        cls.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='SEGER',
            str_nome='Secretaria de Estado da Gestão e Recursos Humanos',
            id_status_progresso=cls.status_progresso,
            dat_criacao=timezone.now(),
            id_usuario_criacao=cls.user
        )
    
    def setUp(self):
        self.client = Client()


# ============================================
# TESTES DE AUTENTICAÇÃO
# ============================================

class AuthenticationViewsTest(WebViewsBaseTest):
    """Testes de login e logout"""
    
    def test_login_page_loads(self):
        """Página de login deve carregar"""
        response = self.client.get(reverse('carga_org_lot_web:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/login.html')
    
    def test_login_success(self):
        """Login com credenciais válidas deve redirecionar para dashboard"""
        response = self.client.post(
            reverse('carga_org_lot_web:login'),
            {'email': 'gestor@example.com', 'password': 'senha123'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_invalid_credentials(self):
        """Login com senha incorreta deve mostrar erro"""
        response = self.client.post(
            reverse('carga_org_lot_web:login'),
            {'email': 'gestor@example.com', 'password': 'senha_errada'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'incorreta', status_code=200)
    
    def test_login_user_without_permission(self):
        """Usuário sem permissão não deve conseguir fazer login"""
        response = self.client.post(
            reverse('carga_org_lot_web:login'),
            {'email': 'sem_permissao@example.com', 'password': 'senha123'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'permissão', status_code=200)
    
    def test_login_empty_fields(self):
        """Login com campos vazios deve mostrar erro"""
        response = self.client.post(
            reverse('carga_org_lot_web:login'),
            {'email': '', 'password': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'campos', status_code=200)
    
    def test_login_user_not_found(self):
        """Login com usuário inexistente deve mostrar erro"""
        response = self.client.post(
            reverse('carga_org_lot_web:login'),
            {'email': 'inexistente@example.com', 'password': 'senha123'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'encontrado', status_code=200)
    
    def test_logout(self):
        """Logout deve desautenticar usuário"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(reverse('carga_org_lot_web:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


# ============================================
# TESTES DE DASHBOARD
# ============================================

class DashboardViewTest(WebViewsBaseTest):
    """Testes do dashboard principal"""
    
    def test_dashboard_requires_login(self):
        """Dashboard deve exigir login"""
        response = self.client.get(reverse('carga_org_lot_web:dashboard'))
        self.assertEqual(response.status_code, 302)
    
    def test_dashboard_loads_authenticated(self):
        """Dashboard deve carregar para usuário autenticado"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(reverse('carga_org_lot_web:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/dashboard.html')
    
    def test_dashboard_context_has_stats(self):
        """Dashboard deve conter estatísticas"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(reverse('carga_org_lot_web:dashboard'))
        self.assertIn('stats', response.context)
        self.assertIn('patriarcas', response.context['stats'])


# ============================================
# TESTES DE PATRIARCAS
# ============================================

class PatriarcaViewsTest(WebViewsBaseTest):
    """Testes de views de patriarcas"""
    
    def test_patriarca_list_requires_login(self):
        """Listagem de patriarcas exige login"""
        response = self.client.get(reverse('carga_org_lot_web:patriarca_list'))
        self.assertEqual(response.status_code, 302)
    
    def test_patriarca_list_loads(self):
        """Listagem de patriarcas deve carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(reverse('carga_org_lot_web:patriarca_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/patriarca_list.html')
    
    def test_patriarca_list_with_search(self):
        """Busca de patriarcas deve filtrar resultados"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:patriarca_list'),
            {'search': 'SEGER'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SEGER')
    
    def test_patriarca_detail_loads(self):
        """Detalhes de patriarca devem carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:patriarca_detail', args=[self.patriarca.id_patriarca])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/patriarca_detail.html')
        self.assertEqual(response.context['patriarca'], self.patriarca)
    
    def test_patriarca_detail_not_found(self):
        """Patriarca inexistente deve retornar 404"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:patriarca_detail', args=[99999])
        )
        self.assertEqual(response.status_code, 404)


# ============================================
# TESTES DE ORGANOGRAMAS
# ============================================

class OrganogramaViewsTest(WebViewsBaseTest):
    """Testes de views de organogramas"""
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.organograma = TblOrganogramaVersao.objects.create(
            id_patriarca=cls.patriarca,
            dat_processamento=timezone.now(),
            flg_ativo=True
        )
        
        cls.orgao_raiz = TblOrgaoUnidade.objects.create(
            id_patriarca=cls.patriarca,
            id_organograma_versao=cls.organograma,
            str_sigla='SEGER',
            str_nome='Raiz',
            int_nivel_hierarquia=1,
            flg_ativo=True
        )
    
    def test_organograma_list_loads(self):
        """Listagem de organogramas deve carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(reverse('carga_org_lot_web:organograma_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/organograma_list.html')
    
    def test_organograma_list_filter_by_patriarca(self):
        """Filtro por patriarca deve funcionar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:organograma_list'),
            {'patriarca': self.patriarca.id_patriarca}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SEGER')
    
    def test_organograma_detail_loads(self):
        """Detalhes de organograma devem carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:organograma_detail', args=[self.organograma.id_organograma_versao])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/organograma_detail.html')
    
    def test_organograma_hierarquia_json(self):
        """Hierarquia JSON deve retornar estrutura correta"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:organograma_hierarquia_json', args=[self.organograma.id_organograma_versao])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('hierarquia', data)
        self.assertIn('patriarca', data)


# ============================================
# TESTES DE LOTAÇÕES
# ============================================

class LotacaoViewsTest(WebViewsBaseTest):
    """Testes de views de lotações"""
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        cls.organograma = TblOrganogramaVersao.objects.create(
            id_patriarca=cls.patriarca,
            dat_processamento=timezone.now(),
            flg_ativo=True
        )
        
        cls.lotacao_versao = TblLotacaoVersao.objects.create(
            id_patriarca=cls.patriarca,
            id_organograma_versao=cls.organograma,
            dat_processamento=timezone.now()
        )
        
        cls.orgao = TblOrgaoUnidade.objects.create(
            id_patriarca=cls.patriarca,
            id_organograma_versao=cls.organograma,
            str_sigla='SEGER',
            str_nome='Secretaria',
            int_nivel_hierarquia=1,
            flg_ativo=True
        )
        
        cls.lotacao = TblLotacao.objects.create(
            id_lotacao_versao=cls.lotacao_versao,
            id_orgao_lotacao=cls.orgao,
            id_unidade_lotacao=cls.orgao,
            str_cpf='12345678901',
            flg_valido=True
        )
    
    def test_lotacao_list_loads(self):
        """Listagem de lotações deve carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(reverse('carga_org_lot_web:lotacao_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/lotacao_list.html')
    
    def test_lotacao_detail_loads(self):
        """Detalhes de lotação devem carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:lotacao_detail', args=[self.lotacao_versao.id_lotacao_versao])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/lotacao_detail.html')
        self.assertIn('stats', response.context)
    
    def test_lotacao_detail_filter_by_cpf(self):
        """Filtro por CPF deve funcionar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:lotacao_detail', args=[self.lotacao_versao.id_lotacao_versao]),
            {'cpf': '12345'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '12345')
    
    def test_lotacao_inconsistencias_loads(self):
        """Página de inconsistências deve carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:lotacao_inconsistencias', args=[self.lotacao_versao.id_lotacao_versao])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/lotacao_inconsistencias.html')


# ============================================
# TESTES DE CARGAS
# ============================================

class CargaViewsTest(WebViewsBaseTest):
    """Testes de views de cargas"""
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        cls.status_carga = TblStatusCarga.objects.get_or_create(
            id_status_carga=1,
            defaults={'str_descricao': 'Iniciado', 'flg_sucesso': 0}
        )[0]
        
        cls.tipo_carga = TblTipoCarga.objects.get_or_create(
            id_tipo_carga=1,
            defaults={'str_descricao': 'Organograma'}
        )[0]
        
        cls.status_token = TblStatusTokenEnvioCarga.objects.get_or_create(
            id_status_token_envio_carga=1,
            defaults={'str_descricao': 'Ativo'}
        )[0]
        
        cls.token = TblTokenEnvioCarga.objects.create(
            id_patriarca=cls.patriarca,
            id_status_token_envio_carga=cls.status_token,
            str_token_retorno='TOKEN123',
            dat_data_hora_inicio=timezone.now()
        )
        
        cls.carga = TblCargaPatriarca.objects.create(
            id_patriarca=cls.patriarca,
            id_tipo_carga=cls.tipo_carga,
            id_status_carga=cls.status_carga,
            id_token_envio_carga=cls.token,
            dat_data_hora_inicio=timezone.now()
        )
    
    def test_carga_list_loads(self):
        """Listagem de cargas deve carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(reverse('carga_org_lot_web:carga_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/carga_list.html')
    
    def test_carga_list_filter_by_patriarca(self):
        """Filtro por patriarca deve funcionar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:carga_list'),
            {'patriarca': self.patriarca.id_patriarca}
        )
        self.assertEqual(response.status_code, 200)
    
    def test_carga_detail_loads(self):
        """Detalhes de carga devem carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:carga_detail', args=[self.carga.id_carga_patriarca])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/carga_detail.html')
        self.assertIn('timeline', response.context)


# ============================================
# TESTES DE UPLOAD
# ============================================

class UploadViewsTest(WebViewsBaseTest):
    """Testes de views de upload"""
    
    def test_upload_page_loads(self):
        """Página de upload deve carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(reverse('carga_org_lot_web:upload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carga_org_lot/upload.html')
    
    def test_upload_organograma_handler(self):
        """Handler de upload de organograma deve aceitar POST"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.post(
            reverse('carga_org_lot_web:upload_organograma_handler'),
            {},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
    
    def test_upload_lotacao_handler(self):
        """Handler de upload de lotação deve aceitar POST"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.post(
            reverse('carga_org_lot_web:upload_lotacao_handler'),
            {},
            follow=True
        )
        self.assertEqual(response.status_code, 200)


# ============================================
# TESTES DE AJAX/BUSCA
# ============================================

class AjaxViewsTest(WebViewsBaseTest):
    """Testes de views AJAX"""
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        cls.organograma = TblOrganogramaVersao.objects.create(
            id_patriarca=cls.patriarca,
            dat_processamento=timezone.now(),
            flg_ativo=True
        )
        
        cls.orgao = TblOrgaoUnidade.objects.create(
            id_patriarca=cls.patriarca,
            id_organograma_versao=cls.organograma,
            str_sigla='SEGER',
            str_nome='Secretaria',
            int_nivel_hierarquia=1,
            flg_ativo=True
        )
    
    def test_search_orgao_ajax_returns_json(self):
        """Busca de órgãos deve retornar JSON"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:search_orgao_ajax'),
            {'q': 'SEGER'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertIn('results', data)
    
    def test_search_orgao_ajax_short_query(self):
        """Busca com query muito curta deve retornar vazio"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:search_orgao_ajax'),
            {'q': 'S'}
        )
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 0)


# ============================================
# TESTES DE PAGINAÇÃO
# ============================================

class PaginationTest(WebViewsBaseTest):
    """Testes de paginação"""
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        # Criar 25 patriarcas para testar paginação
        for i in range(25):
            TblPatriarca.objects.create(
                id_externo_patriarca=uuid.uuid4(),
                str_sigla_patriarca=f'ORG{i}',
                str_nome=f'Organização {i}',
                id_status_progresso=cls.status_progresso,
                dat_criacao=timezone.now(),
                id_usuario_criacao=cls.user
            )
    
    def test_pagination_first_page(self):
        """Primeira página deve carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(reverse('carga_org_lot_web:patriarca_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['page_obj'].has_next())
    
    def test_pagination_second_page(self):
        """Segunda página deve carregar"""
        self.client.login(username='gestor@example.com', password='senha123')
        response = self.client.get(
            reverse('carga_org_lot_web:patriarca_list'),
            {'page': 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['page_obj'].has_previous())
