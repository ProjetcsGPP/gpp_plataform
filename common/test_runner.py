# common/test_runner.py
from django.test.runner import DiscoverRunner
from django.db import connection

class GPPTestRunner(DiscoverRunner):
    """
    Test runner customizado para GPP Platform
    Cria schemas e dados essenciais antes de rodar migrations
    """
    
    def setup_databases(self, **kwargs):
        """Configura banco de dados de teste com schemas e dados essenciais"""
        
        # Primeiro, deixa o Django criar o banco e rodar migrations básicas
        old_config = super().setup_databases(**kwargs)
        
        # Agora cria schemas e dados essenciais
        with connection.cursor() as cursor:
            try:
                print("\n=== Configurando ambiente de testes ===")
                
                # 1. Criar schemas
                print("✓ Criando schemas...")
                cursor.execute("CREATE SCHEMA IF NOT EXISTS acoes_pngi;")
                cursor.execute("CREATE SCHEMA IF NOT EXISTS carga_org_lot;")
                
                # 2. Inserir dados essenciais na tblaplicacao (se existir)
                print("✓ Verificando tblaplicacao...")
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'tblaplicacao'
                    );
                """)
                
                if cursor.fetchone()[0]:
                    print("✓ Populando dados essenciais...")
                    # Inserir aplicações básicas
                    cursor.execute("""
                        INSERT INTO tblaplicacao (idaplicacao, straplicacao, strurl)
                        VALUES 
                            (1, 'Portal', 'http://localhost:8000'),
                            (2, 'Ações PNGI', 'http://localhost:8001'),
                            (3, 'Carga Org/Lot', 'http://localhost:8002')
                        ON CONFLICT (idaplicacao) DO NOTHING;
                    """)
                
                print("✓ Ambiente de testes configurado com sucesso!\n")
                
            except Exception as e:
                print(f"⚠ Aviso ao configurar ambiente de testes: {e}")
        
        return old_config
