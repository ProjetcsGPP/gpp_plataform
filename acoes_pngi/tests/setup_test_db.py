from django.db import connection

def create_acoes_pngi_tables():
    """Cria as tabelas do schema acoes_pngi no banco de teste"""
    with connection.cursor() as cursor:
        # Criar schema se não existir
        cursor.execute("CREATE SCHEMA IF NOT EXISTS acoes_pngi;")
        
        # Criar tabela tbleixos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS acoes_pngi.tbleixos (
                ideixo SERIAL PRIMARY KEY,
                strdescricaoeixo VARCHAR(100) NOT NULL,
                stralias VARCHAR(5) UNIQUE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)
        
        # Criar tabela tblsituacaoacao
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS acoes_pngi.tblsituacaoacao (
                idsituacaoacao SERIAL PRIMARY KEY,
                strdescricaosituacao VARCHAR(15) UNIQUE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)
        
        # Criar tabela tblvigenciapngi
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS acoes_pngi.tblvigenciapngi (
                idvigenciapngi SERIAL PRIMARY KEY,
                strdescricaovigenciapngi VARCHAR(100) NOT NULL,
                datiniciovigencia DATE NOT NULL,
                datfinalvigencia DATE NOT NULL,
                isvigenciaativa BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)
