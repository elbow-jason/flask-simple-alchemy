from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

#from sqlalchemy.ext.declarative import declared_attr

from flask_simple_alchemy import RelationshipFactories

app = Flask(__name__)
app.config.update(dict(SECRET_KEY="nonono",
                       SQLALCHEMY_DATABASE_URI='sqlite:///faketest.db')
                  )

db = SQLAlchemy(app)
fact = RelationshipFactories(db)


class FakeTable(db.Model):
    __tablename__   = 'faketable'
    id              = db.Column(db.Integer, primary_key=True)
    unique_name     = db.Column(db.String, unique=True)
    non_unique_col  = db.Column(db.String)


class OtherTable(db.Model):
    __tablename__   = 'othertable'
    uuid            = db.Column(db.String, primary_key=True)
    event_count     = db.Column(db.Integer)


def test_RelationshipFactories_init():
    #db = SQLAlchemy()
    try:
        factr = RelationshipFactories(db)
    except:
        assert "initialization errored" is "Yes"
    assert isinstance(factr, RelationshipFactories)
    assert factr.db

def test_RelationshipFactories_init_not_passed_SQLAlchemy_db_object():
    class BlankClass(object):
        pass

    not_db = BlankClass()
    errored = False
    try:
        RelationshipFactories(not_db)
        errored = True
    except:
        errored = False

    assert not errored

def test_foreign_key_func():
    #db = SQLAlchemy()
    #fact = RelationshipFactories(db)
    fk = fact.foreign_key('jason')
    assert isinstance(fk, db.ForeignKey)
    assert fk._colspec == 'jason'
    def print_update():
        print "update!!"
    fk2 = fact.foreign_key('rahul', onupdate=print_update)
    assert fk2._colspec == 'rahul'
    assert fk2.onupdate == print_update

def test_foreign_key_factory():
    #fact = RelationshipFactories(db)
    FakeTableFKRelation = fact.foreign_key_factory('faketable')
    print FakeTableFKRelation.faketable_id.__dict__
    assert isinstance(FakeTableFKRelation.faketable_id, db.Column)
    testInt = db.Integer()
    assert FakeTableFKRelation.faketable_id.type.__dict__ == testInt.__dict__
    FakeTableFKRelation2 = fact.foreign_key_factory('faketable', 
                                                    foreign_key='unique_name')
    assert str(FakeTableFKRelation2.faketable_unique_name.foreign_keys)\
        == "set([ForeignKey('faketable.unique_name')])"
    assert str(FakeTableFKRelation2.faketable_unique_name.type)\
        == 'INTEGER'

def test_relationship_func():
    rel1to1 = fact.relationship(FakeTable, 'FakeTable',
                                uselist=False, lazy='select')
    assert rel1to1
    assert type(rel1to1) is type(db.relationship('FakeTable'))

def test_one_to_one_factory():
    #db = SQLAlchemy()
    
    FakeTableFK = fact.foreign_key_factory('faketable')
    FakeTableOneToOne = fact.one_to_one_factory('FakeTable', FakeTableFK)
    assert issubclass(FakeTableOneToOne, FakeTableFK)
    assert FakeTableOneToOne.faketable_id is not None
    assert isinstance(FakeTableOneToOne.faketable_id, db.Column)

def test_ForeignKeyMixin():
    FakeTableFK = fact.foreign_key_factory('faketable')
    class AnotherFakeTable(db.Model, FakeTableFK):
        __tablename__   = 'anotherfaketable'
        id              = db.Column(db.Integer, primary_key=True)
        unique_name     = db.Column(db.String, unique=True)

    assert AnotherFakeTable.__dict__.has_key('faketable_id')
    fk_obj = AnotherFakeTable.faketable_id
    assert fk_obj

def test_database_build():
    db.drop_all()
    db.create_all()



