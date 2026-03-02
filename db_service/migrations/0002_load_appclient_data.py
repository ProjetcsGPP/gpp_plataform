# db_service/migrations/0002_load_appclient_data.py
from django.db import migrations

def load_appclients(apps, schema_editor):
    AppClient = apps.get_model('db_service', 'AppClient')
    data = [
        {
            'id': 1,
            'client_id': 'portal_gpp_client',
            'client_secret_hash': 'pbkdf2_sha256$1200000$7WXToFpeRmW81wl0R9FLtD$xSDYXHT/RO0Kaoke71BSSoM+j8lIpIfj4A5IpVAkxSA=',
            'is_active': True,
            'aplicacao_id': 1
        },
        {
            'id': 2,
            'client_id': 'carga_org_lot_client',
            'client_secret_hash': 'pbkdf2_sha256$1200000$9Vy7iHSdCt94zh6zD3OYx2$o1T0B9EzLPDT+rHLWDuqntTU4wJv3ENQwaHwwAqe1x8=',
            'is_active': True,
            'aplicacao_id': 2
        },
        {
            'id': 3,
            'client_id': 'acoes_pngi_client',
            'client_secret_hash': 'pbkdf2_sha256$1200000$XEmLDIpCgtfcb1A7Oim59a$/4j2WVglFJsp5DtceTXjW7guRBgJL+GAtAAy9yBhhX4=',
            'is_active': True,
            'aplicacao_id': 3
        },
    ]
    for item in data:
        AppClient.objects.create(**item)

class Migration(migrations.Migration):
    dependencies = [
        ('db_service', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_appclients, reverse_code=migrations.RunPython.noop),
    ]
