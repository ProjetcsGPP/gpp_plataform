"""Classe base unificada para todos os testes do módulo acoes_pngi"""
from django.test import TestCase
from django.utils import timezone
from .fixtures.test_data_base import create_base_test_data


class BaseTestCase(TestCase):
    """
    Classe base para testes Django do módulo acoes_pngi.
    
    Fornece:
        - Dados base compartilhados (eixo, situação, vigência)
        - Factory method para criar ações completas
        - Configuração de banco de dados multi-schema
    """
    databases = {'default', 'gpp_plataform_db'}
    
    @classmethod
    def setUpClass(cls):
        """Configuração executada UMA VEZ por classe de teste"""
        super().setUpClass()
        
        # Criar dados base compartilhados
        base_data = create_base_test_data()
        cls.eixo_base = base_data.eixo
        cls.situacao_base = base_data.situacao
        cls.vigencia_base = base_data.vigencia
        
        # Aplicacao PNGI - importar de accounts
        try:
            from accounts.models import Aplicacao
            cls.app, _ = Aplicacao.objects.using('gpp_plataform_db').get_or_create(
                codigointerno='ACOES_PNGI',
                defaults={'descricao': 'Sistema de Ações PNGI'}
            )
        except (ImportError, Exception) as e:
            # Se não existir o modelo Aplicacao, apenas avisar
            print(f"Aviso: Não foi possível carregar Aplicacao: {e}")
            cls.app = None
    
    def create_acao_base(self, **kwargs):
        """
        Factory method para criar ações sempre completas.
        
        Args:
            **kwargs: Campos customizados para sobrescrever padrões
        
        Returns:
            Acoes: Instância de ação criada com todos os campos obrigatórios
        
        Exemplo:
            >>> acao = self.create_acao_base(strapelido="ACAO-CUSTOM")
            >>> acao2 = self.create_acao_base(strdescricaoacao="Descrição customizada")
        """
        from acoes_pngi.models import Acoes
        
        # Defaults com TODOS os campos obrigatórios
        defaults = {
            'strapelido': f"ACAO-{timezone.now().strftime('%Y%m%d%H%M%S%f')}",
            'strdescricaoacao': 'Ação Base para Testes',
            'strdescricaoentrega': 'Entrega Base',
            'idvigenciapngi': self.vigencia_base,
            'ideixo': self.eixo_base,  # ← SEMPRE PRESENTE
            'idsituacaoacao': self.situacao_base,  # ← SEMPRE PRESENTE
        }
        
        # Sobrescrever com valores customizados
        defaults.update(kwargs)
        
        return Acoes.objects.create(**defaults)


class BaseAPITestCase(TestCase):
    """
    Classe base para testes de API (DRF) do módulo acoes_pngi.
    
    Fornece:
        - Tudo do BaseTestCase
        - Cliente REST Framework configurado
        - Helpers para autenticação de API
    """
    databases = {'default', 'gpp_plataform_db'}
    
    @classmethod
    def setUpClass(cls):
        """Configuração executada UMA VEZ por classe de teste"""
        super().setUpClass()
        
        # Criar dados base compartilhados
        base_data = create_base_test_data()
        cls.eixo_base = base_data.eixo
        cls.situacao_base = base_data.situacao
        cls.vigencia_base = base_data.vigencia
        
        # Aplicacao PNGI - importar de accounts
        try:
            from accounts.models import Aplicacao
            cls.app, _ = Aplicacao.objects.using('gpp_plataform_db').get_or_create(
                codigointerno='ACOES_PNGI',
                defaults={'descricao': 'Sistema de Ações PNGI'}
            )
        except (ImportError, Exception) as e:
            print(f"Aviso: Não foi possível carregar Aplicacao: {e}")
            cls.app = None
    
    def create_acao_base(self, **kwargs):
        """
        Factory method para criar ações sempre completas.
        
        Args:
            **kwargs: Campos customizados para sobrescrever padrões
        
        Returns:
            Acoes: Instância de ação criada com todos os campos obrigatórios
        """
        from acoes_pngi.models import Acoes
        
        defaults = {
            'strapelido': f"ACAO-{timezone.now().strftime('%Y%m%d%H%M%S%f')}",
            'strdescricaoacao': 'Ação Base para Testes',
            'strdescricaoentrega': 'Entrega Base',
            'idvigenciapngi': self.vigencia_base,
            'ideixo': self.eixo_base,
            'idsituacaoacao': self.situacao_base,
        }
        
        defaults.update(kwargs)
        
        return Acoes.objects.create(**defaults)

    def get_api_results(self, response):
        """Extrai results de response paginada ou lista direta"""
        if 'results' in response.data:
            return response.data['results'], response.data['count']
        return response.data, len(response.data)