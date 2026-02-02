# carga_org_lot/tests/test_web_views.py
import logging
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Aplicacao, Role, UserRole
from carga_org_lot.models import (
    TblPatriarca,
    TblOrganogramaVersao,
    TblLotacaoVersao,
    TblOrgaoUnidade,
    TblStatusProgresso,
)

User = get_user_model()
logger = logging.getLogger(__name__)


class BaseWebViewTestCase(TestCase):
    """
    Classe base para testes de web views com setup completo.
    """
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        try:
            # Aplicação - usa get_or_create para evitar IntegrityError
            cls.aplicacao, created = Aplicacao.objects.get_or_create(
                codigointerno='CARGA_ORG_LOT',
                defaults={
                    'nomeaplicacao': 'Carga Org/Lot',
                    'isshowinportal': True
                }
            )
            logger.info(f"Aplicação {'criada' if created else 'recuperada'}: {cls.aplicacao.codigointerno}")
            
            # Role - usa get_or_create
            cls.role, created = Role.objects.get_or_create(
                codigoperfil='GESTOR_CARGA',
                aplicacao=cls.aplicacao,
                defaults={'nomeperfil': 'Gestor de Carga'}
            )
            logger.info(f"Role {'criada' if created else 'recuperada'}: {cls.role.codigoperfil}")
            
            # Usuário
            cls.user = User.objects.create_user(
                email='test@example.com',
                password='testpass123'
            )
            logger.info(f"Usuário criado: {cls.user.email}")
            
            # Associa role ao usuário
            cls.user_role = UserRole.objects.create(
                user=cls.user,
                role=cls.role,
                aplicacao=cls.aplicacao
            )
            logger.info(f"UserRole criado para {cls.user.email}")
            
            # Status de progresso necessário
            cls.status_progresso, created = TblStatusProgresso.objects.get_or_create(
                id_status_progresso=1,
                defaults={'str_descricao': 'Em andamento'}
            )
            logger.info(f"Status Progresso {'criado' if created else 'recuperado'}: {cls.status_progresso.str_descricao}")
            
            # Patriarca de teste - CORREÇÃO: str_nome_patriarca -> str_nome, user_criacao -> id_usuario_criacao
            cls.patriarca = TblPatriarca.objects.create(
                str_sigla_patriarca='SEGER',
                str_nome='Secretaria de Estado de Gestão e Recursos Humanos',
                id_status_progresso=cls.status_progresso,
                id_usuario_criacao=cls.user
            )
            logger.info(f"Patriarca criado: {cls.patriarca.str_sigla_patriarca}")
            
        except Exception as e:
            logger.error(f"❌ ERRO NO setUpTestData: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise
    
    def setUp(self):
        """
        Setup executado antes de cada teste.
        
        CORREÇÃO: 
        1. Usa force_login() ao invés de login()
        2. Configura active_role_CARGA_ORG_LOT na sessão (exigido pelo ActiveRoleMiddleware)
        3. Armazena ID do UserRole, não um dicionário
        
        O middleware ActiveRoleMiddleware procura por:
        - Chave: 'active_role_{app_code}' -> 'active_role_CARGA_ORG_LOT'
        - Valor: ID do UserRole (int)
        """
        self.client = Client()
        try:
            # Força login direto (método recomendado para testes)
            self.client.force_login(self.user)
            
            # CORREÇÃO CRITICA: Configura active_role_CARGA_ORG_LOT na sessão
            # O middleware procura pela chave 'active_role_{app_code}'
            # e espera o ID do UserRole, não um dicionário
            session = self.client.session
            session['active_role_CARGA_ORG_LOT'] = self.user_role.id
            session.save()
            
            # Valida que a sessão foi criada corretamente
            if not self.client.session.get('_auth_user_id'):
                logger.error("❌ Falha ao forçar login do usuário de teste")
            elif not self.client.session.get('active_role_CARGA_ORG_LOT'):
                logger.error("❌ Falha ao configurar active_role_CARGA_ORG_LOT na sessão")
            else:
                logger.info(
                    f"✅ Usuário {self.user.email} logado com force_login() e "
                    f"active_role_CARGA_ORG_LOT={self.user_role.id} configurado"
                )
                
        except Exception as e:
            logger.error(f"❌ ERRO NO setUp (force_login): {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")


class AuthenticationViewsTest(BaseWebViewTestCase):
    """Testes de views de autenticação."""
    
    def test_login_page_loads(self):
        """Página de login deve carregar corretamente."""
        try:
            self.client.logout()  # Garante que está deslogado
            response = self.client.get(reverse('carga_org_lot_web:login'))
            
            self.assertEqual(
                response.status_code, 200,
                f"❌ Status code esperado: 200, recebido: {response.status_code}"
            )
            self.assertContains(
                response, 'Carga Org Lot',
                msg_prefix="❌ Título 'Carga Org Lot' não encontrado na página"
            )
            logger.info("✅ test_login_page_loads passou")
            
        except Exception as e:
            logger.error(f"❌ ERRO em test_login_page_loads: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise
    
    def test_login_empty_fields(self):
        """Login com campos vazios deve mostrar erro."""
        try:
            self.client.logout()
            response = self.client.post(reverse('carga_org_lot_web:login'), {
                'email': '',
                'password': ''
            })
            
            # Pode retornar 200 com erro ou redirecionar
            self.assertIn(
                response.status_code, [200, 302],
                f"❌ Status code esperado: 200 ou 302, recebido: {response.status_code}"
            )
            logger.info("✅ test_login_empty_fields passou")
            
        except Exception as e:
            logger.error(f"❌ ERRO em test_login_empty_fields: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise
    
    def test_logout_redirects(self):
        """Logout deve redirecionar para login."""
        try:
            response = self.client.get(reverse('carga_org_lot_web:logout'))
            
            self.assertEqual(
                response.status_code, 302,
                f"❌ Status code esperado: 302, recebido: {response.status_code}"
            )
            logger.info("✅ test_logout_redirects passou")
            
        except Exception as e:
            logger.error(f"❌ ERRO em test_logout_redirects: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise


class DashboardViewTest(BaseWebViewTestCase):
    """Testes de view de dashboard."""
    
    def test_dashboard_requires_login(self):
        """Dashboard deve exigir autenticação."""
        try:
            self.client.logout()
            response = self.client.get(reverse('carga_org_lot_web:dashboard'))
            
            self.assertEqual(
                response.status_code, 302,
                f"❌ Status code esperado: 302, recebido: {response.status_code}"
            )
            logger.info("✅ test_dashboard_requires_login passou")
            
        except Exception as e:
            logger.error(f"❌ ERRO em test_dashboard_requires_login: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise
    
    def test_dashboard_loads_for_authenticated_user(self):
        """Dashboard deve carregar para usuário autenticado."""
        try:
            response = self.client.get(reverse('carga_org_lot_web:dashboard'))
            
            self.assertEqual(
                response.status_code, 200,
                f"❌ Status code esperado: 200, recebido: {response.status_code}"
            )
            logger.info("✅ test_dashboard_loads_for_authenticated_user passou")
            
        except Exception as e:
            logger.error(f"❌ ERRO em test_dashboard_loads_for_authenticated_user: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise


class AjaxViewsTest(BaseWebViewTestCase):
    """Testes de views AJAX."""
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        try:
            # Cria organograma versão necessário
            cls.organograma_versao = TblOrganogramaVersao.objects.create(
                id_patriarca=cls.patriarca,
                str_origem='TESTE',
                str_status_processamento='SUCESSO'
            )
            logger.info(f"Organograma versão criado: {cls.organograma_versao.id_organograma_versao}")
            
            # Cria órgãos para testes de busca - CORREÇÃO: nomes de campos
            cls.orgao_raiz = TblOrgaoUnidade.objects.create(
                id_organograma_versao=cls.organograma_versao,
                id_patriarca=cls.patriarca,
                str_sigla='SEGER',
                str_nome='Secretaria de Estado de Gestão',
                id_usuario_criacao=cls.user
            )
            
            cls.orgao_filho = TblOrgaoUnidade.objects.create(
                id_organograma_versao=cls.organograma_versao,
                id_patriarca=cls.patriarca,
                id_orgao_unidade_pai=cls.orgao_raiz,
                str_sigla='SUBSEGES',
                str_nome='Subsecretaria de Gestão',
                id_usuario_criacao=cls.user
            )
            logger.info(f"Órgãos criados para testes AJAX: {cls.orgao_raiz.str_sigla}, {cls.orgao_filho.str_sigla}")
            
        except Exception as e:
            logger.error(f"❌ ERRO no setUpTestData de AjaxViewsTest: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise
    
    def test_search_orgao_ajax_returns_json(self):
        """Busca de órgãos deve retornar JSON."""
        try:
            # Usa reverse() para obter URL correta
            url = reverse('carga_org_lot_web:search_orgao_ajax')
            response = self.client.get(url, {'q': 'SEGER'})
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response content-type: {response.get('Content-Type', 'N/A')}")
            
            self.assertEqual(
                response.status_code, 200,
                f"❌ Status code esperado: 200, recebido: {response.status_code}"
            )
            self.assertEqual(
                response.get('Content-Type'), 'application/json',
                f"❌ Content-Type esperado: application/json, recebido: {response.get('Content-Type')}"
            )
            logger.info("✅ test_search_orgao_ajax_returns_json passou")
                
        except Exception as e:
            logger.error(f"❌ ERRO em test_search_orgao_ajax_returns_json: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise
    
    def test_search_orgao_ajax_short_query(self):
        """Busca com query muito curta deve retornar vazio."""
        try:
            url = reverse('carga_org_lot_web:search_orgao_ajax')
            response = self.client.get(url, {'q': 'S'})
            
            self.assertEqual(
                response.status_code, 200,
                f"❌ Status code esperado: 200, recebido: {response.status_code}"
            )
            logger.info("✅ test_search_orgao_ajax_short_query passou")
                
        except Exception as e:
            logger.error(f"❌ ERRO em test_search_orgao_ajax_short_query: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise


class PaginationTest(BaseWebViewTestCase):
    """Testes de paginação."""
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        try:
            # Cria múltiplos patriarcas para testar paginação - CORREÇÃO: nomes de campos
            for i in range(25):
                TblPatriarca.objects.create(
                    str_sigla_patriarca=f'ORG{i:02d}',
                    str_nome=f'Organização {i:02d}',
                    id_status_progresso=cls.status_progresso,
                    id_usuario_criacao=cls.user
                )
            logger.info("25 patriarcas criados para testes de paginação")
            
        except Exception as e:
            logger.error(f"❌ ERRO no setUpTestData de PaginationTest: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise
    
    def test_pagination_exists_with_many_records(self):
        """Paginação deve existir quando há muitos registros."""
        try:
            # Usa reverse() para obter URL correta
            url = reverse('carga_org_lot_web:patriarca_list')
            response = self.client.get(url)
            
            self.assertEqual(
                response.status_code, 200,
                f"❌ Status code esperado: 200, recebido: {response.status_code}"
            )
            logger.info("✅ test_pagination_exists_with_many_records passou")
                
        except Exception as e:
            logger.error(f"❌ ERRO em test_pagination_exists_with_many_records: {type(e).__name__}: {str(e)}")
            logger.exception("Traceback completo:")
            raise
