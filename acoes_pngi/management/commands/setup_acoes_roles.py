from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from accounts.models import Role, Aplicacao, RolePermission

class Command(BaseCommand):
    help = 'Configura roles e permissões para Ações PNGI'

    def handle(self, *args, **kwargs):
        # Buscar aplicação
        try:
            app = Aplicacao.objects.get(codigointerno='ACOES_PNGI')
        except Aplicacao.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Aplicação ACOES_PNGI não encontrada!'))
            return
        
        # Definir roles e permissões
        roles_config = {
            'GESTOR_PNGI': {
                'nome': 'Gestor PNGI - Acesso Total',
                'permissions': [
                    'add_eixo', 'change_eixo', 'delete_eixo', 'view_eixo',
                    'add_situacaoacao', 'change_situacaoacao', 'delete_situacaoacao', 'view_situacaoacao',
                    'add_vigenciapngi', 'change_vigenciapngi', 'delete_vigenciapngi', 'view_vigenciapngi',
                ]
            },
            'COORDENADOR_PNGI': {
                'nome': 'Coordenador - Gerencia Configurações',
                'permissions': [
                    'add_eixo', 'change_eixo', 'view_eixo',
                    'add_situacaoacao', 'change_situacaoacao', 'view_situacaoacao',
                    'add_vigenciapngi', 'change_vigenciapngi', 'view_vigenciapngi',
                ]
            },
            'OPERADOR_ACAO': {
                'nome': 'Operador - Apenas Ações',
                'permissions': [
                    'view_eixo',
                    'view_situacaoacao',
                    'view_vigenciapngi',
                ]
            },
            'CONSULTOR_PNGI': {
                'nome': 'Consultor - Apenas Leitura',
                'permissions': [
                    'view_eixo',
                    'view_situacaoacao',
                    'view_vigenciapngi',
                ]
            }
        }

        for codigo, config in roles_config.items():
            # Criar ou buscar role
            role, created = Role.objects.get_or_create(
                aplicacao=app,
                codigoperfil=codigo,
                defaults={'nomeperfil': config['nome']}
            )
            
            status = '🆕 CRIADA' if created else '🔄 ATUALIZADA'
            self.stdout.write(f'\n{status}: {codigo}')
            self.stdout.write(f'   Nome: {config["nome"]}')
            
            # Limpar permissões antigas desta role
            RolePermission.objects.filter(role=role).delete()
            
            # Adicionar permissões
            perms_added = 0
            for codename in config['permissions']:
                try:
                    permission = Permission.objects.get(codename=codename)
                    RolePermission.objects.create(role=role, permission=permission)
                    self.stdout.write(f'   ✓ {codename}')
                    perms_added += 1
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'   ⚠ Permissão não existe: {codename}')
                    )
            
            self.stdout.write(f'   Total: {perms_added} permissões')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Configuração concluída!'))
        
        # Mostrar resumo
        self.stdout.write('\n📊 RESUMO:')
        for role in Role.objects.filter(aplicacao=app):
            count = RolePermission.objects.filter(role=role).count()
            self.stdout.write(f'   {role.codigoperfil}: {count} permissões')
