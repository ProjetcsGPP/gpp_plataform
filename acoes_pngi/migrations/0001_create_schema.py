# acoes_pngi/migrations/0001_create_schema.py
from django.db import migrations

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            sql='CREATE SCHEMA IF NOT EXISTS acoes_pngi;',
            reverse_sql='DROP SCHEMA IF EXISTS acoes_pngi CASCADE;'
        ),
    ]
