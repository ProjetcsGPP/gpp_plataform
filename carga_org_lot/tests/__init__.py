# Força os models a serem gerenciados durante os testes
import sys
if 'test' in sys.argv:
    from django.apps import apps
    app_config = apps.get_app_config('carga_org_lot')
    for model in app_config.get_models():
        model._meta.managed = True
