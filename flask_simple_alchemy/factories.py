"""
I am a module called 'factories' in a file named 'factories.py' inside the
flask_simple_alchemy folder. I contain the RelationshipFactories class
which is used to generate Relationship Mixins.
"""

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

from flask_simple_alchemy.factory_helpers import kwarg_corrector


class RelationshipFactories(object):
    """
    I hold the factories that return objects which can be used to\n
    create extremely brief declaration of relationships between\n
    SQLAlchemy.Model (db.Model actually) objects.\n
    """

    def __init__(self, db):
        """
        I initialize the RelationshipFactories's instance.\n
        I expect an instance of the SQLAlchemy object as my first\n
        argument. If I don't get a SQLAlchemy object as my first\n
        argument I will throw an Exception.\n

        Constructor.

            :param db:
                Flask-SQLAlchemy database object. Instance of
                flask.ext.sqlalchemy.SQLAlchemy()
        """
        if not isinstance(db, SQLAlchemy):
            raise Exception('The RelationshipFactories object\
                requires/expects an instance of the SQLAlchemy object.')
        self.db = db

    def foreign_key(self, name, **kwargs):
        """
        I am for generating foreign keys.
        I return a Flask-SQLAlchemy ForeignKey.
        I expect a string (name) as my first arg.
        """
        if not isinstance(name, str):
            e = 'foreign_key must be a string (str). Got a ' + str(type(name))
            raise Exception(e)
        return self.db.ForeignKey(name, **kwargs)

    def relationship(self, class_obj, table_class_name, one_to_one=False,
                     many_to_one=False, uselist=None, lazy=None):
        """
        I return relationship objects.
        """
        kwargs = dict(one_to_one=one_to_one, many_to_one=many_to_one,
                      uselist=uselist, lazy=lazy)

        kwargs = kwarg_corrector(**kwargs)
        return self.db.relationship(table_class_name, uselist=uselist,
                                    backref=self.db.backref(
                                        class_obj.__tablename__,
                                        lazy=lazy))

    def foreign_key_factory(self, tablename, foreign_key='id',
                            fk_type=None, **kwargs):
        """
        I am used to generate ForeignKey mixin objects.
        """
        if fk_type is None:
            fk_type = self.db.Integer
        table_and_fk = [tablename, foreign_key]
        #given 'person' and 'id' => person_id
        local_ref = '_'.join(table_and_fk)
        #given 'person' and 'id' => person.id
        remote_fk = '.'.join(table_and_fk)

        def declare_id():
            @declared_attr
            def func(cls):
                return self.db.Column(fk_type, self.foreign_key(remote_fk))
            return func

        class ForeignKeyMixin(object):
            pass

        setattr(ForeignKeyMixin, 'table_of_fk', tablename)
        #setattr(ForeignKeyRelationship, 'foreign_key', foreign_key)
        setattr(ForeignKeyMixin, local_ref, declare_id())
        return ForeignKeyMixin

    def one_to_one_factory(self, table_class_name_reference,
                           ForeignKeyMixinClass):
        """
        I am used to generate One-to-One relationship mixins.
        """
        def declare_one_to_one(table_class_name):
            """

            """
            @declared_attr
            def func(cls):
                return self.db.relationship(table_class_name,
                      backref=self.db.backref(cls.__tablename__,
                                uselist=False, lazy='select'), )
            return func

        class OneToOneRelationship(ForeignKeyMixinClass):
            """
            I am the Mixin Class for OneToOne Relationships.
            I inherit from ForeignKeyRelClass\n which is generated
            returned by instances RelationshipFactories.foreign_key_factory.\n
            After leaving this factory I will have two '@declared_attr'
            methods: a foreign key and a\n relationship object.
            """
            pass

        setattr(OneToOneRelationship,
                OneToOneRelationship.table_of_fk,
                declare_one_to_one(table_class_name_reference))

        return OneToOneRelationship

    def many_to_one_factory(self, table_class_name_reference,
                            ForeignKeyMixinClass):
        """
        I am used to generate One-to-One relationship mixins.
        """
        def declare_one_to_one(table_class_name):
            """

            """
            @declared_attr
            def func(cls):
                return self.db.relationship(table_class_name,
                    backref=self.db.backref(cls.__tablename__,
                                            lazy='dynamic'), lazy='select'
                                            )
            return func

        class OneToManyRelationship(ForeignKeyMixinClass):
            """
            I am the Mixin Class for OneToOne Relationships.
            I inherit from ForeignKeyRelClass which is generated
            returned by instances RelationshipFactories.foreign_key_factory.
            After leaving this factory I will have two '@declared_attr'
            methods: a foreign key and a relationship object.
            """
            pass

        setattr(OneToManyRelationship,
                OneToManyRelationship.table_of_fk,
                declare_one_to_one(table_class_name_reference))

        return OneToManyRelationship


from flask.ext.sqlalchemy import _BoundDeclarativeMeta

def simple_table_factory(db, default_primary_key='id',
                         default_pk_type='integer'):
    """
    I am a factory that produces a class Mixin that provides:
    1) default 'id' primary_key columns
        change primary key attribute and type via:
            default_primary_key='some_stringy_key'
            default_pk_type='string'
    2) and table attributes/columns in easy-to-use lists
    """

    def get_type(typename):
        """
        I am the get_type function.
        I am a function that returns SQLAlchemy column data types given
        a stringy representation of that type.
            i.e. given the arg 'string', I return the db.String function.
            i.e. given the arg 'integer', I return the db.Integer function.
        """
        types = {
                'string':  db.String,
                'integer': db.Integer
                }
        try:
            return types[str(typename)]
        except:
            raise Exception(str(typename) + ' was not a valid type')

    def simple_setter(class_object, column_typename):
        """
        """
        def set_type(self, value):
            for item in value:
                setattr(class_object,
                        item,
                        db.Column(get_type(column_typename)))
                setattr(self, '_' + column_typename, value)
        return set_type

    def simple_getter(column_typename):
        def get_type(self):
                return getattr(self, '_' + column_typename)
        return get_type


    class SimpleMetaClass(type):
        pass

    setattr(SimpleMetaClass, 'strings',
            property(simple_getter('string'),
                     simple_setter(SimpleMetaClass, 'string')))

    setattr(SimpleMetaClass, 'integers',
            property(simple_getter('integer'),
                     simple_setter(SimpleMetaClass, 'integer')))



    class DoubleMetaClass(SimpleMetaClass, _BoundDeclarativeMeta):
        pass

    class SimpleTable(object):
        """
        I am SimpleTable. I am a Mixin that provides:
            1) an integer primary key 'id'
            2) the ability to define SQLAlchemy columns via iterable lists.
        """
        _decl_class_registry = []
        __metaclass__ = DoubleMetaClass
        __abstract__= True


    if default_primary_key:
        setattr(SimpleTable, default_primary_key,
                db.Column(get_type(default_pk_type), primary_key=True))


    return SimpleTable
