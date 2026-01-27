# carga_org_lot/tests/__init__.py
import sys
from django.core.management import call_command
from django.db import connection
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


if "test" in sys.argv:
    call_command("migrate", "carga_org_lot", verbosity=0)


class CargaOrgLotTestCase(TestCase):
    """
    Classe base para testes do módulo carga_org_lot.
    Configura o schema PostgreSQL e dados iniciais.
    """
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute('CREATE SCHEMA IF NOT EXISTS carga_org_lot;')
            cursor.execute('SET search_path TO carga_org_lot, public;')
    
    @classmethod
    def tearDownClass(cls):
        with connection.cursor() as cursor:
            cursor.execute('SET search_path TO public;')
        super().tearDownClass()


class BaseDataTestCase(CargaOrgLotTestCase):
    """
    Classe base que cria dados de referência necessários para os testes.
    Separa dados estáticos (que existiriam em produção via migration)
    de dados de teste específicos.
    """
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        # Importações locais para evitar problemas de importação circular
        from accounts.models import Aplicacao, Role
        from carga_org_lot.models import (
            TblStatusProgresso,
            TblStatusTokenEnvioCarga,
            TblStatusCarga,
            TblTipoCarga,
        )
        
        # ==========================================
        # DADOS ESTÁTICOS (que viriam de migrations)
        # ==========================================
        
        # Aplicação Carga Org/Lot
        cls.aplicacao_carga, _ = Aplicacao.objects.get_or_create(
            codigointerno='CARGA_ORG_LOT',
            defaults={
                'nomeaplicacao': 'Carga Org/Lot',
                'isshowinportal': True
            }
        )
        
        # Role GESTOR_CARGA
        cls.role_gestor, _ = Role.objects.get_or_create(
            codigoperfil='GESTOR_CARGA',
            aplicacao=cls.aplicacao_carga,
            defaults={'nomeperfil': 'Gestor de Carga'}
        )
        
        # Status de Progresso
        cls.status_nova_carga, _ = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=1,
            defaults={'str_descricao': 'Nova Carga'}
        )
        cls.status_processando, _ = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=2,
            defaults={'str_descricao': 'Processando'}
        )
        cls.status_concluido, _ = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=3,
            defaults={'str_descricao': 'Concluído'}
        )
        cls.status_erro, _ = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=4,
            defaults={'str_descricao': 'Erro'}
        )
        
        # Status de Token
        cls.status_token_ativo, _ = TblStatusTokenEnvioCarga.objects.get_or_create(
            id_status_token_envio_carga=1,
            defaults={'str_descricao': 'Ativo'}
        )
        cls.status_token_expirado, _ = TblStatusTokenEnvioCarga.objects.get_or_create(
            id_status_token_envio_carga=2,
            defaults={'str_descricao': 'Expirado'}
        )
        
        # Status de Carga
        cls.status_carga_pendente, _ = TblStatusCarga.objects.get_or_create(
            id_status_carga=1,
            defaults={'str_descricao': 'Pendente', 'flg_sucesso': 0}
        )
        cls.status_carga_processando, _ = TblStatusCarga.objects.get_or_create(
            id_status_carga=2,
            defaults={'str_descricao': 'Processando', 'flg_sucesso': 0}
        )
        cls.status_carga_sucesso, _ = TblStatusCarga.objects.get_or_create(
            id_status_carga=3,
            defaults={'str_descricao': 'Sucesso', 'flg_sucesso': 1}
        )
        cls.status_carga_erro, _ = TblStatusCarga.objects.get_or_create(
            id_status_carga=4,
            defaults={'str_descricao': 'Erro', 'flg_sucesso': 0}
        )
        
        # Tipos de Carga
        cls.tipo_carga_org, _ = TblTipoCarga.objects.get_or_create(
            id_tipo_carga=1,
            defaults={'str_descricao': 'Organograma'}
        )
        cls.tipo_carga_lot, _ = TblTipoCarga.objects.get_or_create(
            id_tipo_carga=2,
            defaults={'str_descricao': 'Lotação'}
        )
        
        # ==========================================
        # DADOS DE TESTE (específicos para testes)
        # ==========================================
        
        # Usuário de teste - User NÃO tem campo username!
        cls.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
