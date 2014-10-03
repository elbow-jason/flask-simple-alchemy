"""
I am a module called 'factories' in a file named 'factories.py' inside the
flask_simple_alchemy folder. I contain the RelationshipFactories class
which is used to generate Relationship Mixins.
"""

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

from factory_helpers import kwarg_corrector


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
                Flask-SQLAlchemy database object
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
                     one_to_many=False, uselist=None, lazy=None):
        """
        I return relationship objects.
        """
        kwargs = dict(one_to_one=one_to_one, one_to_many=one_to_many,
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

        class ForeignKeyRelationship(object):
            pass

        setattr(ForeignKeyRelationship, 'table_of_fk', tablename)
        #setattr(ForeignKeyRelationship, 'foreign_key', foreign_key)
        setattr(ForeignKeyRelationship, local_ref, declare_id())
        return ForeignKeyRelationship

    def one_to_one_factory(self, table_class_name_reference,
                           ForeignKeyRelClass):
        """
        I am used to generate One-to-One relationship mixins
        """
        def declare_one_to_one(table_class_name):

            @declared_attr
            def func(cls):
                return self.relationship(cls, table_class_name,
                                         uselist=False, lazy='select')
            return func

        class OneToOneRelationship(ForeignKeyRelClass):
            pass

        setattr(OneToOneRelationship,
                OneToOneRelationship.table_of_fk,
                declare_one_to_one(table_class_name_reference))

        return OneToOneRelationship
