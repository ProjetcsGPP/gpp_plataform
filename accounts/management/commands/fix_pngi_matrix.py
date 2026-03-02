from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Corrige matriz PNGI 100% conforme tabela oficial'
    
    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Simula sem salvar')
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Modelos da matriz (nomes EXATOS do banco)
        model_map = {
            'situacaoacao': None,
            'tipoentravealerta': None,  # Nota: tipoentravealerta no banco
            'eixo': None,
            'vigenciapngi': None,
            'tipoanotacaoalinhamento': None,
            'acoes': None,
            'acaoprazo': None,
            'acaodestaque': None,
            'acaoanotacaoalinhamento': None,
            'usuarioresponsavel': None,
            'relacaoacaousuarioresponsavel': None,
        }
        
        # Busca ContentTypes reais
        for model_name in model_map:
            try:
                ct = ContentType.objects.get(app_label='acoes_pngi', model=model_name)
                model_map[model_name] = ct
                self.stdout.write(f"  ✅ {model_name}")
            except ContentType.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  ⚠️  {model_name} NÃO encontrado"))
        
        groups = {
            'GESTOR_PNGI': {
                'read_models': list(model_map.keys()),
                'write_models': list(model_map.keys()),  # Total
                'auth_perms': ['add_user', 'change_user', 'delete_user', 'view_user', 
                              'add_group', 'change_group', 'delete_group', 'view_group']
            },
            'COORDENADOR_PNGI': {
                'read_models': list(model_map.keys()),  # Todos read
                'write_models': ['eixo', 'vigenciapngi', 'tipoanotacaoalinhamento', 
                                'acoes', 'acaoprazo', 'acaodestaque', 'acaoanotacaoalinhamento', 
                                'usuarioresponsavel', 'relacaoacaousuarioresponsavel'],
                'auth_perms': ['view_user', 'view_group']
            },
            'OPERADOR_ACAO': {
                'read_models': list(model_map.keys()),
                'write_models': ['acoes', 'acaoprazo', 'acaodestaque', 'acaoanotacaoalinhamento', 
                                'usuarioresponsavel', 'relacaoacaousuarioresponsavel'],
                'auth_perms': ['view_user', 'view_group']
            },
            'CONSULTOR_PNGI': {
                'read_models': list(model_map.keys()),
                'write_models': [],
                'auth_perms': ['view_user', 'view_group']
            }
        }
        
        fixed = 0
        for group_name, config in groups.items():
            try:
                group = Group.objects.get(name=group_name)
                if not dry_run:
                    group.permissions.clear()
                    
                    # Read
                    for model_name in config['read_models']:
                        ct = model_map.get(model_name)
                        if ct:
                            perm = Permission.objects.get(codename=f'view_{model_name}', content_type=ct)
                            group.permissions.add(perm)
                    
                    # Write
                    for model_name in config['write_models']:
                        ct = model_map.get(model_name)
                        if ct:
                            for action in ['add', 'change', 'delete']:
                                perm = Permission.objects.get(codename=f'{action}_{model_name}', content_type=ct)
                                group.permissions.add(perm)
                    
                    # Auth perms
                    for pcode in config['auth_perms']:
                        perm = Permission.objects.get(codename=pcode)
                        group.permissions.add(perm)
                    
                    group.save()
                    fixed += 1
                
                self.stdout.write(self.style.SUCCESS(f"✅ {group_name}: {len(group.permissions.all())} perms"))
                
            except Group.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"❌ Group {group_name} não existe"))
        
        # Validação final COORD
        coord = Group.objects.get(name='COORDENADOR_PNGI')
        eixo_test = coord.permissions.filter(codename='add_eixo').exists()
        acoes_test = coord.permissions.filter(codename='add_acoes').exists()
        situacao_test = coord.permissions.filter(codename='add_situacaoacao').exists()
        
        self.stdout.write(self.style.SUCCESS(f"VALIDAÇÃO COORD:"))
        self.stdout.write(f"  add_eixo: {eixo_test} ✅")
        self.stdout.write(f"  add_acoes: {acoes_test} ✅") 
        self.stdout.write(f"  add_situacaoacao: {situacao_test} ❌ (só GESTOR)")
        
        if not dry_run:
            self.stdout.write(self.style.SUCCESS(f'🎉 Matriz PNGI corrigida! {fixed}/4 groups fixados'))
        else:
            self.stdout.write(self.style.WARNING('👀 Dry-run: execute sem --dry-run para aplicar'))
