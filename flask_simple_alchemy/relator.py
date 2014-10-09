
from flask_simple_alchemy.factories import (RelationshipFactories,
                                            simple_table_factory
                                            )


class HasOneToOneWith(object):
    def __init__(self, db, factory_instance):
        self.db = db
        self.factory = factory_instance

    def add(self, class_name, relation_name, fk_obj=None):
        if fk_obj is None:
            fk_obj = class_name.lower()
        setattr(self, relation_name,
                self.factory.one_to_one_factory(class_name, fk_obj))

    def get(self, method_name):
        return self.__dict__[method_name]


class HasManyToOneWith(object):
    def __init__(self, db, factory_instance):
        self.db = db
        self.factory = factory_instance

    def add(self, class_name, relation_name, fk_obj=None):
        if fk_obj is None:
            fk_obj = class_name.lower()
        setattr(self, relation_name,
                self.factory.many_to_one_factory(class_name, fk_obj))

    def get(self, method_name):
        return self.__dict__[method_name]


class HasForeignKeyOf(object):
    def __init__(self, db, factory_instance):
        self.db = db
        self.factory = factory_instance

    def add(self, class_name, relation_name, fk='id', fk_type=None):
        if fk_type is None:
            fk_type = self.db.Integer()
        setattr(self, relation_name,
                self.factory.foreign_key_factory(class_name.lower(),
                                                 fk, fk_type=fk_type))

    def get(self, method_name):
        return self.__dict__[method_name]




class SimpleTableMetaClass(type):
    @property
    def IsASimpleTable(self):
        self._IsASimpleTable
        SimpleTable = simple_table_factory(db)
        SimpleTable._decl_class_registry = db.Model._decl_class_registry
        return SimpleTable

    @IsASimpleTable.setter
    def IsASimpleTable(self, value):
        print "IsASimpleTable is not assignable."




class Relator(object):
    __metaclass__ = SimpleTableMetaClass

    def __init__(self, db):
        self.db = db
        self.factories          = RelationshipFactories(db)
        self.HasForeignKeyOf    = HasForeignKeyOf(db, self.factories)
        self.HasOneToOneWith    = HasOneToOneWith(db, self.factories)
        self.HasManyToOneWith   = HasManyToOneWith(db, self.factories)
        self.IsASimpleTable     = simple_table_factory(db)

    def add(self, table_class_name, foreign_key='id',
            relation_name=None, fk_type=None):

        if relation_name is None:
            relation_name = table_class_name
        if fk_type is None:
            fk_type = self.db.Integer()

        self.HasForeignKeyOf.add(table_class_name, relation_name,
                                 fk=foreign_key, fk_type=fk_type)
        self.HasOneToOneWith.add(table_class_name, relation_name,
                                 self.HasForeignKeyOf.get(relation_name))
        self.HasManyToOneWith.add(table_class_name, relation_name,
                                  self.HasForeignKeyOf.get(relation_name))


class SimpleAlchemy(Relator):
    pass