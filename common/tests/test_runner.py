# common/test_runner.py
from django.test.runner import DiscoverRunner
from django.db import connection

class CustomTestRunner(DiscoverRunner):
    """Test runner que cria schemas necessários antes dos testes"""
    
    def setup_databases(self, **kwargs):
        """Setup banco de dados de teste com schemas"""
        old_config = super().setup_databases(**kwargs)
        
        # Criar schemas necessários
        with connection.cursor() as cursor:
            try:
                cursor.execute("CREATE SCHEMA IF NOT EXISTS acoes_pngi;")
                cursor.execute("CREATE SCHEMA IF NOT EXISTS carga_org_lot;")
                print("✓ Schemas criados com sucesso")
            except Exception as e:
                print(f"Aviso ao criar schemas: {e}")
        
        return old_config
