class DatabaseRouter:
    route_app_labels = {'auth', 'authtoken', 'contenttypes', 'sessions', 'admin', 'account', 'socialaccount'}
    meta_ads_models = {'metaadsdata', 'metaadsdata'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'auth_db'
        elif model._meta.model_name == 'metaadsdata':
            return 'meta_ads_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'auth_db'
        elif model._meta.model_name == 'metaadsdata':
            return 'meta_ads_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'auth_db'
        elif model_name == 'metaadsdata':
            return db == 'meta_ads_db'
        return None