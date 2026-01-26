# carga_org_lot/migrations/0003_fix_schema_tables.py
from django.db import migrations


def populate_status_progresso(apps, schema_editor):
    """Popula status de progresso"""
    TblStatusProgresso = apps.get_model('carga_org_lot', 'TblStatusProgresso')
    
    status_list = [
        {'id_status_progresso': 1, 'str_descricao': 'Nova Carga'},
        {'id_status_progresso': 2, 'str_descricao': 'Processando'},
        {'id_status_progresso': 3, 'str_descricao': 'Concluído'},
        {'id_status_progresso': 4, 'str_descricao': 'Erro'},
    ]
    
    for status_data in status_list:
        TblStatusProgresso.objects.get_or_create(
            id_status_progresso=status_data['id_status_progresso'],
            defaults={'str_descricao': status_data['str_descricao']}
        )


def populate_status_token(apps, schema_editor):
    """Popula status de token"""
    TblStatusTokenEnvioCarga = apps.get_model('carga_org_lot', 'TblStatusTokenEnvioCarga')
    
    status_list = [
        {'id_status_token_envio_carga': 1, 'str_descricao': 'Ativo'},
        {'id_status_token_envio_carga': 2, 'str_descricao': 'Expirado'},
        {'id_status_token_envio_carga': 3, 'str_descricao': 'Cancelado'},
    ]
    
    for status_data in status_list:
        TblStatusTokenEnvioCarga.objects.get_or_create(
            id_status_token_envio_carga=status_data['id_status_token_envio_carga'],
            defaults={'str_descricao': status_data['str_descricao']}
        )


def populate_status_carga(apps, schema_editor):
    """Popula status de carga"""
    TblStatusCarga = apps.get_model('carga_org_lot', 'TblStatusCarga')
    
    status_list = [
        {'id_status_carga': 1, 'str_descricao': 'Pendente', 'flg_sucesso': 0},
        {'id_status_carga': 2, 'str_descricao': 'Processando', 'flg_sucesso': 0},
        {'id_status_carga': 3, 'str_descricao': 'Sucesso', 'flg_sucesso': 1},
        {'id_status_carga': 4, 'str_descricao': 'Erro', 'flg_sucesso': 0},
        {'id_status_carga': 5, 'str_descricao': 'Cancelado', 'flg_sucesso': 0},
    ]
    
    for status_data in status_list:
        TblStatusCarga.objects.get_or_create(
            id_status_carga=status_data['id_status_carga'],
            defaults={
                'str_descricao': status_data['str_descricao'],
                'flg_sucesso': status_data['flg_sucesso']
            }
        )


def populate_tipo_carga(apps, schema_editor):
    """Popula tipos de carga"""
    TblTipoCarga = apps.get_model('carga_org_lot', 'TblTipoCarga')
    
    tipos_list = [
        {'id_tipo_carga': 1, 'str_descricao': 'Organograma'},
        {'id_tipo_carga': 2, 'str_descricao': 'Lotação'},
    ]
    
    for tipo_data in tipos_list:
        TblTipoCarga.objects.get_or_create(
            id_tipo_carga=tipo_data['id_tipo_carga'],
            defaults={'str_descricao': tipo_data['str_descricao']}
        )


def reverse_populate(apps, schema_editor):
    """Remove dados populados"""
    TblStatusProgresso = apps.get_model('carga_org_lot', 'TblStatusProgresso')
    TblStatusTokenEnvioCarga = apps.get_model('carga_org_lot', 'TblStatusTokenEnvioCarga')
    TblStatusCarga = apps.get_model('carga_org_lot', 'TblStatusCarga')
    TblTipoCarga = apps.get_model('carga_org_lot', 'TblTipoCarga')
    
    TblStatusProgresso.objects.all().delete()
    TblStatusTokenEnvioCarga.objects.all().delete()
    TblStatusCarga.objects.all().delete()
    TblTipoCarga.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('carga_org_lot', '0002_alter_tblcargapatriarca_options_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                'CREATE SCHEMA IF NOT EXISTS carga_org_lot;',
                'SET search_path TO carga_org_lot, public;',
            ],
            reverse_sql=[
                'SET search_path TO public;',
            ]
        ),
        migrations.RunPython(populate_status_progresso, reverse_populate),
        migrations.RunPython(populate_status_token, reverse_populate),
        migrations.RunPython(populate_status_carga, reverse_populate),
        migrations.RunPython(populate_tipo_carga, reverse_populate),
    ]

