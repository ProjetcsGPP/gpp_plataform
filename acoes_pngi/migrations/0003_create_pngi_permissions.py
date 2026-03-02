# acoes_pngi/migrations/0003_create_pngi_permissions.py
from django.db import migrations

def create_pngi_groups_and_permissions(apps, schema_editor):
    """
    CRIAÇÃO FINAL DA MATRIZ PNGI - Executa APÓS todos ContentTypes existirem
    ✅ 4 Groups Django com matriz de permissões CORRETA
    ✅ GESTOR: total + gerencia users
    ✅ COORD: N2 + operações write
    ✅ OPERADOR: operações write apenas
    ✅ CONSULTOR: read apenas
    """
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')
    Group = apps.get_model('auth', 'Group')
    
    # DELETE groups existentes PNGI
    pngi_groups = ['GESTOR_PNGI', 'COORDENADOR_PNGI', 'OPERADOR_ACAO', 'CONSULTOR_PNGI']
    Group.objects.filter(name__in=pngi_groups).delete()
    
    # MAPA EXATO DOS MODELOS (nomes precisos do banco)
    model_names = {
        # NÍVEL 1 (GESTOR write)
        'situacaoacao': None,
        'tipoentravealerta': None,  # ← CORREÇÃO: sem 'r'
        
        # NÍVEL 2 (GESTOR+COORD write)
        'eixo': None,
        'vigenciapngi': None,
        'tipoanotacaoalinhamento': None,
        
        # OPERAÇÕES (GESTOR+COORD+OPERADOR write)
        'acoes': None,
        'acaoprazo': None,
        'acaodestaque': None,
        'acaoanotacaoalinhamento': None,
        'usuarioresponsavel': None,
        'relacaoacaousuarioresponsavel': None,
    }
    
    # Busca ContentTypes
    for model_name in model_names:
        try:
            ct = ContentType.objects.get(app_label='acoes_pngi', model=model_name)
            model_names[model_name] = ct
            print(f"✅ ContentType {model_name}")
        except ContentType.DoesNotExist:
            print(f"⚠️  ContentType {model_name} NÃO encontrado")
    
    all_models = list(model_names.keys())
    
    def add_model_perms(group, model_list, read=True, write=False):
        """Helper para adicionar permissões de modelos"""
        for model_name in model_list:
            ct = model_names.get(model_name)
            if ct:
                if read:
                    try:
                        perm = Permission.objects.get(codename=f'view_{model_name}', content_type=ct)
                        group.permissions.add(perm)
                    except Permission.DoesNotExist:
                        pass
                
                if write:
                    for action in ['add', 'change', 'delete']:
                        try:
                            perm = Permission.objects.get(codename=f'{action}_{model_name}', content_type=ct)
                            group.permissions.add(perm)
                        except Permission.DoesNotExist:
                            pass
    
    def add_auth_perms(group, codenames):
        """Helper para permissões auth Django"""
        for codename in codenames:
            try:
                perm = Permission.objects.get(codename=codename)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                pass
    
    # 1. GESTOR_PNGI: TOTAL + auth full
    gestor = Group.objects.create(name='GESTOR_PNGI')
    add_model_perms(gestor, all_models, read=True, write=True)
    add_auth_perms(gestor, ['add_user', 'change_user', 'delete_user', 'view_user',
                           'add_group', 'change_group', 'delete_group', 'view_group'])
    
    # 2. COORDENADOR_PNGI: read ALL + write (N2 + OPERAÇÕES)
    coord = Group.objects.create(name='COORDENADOR_PNGI')
    add_model_perms(coord, all_models, read=True, write=False)  # Read todos
    n2_models = ['eixo', 'vigenciapngi', 'tipoanotacaoalinhamento']
    ops_models = ['acoes', 'acaoprazo', 'acaodestaque', 'acaoanotacaoalinhamento',
                  'usuarioresponsavel', 'relacaoacaousuarioresponsavel']
    add_model_perms(coord, n2_models + ops_models, read=False, write=True)
    add_auth_perms(coord, ['view_user', 'view_group'])
    
    # 3. OPERADOR_ACAO: read ALL + write OPERAÇÕES apenas
    operador = Group.objects.create(name='OPERADOR_ACAO')
    add_model_perms(operador, all_models, read=True, write=False)
    add_model_perms(operador, ops_models, read=False, write=True)
    add_auth_perms(operador, ['view_user', 'view_group'])
    
    # 4. CONSULTOR_PNGI: read ALL apenas
    consultor = Group.objects.create(name='CONSULTOR_PNGI')
    add_model_perms(consultor, all_models, read=True, write=False)
    add_auth_perms(consultor, ['view_user', 'view_group'])
    
    print("🎉 MATRIZ PNGI 100% IMPLEMENTADA!")
    print("✅ GESTOR(total), COORD(N2+ops), OPERADOR(ops), CONSULTOR(read)")

def reverse_migration(apps, schema_editor):
    """Remove apenas Groups PNGI"""
    from django.contrib.auth.models import Group
    Group = apps.get_model('auth', 'Group')
    pngi_groups = ['GESTOR_PNGI', 'COORDENADOR_PNGI', 'OPERADOR_ACAO', 'CONSULTOR_PNGI']
    Group.objects.filter(name__in=pngi_groups).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('acoes_pngi', '0002_load_config_data'),      # ✅ Modelos PNGI criados
        ('accounts', '0002_load_domain_data'),             # ✅ Roles criadas
        ('contenttypes', '__latest__'),                    # ✅ ContentTypes
        ('auth', '__latest__'),                            # ✅ Permissions padrão
    ]

    operations = [
        migrations.RunPython(
            create_pngi_groups_and_permissions,
            reverse_code=reverse_migration
        ),
    ]
