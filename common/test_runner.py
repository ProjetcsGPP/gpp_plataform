# common/test_runner.py
from django.test.runner import DiscoverRunner
from django.db import connection


class GPPTestRunner(DiscoverRunner):
    """
    Test runner customizado para GPP Platform
    Cria schemas necessários antes de executar migrations
    """
    
    def setup_databases(self, **kwargs):
        """
        Configura banco de dados de teste com schemas customizados
        """
        # Primeiro, criar o banco e rodar migrations normalmente
        old_config = super().setup_databases(**kwargs)
        
        # Depois, criar schemas adicionais e popular dados essenciais
        with connection.cursor() as cursor:
            try:
                if self.verbosity >= 1:
                    self.log("\n=== Configurando schemas de teste ===")
                
                # Criar schemas customizados
                cursor.execute("CREATE SCHEMA IF NOT EXISTS acoes_pngi;")
                cursor.execute("CREATE SCHEMA IF NOT EXISTS carga_org_lot;")
                
                if self.verbosity >= 1:
                    self.log("✓ Schemas criados")
                
                # Popular tblaplicacao se existir
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'tblaplicacao'
                    );
                """)
                
                if cursor.fetchone()[0]:
                    if self.verbosity >= 1:
                        self.log("✓ Populando tblaplicacao...")
                    
                    cursor.execute("""
                        INSERT INTO tblaplicacao (idaplicacao, codigointerno, nomeaplicacao, base_url, isshowinportal)
                        VALUES 
                            (1, 'PORTAL', 'Portal GPP', 'http://localhost:8000', true),
                            (2, 'ACOES_PNGI', 'Ações PNGI', 'http://localhost:8001', true),
                            (3, 'CARGA_ORG_LOT', 'Carga Org/Lot', 'http://localhost:8002', true)
                        ON CONFLICT (idaplicacao) DO NOTHING;
                    """)
                    
                    if self.verbosity >= 1:
                        self.log("✓ Dados populados")
                
                if self.verbosity >= 1:
                    self.log("✓ Ambiente de testes configurado!\n")
                
            except Exception as e:
                if self.verbosity >= 1:
                    self.log(f"⚠ Aviso ao configurar ambiente: {e}\n")
        
        return old_config
