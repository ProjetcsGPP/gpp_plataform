from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Corrige sequências do PostgreSQL após inserções manuais'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Lista de tabelas que têm auto-increment
            tables = [
                ('accounts_role', 'id'),
                ('accounts_userrole', 'id'),
                ('accounts_rolepermission', 'id'),
                ('tblaplicacao', 'idaplicacao'),
            ]
            
            for table, pk_field in tables:
                try:
                    # Buscar o nome da sequência
                    cursor.execute(f"""
                        SELECT pg_get_serial_sequence('{table}', '{pk_field}')
                    """)
                    result = cursor.fetchone()
                    
                    if result and result[0]:
                        seq_name = result[0].split('.')[-1].strip('"')
                        
                        # Buscar o maior ID atual
                        cursor.execute(f"SELECT MAX({pk_field}) FROM {table}")
                        max_id = cursor.fetchone()[0]
                        
                        if max_id is None:
                            max_id = 0
                        
                        # Atualizar a sequência
                        cursor.execute(f"SELECT setval('{seq_name}', {max_id})")
                        
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ {table}: sequência ajustada para {max_id}'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'⚠ {table}: sequência não encontrada'
                            )
                        )
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ {table}: {str(e)}')
                    )
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sequências corrigidas!'))
