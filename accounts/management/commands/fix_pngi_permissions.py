# accounts/management/commands/fix_pngi_permissions.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Corrige matriz PNGI 100% - COORD N2+ops, etc.'
    
    def handle(self, *args, **options):
        acoes_cts = ContentType.objects.filter(app_label='acoes_pngi')
        models = {ct.model: ct for ct in acoes_cts}
        
        model_perms = {
            'situacaoacao': models.get('situacaoacao'),
            'tipoentravealerta': models.get('tipoentravealerta'),  # Nota: 'tipoentravealerta' não 'tipoentraveralerta'
            'eixo': models.get('eixo'),
            'vigenciapngi': models.get('vigenciapngi'),
            'tipoanotacaoalinhamento': models.get('tipoanotacaoalinhamento'),
            'acoes': models.get('acoes'),
            'acaoprazo': models.get('acaoprazo'),
            'acaodestaque': models.get('acaodestaque'),
            'acaoanotacaoalinhamento': models.get('acaoanotacaoalinhamento'),
            'usuarioresponsavel': models.get('usuarioresponsavel'),
            'relacaoacaousuarioresponsavel': models.get('relacaoacaousuarioresponsavel'),
        }
        
        # COORD: read ALL + write N2+OPERAÇÕES
        coord = Group.objects.get(name='COORDENADOR_PNGI')
        coord.permissions.clear()
        
        # Read todos
        for ct in model_perms.values():
            if ct:
                view_perm = Permission.objects.get(codename='view_' + ct.model, content_type=ct)
                coord.permissions.add(view_perm)
        
        # Write N2
        n2 = ['eixo', 'vigenciapngi', 'tipoanotacaoalinhamento']
        for model in n2:
            ct = model_perms.get(model)
            if ct:
                for action in ['add', 'change', 'delete']:
                    perm = Permission.objects.get(codename=f'{action}_{model}', content_type=ct)
                    coord.permissions.add(perm)
        
        # Write OPERAÇÕES
        ops = ['acoes', 'acaoprazo', 'acaodestaque', 'acaoanotacaoalinhamento', 'usuarioresponsavel', 'relacaoacaousuarioresponsavel']
        for model in ops:
            ct = model_perms.get(model)
            if ct:
                for action in ['add', 'change', 'delete']:
                    perm = Permission.objects.get(codename=f'{action}_{model}', content_type=ct)
                    coord.permissions.add(perm)
        
        # User/group read
        for pcode in ['view_user', 'view_group']:
            coord.permissions.add(Permission.objects.get(codename=pcode))
        
        self.stdout.write(self.style.SUCCESS('✅ COORDENADOR_PNGI corrigido: N2+ops write'))
        
        # Validação
        self.stdout.write(f"COORD add_eixo: {coord.permissions.filter(codename='add_eixo').exists()}")
        self.stdout.write(f"COORD add_acoes: {coord.permissions.filter(codename='add_acoes').exists()}")
