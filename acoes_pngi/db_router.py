# acoes_pngi/db_router.py

class AcoesPNGIRouter:
    """
    Router para direcionar operações do app acoes_pngi para o schema correto
    """
    route_app_labels = {'acoes_pngi'}
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            # Força o schema correto antes de migrations
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SET search_path TO acoes_pngi, public")
            return db == 'default'
        return None
