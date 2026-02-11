# Generated migration for complete RBAC setup

from django.db import migrations
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


def create_complete_permissions(apps, schema_editor):
    """
    Cria RolePermissions completas para ACOES_PNGI.
    
    Hierarquia:
    - GESTOR_PNGI: CRUD em tudo (44 permissões)
    - COORDENADOR_PNGI: view configs + CRUD negócio/filhas (29 permissões)
    - OPERADOR_ACAO: view configs/negócio + add/view filhas (15 permissões)
    - CONSULTOR_PNGI: view tudo (11 permissões)
    """
    Aplicacao = apps.get_model('accounts', 'Aplicacao')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')
    
    # Buscar aplicação
    try:
        app_acoes = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
    except Aplicacao.DoesNotExist:
        print("⚠️  Aplicação ACOES_PNGI não encontrada. Pulando migration...")
        return
    
    # Classificação de modelos
    models_config = {
        'CONFIGURAÇÕES/TIPOS': [
            ('acoes_pngi', 'eixo'),
            ('acoes_pngi', 'situacaoacao'),
            ('acoes_pngi', 'vigenciapngi'),
            ('acoes_pngi', 'tipoanotacaoalinhamento'),
            ('acoes_pngi', 'tipoentravealerta'),
        ],
        'NEGÓCIO': [
            ('acoes_pngi', 'acoes'),
            ('acoes_pngi', 'usuarioresponsavel'),
        ],
        'FILHAS': [
            ('acoes_pngi', 'acaoprazo'),
            ('acoes_pngi', 'acaodestaque'),
            ('acoes_pngi', 'acaoanotacaoalinhamento'),
            ('acoes_pngi', 'relacaoacaousuarioresponsavel'),
        ]
    }
    
    actions = ['add', 'change', 'delete', 'view']
    
    # Criar/obter todas as permissões
    permissions_by_model = {}
    total_created = 0
    
    print("\n🔧 Criando permissões...")
    for category, model_list in models_config.items():
        for app_label, model_name in model_list:
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name)
                permissions_by_model[model_name] = {}
                
                for action in actions:
                    codename = f'{action}_{model_name}'
                    perm, created = Permission.objects.get_or_create(
                        codename=codename,
                        content_type=ct,
                        defaults={'name': f'Can {action} {model_name}'}
                    )
                    permissions_by_model[model_name][action] = perm
                    if created:
                        total_created += 1
                        print(f"  ✅ Criada: {codename}")
                
            except ContentType.DoesNotExist:
                print(f"  ⚠️  ContentType para {app_label}.{model_name} não encontrado")
                continue
    
    if total_created > 0:
        print(f"\n✅ {total_created} novas permissões criadas")
    else:
        print("\n✅ Todas as permissões já existiam")
    
    # Hierarquia de permissões por role
    roles_hierarchy = {
        'GESTOR_PNGI': {
            'CONFIGURAÇÕES/TIPOS': ['add', 'change', 'delete', 'view'],
            'NEGÓCIO': ['add', 'change', 'delete', 'view'],
            'FILHAS': ['add', 'change', 'delete', 'view'],
        },
        'COORDENADOR_PNGI': {
            'CONFIGURAÇÕES/TIPOS': ['view'],
            'NEGÓCIO': ['add', 'change', 'delete', 'view'],
            'FILHAS': ['add', 'change', 'delete', 'view'],
        },
        'OPERADOR_ACAO': {
            'CONFIGURAÇÕES/TIPOS': ['view'],
            'NEGÓCIO': ['view'],
            'FILHAS': ['add', 'view'],
        },
        'CONSULTOR_PNGI': {
            'CONFIGURAÇÕES/TIPOS': ['view'],
            'NEGÓCIO': ['view'],
            'FILHAS': ['view'],
        }
    }
    
    # Vincular permissões às roles
    print("\n🔗 Vinculando RolePermissions...")
    
    for role_code, categories in roles_hierarchy.items():
        try:
            role = Role.objects.get(aplicacao=app_acoes, codigoperfil=role_code)
            role_perms_created = 0
            
            for category, allowed_actions in categories.items():
                model_list = models_config[category]
                
                for app_label, model_name in model_list:
                    if model_name not in permissions_by_model:
                        continue
                    
                    for action in allowed_actions:
                        if action in permissions_by_model[model_name]:
                            perm = permissions_by_model[model_name][action]
                            _, created = RolePermission.objects.get_or_create(
                                role=role,
                                permission=perm
                            )
                            if created:
                                role_perms_created += 1
            
            print(f"  ✅ {role_code}: {role_perms_created} novas RolePermissions")
            
        except Role.DoesNotExist:
            print(f"  ⚠️  Role {role_code} não encontrada. Criá-la primeiro!")
            continue
    
    print("\n🎉 Migração concluída com sucesso!")


def remove_all_permissions(apps, schema_editor):
    """
    Rollback: Remove todas as RolePermissions criadas para ACOES_PNGI.
    Mantém as Permissions (Django as gerencia automaticamente).
    """
    Aplicacao = apps.get_model('accounts', 'Aplicacao')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')
    
    try:
        app_acoes = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
        roles = Role.objects.filter(aplicacao=app_acoes)
        deleted_count = RolePermission.objects.filter(role__in=roles).delete()[0]
        print(f"🗑️  {deleted_count} RolePermissions removidas (rollback)")
    except Aplicacao.DoesNotExist:
        print("⚠️  Aplicação não encontrada, nada a reverter")


class Migration(migrations.Migration):

    dependencies = [
        ('acoes_pngi', '0003_acaoanotacaoalinhamento_acaodestaque_acaoprazo_acoes_and_more'),
        ('accounts', '0004_rolepermission'),
    ]

    operations = [
        migrations.RunPython(create_complete_permissions, remove_all_permissions),
    ]
