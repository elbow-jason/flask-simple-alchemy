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
        I expect an instance of the SQLAlchemy object.
        If I don't get a SQLAlchemy object I will throw an Exception.

        Constructor.

            :param db:
                Flask-SQLAlchemy database object
        """
        if not isinstance(db, SQLAlchemy):
            raise Exception('The RelationshipFactories object\
                requires/expects an instance of the SQLAlchemy object.')
        self.db = db



    def id_num_relation_factory(self, column_name, **kwargs):
        foreign_key  = kwargs.get('foreign_key', 'id')
        nullable     = kwargs.get('nullable', False)
        fk_data_type = kwargs.get('column_type', self.db.Integer)
        fk           = '{}.{}'.format(column_name, foreign_key)
        def declare_id(name):
            @declared_attr
            def func(cls):
                return db.Column(fk_data_type, db.ForeignKey(fk, nullable=nullable))
            return func
        class Ider(object):
            pass
        setattr(Ider, column_name + '_' + fk, declare_id(column_name))
        return Ider

