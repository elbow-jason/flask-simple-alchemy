
from flask_simple_alchemy import RelationshipFactories


class HasOneToOneWith(object):
    def __init__(self, db, factory_instance):
        self.db = db
        self.factory = factory_instance

    def add(self, class_name, fk_obj=None):
        if fk_obj is None:
            fk_obj = class_name.lower()
        setattr(self, class_name, self.factory.one_to_one_factory(class_name, fk_obj))

    def get(self, method_name):
        return self.__dict__[method_name]

class HasManyToOneWith(object):
    def __init__(self, db, factory_instance):
        self.db = db
        self.factory = factory_instance

    def add(self, class_name, fk_obj=None):
        if fk_obj is None:
            fk_obj = class_name.lower()
        setattr(self, class_name, self.factory.many_to_one_factory(class_name, fk_obj))

    def get(self, method_name):
        return self.__dict__[method_name]

class HasForeignKeyOf(object):
    def __init__(self, db, factory_instance):
        self.db = db
        self.factory = factory_instance

    def add(self, class_name, fk='id'):
        setattr(self, class_name, self.factory.foreign_key_factory(class_name.lower(), fk))

    def get(self, method_name):
        return self.__dict__[method_name]

class Relator(object):
    def __init__(self, db):
        self.db = db
        self.factories          = RelationshipFactories(db)
        self.HasForeignKeyOf    = HasForeignKeyOf(db, self.factories)
        self.HasOneToOneWith    = HasOneToOneWith(db, self.factories)
        self.HasManyToOneWith   = HasManyToOneWith(db, self.factories)

    def add(self, table_class_name, foreign_key='id'):
        self.HasForeignKeyOf.add(table_class_name, fk=foreign_key)
        self.HasOneToOneWith.add(table_class_name,
                                 self.HasForeignKeyOf.get(table_class_name))
        self.HasManyToOneWith.add(table_class_name,
                                 self.HasForeignKeyOf.get(table_class_name))
