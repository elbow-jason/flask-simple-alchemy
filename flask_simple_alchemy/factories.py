from flask.ext.sqlalchemy import SQLAlchemy


class RelationshipFactories(object):
    """
    I hold the factories that return objects which can be used to 
    create extremely brief declaration of relationships between 
    SQLAlchemy.Model (db.Model actually) objects.
    """

    def __init__(self, db):
        """
        I initialize the RelationshipFactories's instance.
        I expect an instance of the SQLAlchemy object as my first 
        argument. If I don't get a SQLAlchemy object as my first
        argument I will throw an Exception.

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
        I return a Flask-SQLAlchemy ForeignKey.
        I expect a string (name) as my first arg.
        """
        if not isinstance(name, str):
            raise Exception('foreign_key must be a string (str). Got a '\
                + str(type(name)))
        return self.db.ForeignKey(name, **kwargs)

    def foreign_key_factory(self, tablename, foreign_key='id',
                            fk_type=None, **kwargs):
        if fk_type == None:
            fk_type = db.Integer
        table_and_fk = [tablename, foreign_key]
        #given 'person' and 'id' => person_id
        local_ref = '_'.join(table_and_fk)
        #given 'person' and 'id' => person.id
        remote_fk = '.'.join(table_and_fk)

        def declare_id(name):
            @declared_attr
            def func(cls):
                return db.Column(fk_type, self.foreign_key(remote_fk))
            return func
        class ForeignKeyRelationship(object):
            pass

        setattr(ForeignKeyRelationship, 'table_of_fk', tablename)
        #setattr(ForeignKeyRelationship, 'foreign_key', foreign_key)
        setattr(ForeignKeyRelationship, local_ref, declare_id(column_name))
        return ForeignKeyRelationship

    def one_to_one_factory(self, table_class_name_reference,
                           ForeignKeyRelClass):

        def declare_one_to_one(table_class_name):

            @declared_attr
            def func(cls):
                return self.db.relationship(table_class_name,
                    uselist=False,
                    backref=self.db.backref(cls.__tablename__, lazy='select'))
            return func
        class OneToOneRelationship(ForeignKeyRelClass):
            pass

        setattr(OneToOneRelationship, 
                OneToOneRelationship.table_of_fk, 
                declare_one_to_one(table_class_name_reference))
