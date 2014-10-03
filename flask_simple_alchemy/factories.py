
class RelationshipFactories(object):


    def id_num_relation_factory(column_name, **kwargs):
        foreign_key  = kwargs.get('foreign_key', 'id')
        nullable     = kwargs.get('nullable', False)
        fk_data_type = kwargs.get('column_type', db.Integer)
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

