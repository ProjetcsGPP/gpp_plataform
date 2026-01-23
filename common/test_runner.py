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
                    
                    # Inserir ou atualizar aplicações
                    cursor.execute("""
                        INSERT INTO tblaplicacao (codigointerno, nomeaplicacao, base_url, isshowinportal)
                        VALUES 
                            ('PORTAL', 'Portal GPP', 'http://127.0.0.1:8000/portal/', false),
                            ('CARGA_ORG_LOT', 'Carga Única de Organograma e Lotação', 'http://127.0.0.1:8000/carga_org_lot/', true),
                            ('ACOES_PNGI', 'Ações PNGI', 'http://127.0.0.1:8000/acoes-pngi/', true)
                        ON CONFLICT (codigointerno) DO UPDATE SET
                            nomeaplicacao = EXCLUDED.nomeaplicacao,
                            base_url = EXCLUDED.base_url,
                            isshowinportal = EXCLUDED.isshowinportal;
                    """)
                    
                    # Buscar os IDs reais das aplicações criadas
                    cursor.execute("""
                        SELECT idaplicacao, codigointerno FROM tblaplicacao 
                        WHERE codigointerno IN ('PORTAL', 'CARGA_ORG_LOT', 'ACOES_PNGI')
                        ORDER BY codigointerno;
                    """)
                    
                    app_ids = {row[1]: row[0] for row in cursor.fetchall()}
                    
                    if self.verbosity >= 1:
                        self.log(f"✓ Aplicações populadas: {app_ids}")
                    
                    # Popular accounts_role com os IDs reais
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_schema = 'public' 
                            AND table_name = 'accounts_role'
                        );
                    """)
                    
                    if cursor.fetchone()[0]:
                        if self.verbosity >= 1:
                            self.log("✓ Populando accounts_role...")
                        
                        # Usar os IDs reais das aplicações
                        portal_id = app_ids.get('PORTAL')
                        carga_id = app_ids.get('CARGA_ORG_LOT')
                        acoes_id = app_ids.get('ACOES_PNGI')
                        
                        if portal_id and carga_id and acoes_id:
                            cursor.execute("""
                                INSERT INTO accounts_role (nomeperfil, codigoperfil, aplicacao_id)
                                VALUES 
                                    ('Usuário do Portal', 'USER_PORTAL', %s),
                                    ('Gestor Carga Org/Lot', 'GESTOR_CARGA', %s),
                                    ('Gestor Ações PNGI', 'GESTOR_PNGI', %s)
                                ON CONFLICT (aplicacao_id, codigoperfil) DO UPDATE SET
                                    nomeperfil = EXCLUDED.nomeperfil;
                            """, [portal_id, carga_id, acoes_id])
                            
                            # Verificar roles criadas
                            cursor.execute("""
                                SELECT id, codigoperfil, aplicacao_id 
                                FROM accounts_role 
                                WHERE aplicacao_id IN (%s, %s, %s)
                                ORDER BY aplicacao_id;
                            """, [portal_id, carga_id, acoes_id])
                            
                            roles = cursor.fetchall()
                            if self.verbosity >= 1:
                                self.log(f"✓ Roles criadas: {roles}")
                        else:
                            if self.verbosity >= 1:
                                self.log("⚠ Não foi possível obter IDs de todas as aplicações")
                    else:
                        if self.verbosity >= 1:
                            self.log("⚠ Tabela accounts_role não encontrada")
                
                if self.verbosity >= 1:
                    self.log("✓ Ambiente de testes configurado!\n")
                
            except Exception as e:
                if self.verbosity >= 1:
                    self.log(f"⚠ Erro ao configurar ambiente: {e}\n")
                import traceback
                if self.verbosity >= 1:
                    self.log(traceback.format_exc())
        
        return old_config
