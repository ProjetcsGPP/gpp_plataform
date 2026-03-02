from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Valida matriz PNGI completa'
    
    def handle(self, *args, **options):
        # 1. Verificar 4 Groups PNGI
        pngi_groups = ['GESTOR_PNGI', 'COORDENADOR_PNGI', 'OPERADOR_ACAO', 'CONSULTOR_PNGI']
        groups = Group.objects.filter(name__in=pngi_groups)
        
        if len(groups) != 4:
            self.stdout.write(self.style.ERROR(f'❌ {len(groups)}/4 Groups PNGI'))
            return False
        
        self.stdout.write(self.style.SUCCESS('✅ 4 Groups PNGI OK'))
        
        # 2. Mapa de ContentTypes
        ct_map = {}
        for model in ['acoes', 'eixo', 'situacaoacao']:
            try:
                ct = ContentType.objects.get(app_label='acoes_pngi', model=model)
                ct_map[model] = ct
            except ContentType.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ ContentType acoes_pngi.{model}'))
                return False
        
        # 3. Testes específicos por perfil
        tests = {
            'GESTOR_PNGI': {
                'add_situacaoacao': True,  # N1
                'add_eixo': True,          # N2
                'add_acoes': True,         # Ops
            },
            'COORDENADOR_PNGI': {
                'add_situacaoacao': False, # NÃO N1
                'add_eixo': True,          # N2
                'add_acoes': True,         # Ops
            },
            'OPERADOR_ACAO': {
                'add_situacaoacao': False, # NÃO N1/N2
                'add_eixo': False,         # NÃO N2
                'add_acoes': True,         # Ops
            },
            'CONSULTOR_PNGI': {
                'add_situacaoacao': False,
                'add_eixo': False,
                'add_acoes': False,        # Read apenas
            }
        }
        
        all_passed = True
        for group_name, expected in tests.items():
            group = Group.objects.get(name=group_name)
            self.stdout.write(f"\n🔍 {group_name}: {group.permissions.count()} perms")
            
            for test_name, should_have in expected.items():
                model = test_name.split('_')[1]
                ct = ct_map[model]
                has_perm = group.permissions.filter(
                    codename=test_name, content_type=ct
                ).exists()
                
                status = '✅' if has_perm == should_have else '❌'
                if has_perm != should_have:
                    all_passed = False
                
                self.stdout.write(f"  {test_name}: {has_perm} {status}")
        
        if all_passed:
            self.stdout.write(self.style.SUCCESS('\n🎉 MATRIZ PNGI 100% CORRETA'))
        else:
            self.stdout.write(self.style.ERROR('\n❌ MATRIZ PNGI COM ERROS'))
        
        return all_passed

