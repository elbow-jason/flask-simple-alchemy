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
        return self.db.ForeignKey(name, **kwargs)

    def foreign_key_factory(self, column_name, foreign_key='id',
                            nullable=True, fk_type=None,  **kwargs):
        if fk_type == None:
            fk_type = db.Integer
        table_and_fk = [column_name, foreign_key]
        #given 'person' and 'id' => person_id
        local_ref = '_'.join(table_and_fk)
        #given 'person' and 'id' => person.id
        remote_fk = '.'.join(table_and_fk)

        def declare_id(name):
            @declared_attr
            def func(cls):
                return db.Column(fk_type, self.foreign_key(remote_fk, nullable=nullable))
            return func
        class ForeignKeyRelationship(object):
            pass
        setattr(ForeignKeyRelationship, local_ref, declare_id(column_name))
        return ForeignKeyRelationship

