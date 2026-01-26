import sys
from django.core.management import call_command

if "test" in sys.argv:
    # Força migrations do app no banco de teste
    call_command("migrate", "carga_org_lot", verbosity=0)
