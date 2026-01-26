from django.test import TestCase
from django.db import connection


class CargaOrgLotTestCase(TestCase):
    """
    Classe base para testes do app carga_org_lot.
    Cria as tabelas necessárias no banco de testes pois os models têm managed=False.
    """
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # SQL para criar o schema e as tabelas no banco de testes
        with connection.cursor() as cursor:
            # Criar schema se não existir
            cursor.execute("CREATE SCHEMA IF NOT EXISTS carga_org_lot;")
            
            # Criar tabelas (versão simplificada para testes)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS carga_org_lot.tblstatusprogresso (
                    idstatusprogresso SMALLINT PRIMARY KEY,
                    strdescricao VARCHAR(100)
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS carga_org_lot.tblpatriarca (
                    idpatriarca BIGSERIAL PRIMARY KEY,
                    idexternopatriarca UUID UNIQUE,
                    strsiglapatriarca VARCHAR(20),
                    strnome VARCHAR(255),
                    idstatusprogresso SMALLINT REFERENCES carga_org_lot.tblstatusprogresso(idstatusprogresso),
                    datcriacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    idusuariocriacao BIGINT,
                    datalteracao TIMESTAMP,
                    idusuarioalteracao BIGINT
                );
            """)
            
            # Adicione mais CREATE TABLE conforme necessário...
            # Ou use managed=True temporariamente para gerar as tabelas
