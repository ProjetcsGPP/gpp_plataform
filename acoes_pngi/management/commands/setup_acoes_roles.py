# acoes_pngi/management/commands/setup_acoes_roles.py
"""
Command atualizado para usar auth_group nativo do Django.

✅ Remove RolePermission completamente
✅ Usa auth_group_permissions
✅ Matriz de permissões da migration 0006
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from accounts.models import Role, Aplicacao


class Command(BaseCommand):
    help = 'Configura roles e permissões PNGI usando auth_group NATIVO'

    def handle(self, *args, **kwargs):
        # Buscar aplicação PNGI
        try:
            app = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
        except Aplicacao.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Aplicação ACOES_PNGI não encontrada!'))
            return
        
        app_code = app.codigointerno
        self.stdout.write(self.style.SUCCESS(f'🎯 Configurando {app_code}...'))
        
        # MATRIZ CORRIGIDA (igual migration 0006)
        roles_config = {
            'GESTOR_PNGI': {
                'nome': 'Gestor PNGI - Acesso Total',
                'nivel1': True,  # situacaoacao, tipoentravealerta W/D
                'nivel2': True,  # eixo, vigenciapngi, tipoanotacao W/D
                'operacoes': True,  # acoes, prazos, etc W/D
                'iam_gestao': True,
            },
            'COORDENADOR_PNGI': {
                'nome': 'Coordenador - Gerencia Configurações',
                'nivel1': False,  # Apenas leitura
                'nivel2': True,
                'operacoes': True,
                'iam_gestao': False,
            },
            'OPERADOR_ACAO': {
                'nome': 'Operador - Apenas Ações',
                'nivel1': False,
                'nivel2': False,
                'operacoes': True,
                'iam_gestao': False,
            },
            'CONSULTOR_PNGI': {
                'nome': 'Consultor - Apenas Leitura',
                'nivel1': False,
                'nivel2': False,
                'operacoes': False,
                'iam_gestao': False,
            }
        }
        
        # ContentTypes necessários
        content_types = {
            'accounts': {
                'user': ContentType.objects.get(app_label='accounts', model='user'),
                'role': ContentType.objects.get(app_label='accounts', model='role'),
                'userrole': ContentType.objects.get(app_label='accounts', model='userrole'),
                'aplicacao': ContentType.objects.get(app_label='accounts', model='aplicacao'),
                'attribute': ContentType.objects.get(app_label='accounts', model='attribute'),
            },
            'acoes_pngi': {
                'situacaoacao': ContentType.objects.get(app_label='acoes_pngi', model='situacaoacao'),
                'tipoentravealerta': ContentType.objects.get(app_label='acoes_pngi', model='tipoentravealerta'),
                'eixo': ContentType.objects.get(app_label='acoes_pngi', model='eixo'),
                'vigenciapngi': ContentType.objects.get(app_label='acoes_pngi', model='vigenciapngi'),
                'tipoanotacaoalinhamento': ContentType.objects.get(app_label='acoes_pngi', model='tipoanotacaoalinhamento'),
                'acoes': ContentType.objects.get(app_label='acoes_pngi', model='acoes'),
                'acaoprazo': ContentType.objects.get(app_label='acoes_pngi', model='acaoprazo'),
                'acaodestaque': ContentType.objects.get(app_label='acoes_pngi', model='acaodestaque'),
                'acaoanotacaoalinhamento': ContentType.objects.get(app_label='acoes_pngi', model='acaoanotacaoalinhamento'),
                'usuarioresponsavel': ContentType.objects.get(app_label='acoes_pngi', model='usuarioresponsavel'),
                'relacaoacaousuarioresponsavel': ContentType.objects.get(app_label='acoes_pngi', model='relacaoacaousuarioresponsavel'),
            }
        }
        
        total_perms = 0
        
        for codigo, config in roles_config.items():
            # 1. Criar/atualizar Role (accounts_role)
            role, created = Role.objects.get_or_create(
                aplicacao=app,
                codigoperfil=codigo,
                defaults={'nomeperfil': config['nome']}
            )
            
            status = '🆕 CRIADA' if created else '🔄 ATUALIZADA'
            self.stdout.write(f'\n{status}: {codigo}')
            
            # 2. Grupo Django (auth_group)
            group_name = f"{app_code}_{codigo}"
            group, _ = Group.objects.get_or_create(name=group_name)
            
            # 3. Configurar permissões nativas
            perms_list = []
            
            # NÍVEL 1 - Configurações Críticas
            if config['nivel1']:
                for model in ['situacaoacao', 'tipoentravealerta']:
                    perms_list.extend([
                        f"add_{model}", f"change_{model}", f"delete_{model}", f"view_{model}"
                    ])
            else:
                perms_list.extend(['view_situacaoacao', 'view_tipoentravealerta'])
            
            # NÍVEL 2 - Configurações Compartilhadas
            if config['nivel2']:
                for model in ['eixo', 'vigenciapngi', 'tipoanotacaoalinhamento']:
                    perms_list.extend([
                        f"add_{model}", f"change_{model}", f"delete_{model}", f"view_{model}"
                    ])
            else:
                perms_list.extend([
                    'view_eixo', 'view_vigenciapngi', 'view_tipoanotacaoalinhamento'
                ])
            
            # OPERAÇÕES
            if config['operacoes']:
                for model in ['acoes', 'acaoprazo', 'acaodestaque', 'acaoanotacaoalinhamento',
                            'usuarioresponsavel', 'relacaoacaousuarioresponsavel']:
                    perms_list.extend([
                        f"add_{model}", f"change_{model}", f"delete_{model}", f"view_{model}"
                    ])
            else:
                for model in ['acoes', 'acaoprazo', 'acaodestaque', 'acaoanotacaoalinhamento',
                            'usuarioresponsavel', 'relacaoacaousuarioresponsavel']:
                    perms_list.append(f"view_{model}")
            
            # IAM
            perms_list.extend(['view_user', 'view_role', 'view_userrole', 'view_aplicacao', 'view_attribute'])
            if config['iam_gestao']:
                perms_list.extend(['add_user', 'change_user', 'delete_user'])
                perms_list.extend(['add_userrole', 'change_userrole', 'delete_userrole'])
                perms_list.extend(['add_attribute', 'change_attribute', 'delete_attribute'])
            
            # Buscar e aplicar permissões
            perms_found = []
            for codename in set(perms_list):  # Remover duplicatas
                try:
                    perm = Permission.objects.get(codename=codename)
                    perms_found.append(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'   ⚠ {codename}'))
            
            # Aplicar ao grupo
            group.permissions.set(perms_found)
            total_perms += len(perms_found)
            
            self.stdout.write(f'   📊 {len(perms_found)} permissões nativas')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Setup concluído! {total_perms} perms totais'))
        
        # Resumo final
        self.stdout.write('\n📊 RESUMO FINAL (auth_group):')
        for group in Group.objects.filter(name__startswith=f'{app_code}_'):
            count = group.permissions.count()
            self.stdout.write(f'   {group.name}: {count} perms')
