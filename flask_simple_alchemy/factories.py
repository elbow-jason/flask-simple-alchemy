from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
import logging


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

    def relationship(self, class_obj, table_class_name,
                    one_to_one=False, one_to_many=False,
                    uselist=None, lazy=None):

        return self.db.relationship(table_class_name,
                uselist=uselist,
                backref=self.db.backref(class_obj.__tablename__, 
                lazy=lazy))


    def kwarg_corrector(self, **kwargs):
        if kwargs['one_to_one'] and kwargs['one_to_many']:
            raise Exception('relationship kwargs one_to_one and one_to_many'+\
                            'at the same time.\n That doesn\'t even make'+\
                            'sense. Choose one or the other not both.')

        if kwargs['one_to_one']:
            if kwargs['uselist'] == True:
                self.override_warning('uselist', 'one_to_one', 'True', 'False')
            if kwargs['lazy'] != 'select':
                self.override_warning('lazy', 'one_to_one',
                                     kwargs['lazy'], 'select')
            #set one_to_one kwargs
            kwargs['uselist'] = False
            kwargs['lazy'] = "select"
        
        if kwargs['one_to_many']:
            if kwargs['uselist'] == False:
                self.override_warning('uselist', 'one_to_one', 'False', 'True')
            if kwargs['lazy'] == 'dynamic':
                logging.warning('lazy was unneccessarily specified')
            #set one_to_many kwargs
            kwargs['uselist'] == True


    def override_warning(self, str1, str2, orig_val, override):
        msg = "{str1} kwarg was specified with {str2} kwarg set as {orig_val}."+\
            " Overriding {str1} to {override}."
        logging.warning(msg.format(str1=str1, str2=str2, 
                                    val2=val2, override=override))



    def foreign_key_factory(self, tablename, foreign_key='id',
                            fk_type=None, **kwargs):
        if fk_type == None:
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
