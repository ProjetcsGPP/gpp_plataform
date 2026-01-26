# carga_org_lot/db_router.py
class CargaOrgLotRouter:
    """
    Router para direcionar queries da app carga_org_lot para o schema correto
    """
    route_app_labels = {'carga_org_lot'}
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'default'
        return None
