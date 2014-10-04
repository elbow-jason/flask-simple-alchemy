from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import sqlalchemy
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


def test_one_to_one_factory_default_foreign_key_as_id():
    #db = SQLAlchemy()
    FakeTableFK = fact.foreign_key_factory('faketable')
    FakeTableOneToOne = fact.one_to_one_factory('FakeTable', FakeTableFK)
    assert issubclass(FakeTableOneToOne, FakeTableFK)
    assert FakeTableOneToOne.faketable_id is not None
    assert isinstance(FakeTableOneToOne.faketable_id, db.Column)


def test_one_to_one_factory_foreign_key_as_second_arg():
    OtherTableFK = fact.foreign_key_factory('othertable', 'uuid')
    OtherTableOneToOne = fact.one_to_one_factory('OtherTable', OtherTableFK)
    assert isinstance(OtherTableOneToOne.othertable_uuid, db.Column)


def test_ForeignKeyMixin():
    FakeTableFK = fact.foreign_key_factory('faketable')

    class AnotherFakeTable(db.Model, FakeTableFK):
        __tablename__   = 'anotherfaketable'
        id              = db.Column(db.Integer, primary_key=True)
        unique_name     = db.Column(db.String, unique=True)

    assert 'faketable_id' in AnotherFakeTable.__dict__
    fk_obj = AnotherFakeTable.faketable_id
    assert fk_obj
    assert "InstrumentedAttribute" in str(type(fk_obj))


def test_database_build():
    db.drop_all()
    db.create_all()


def test_many_to_one_factory():
    FakeTableFK = fact.foreign_key_factory('faketable')
    FakeTableManyToOne = fact.many_to_one_factory('FakeTable', FakeTableFK)
    assert FakeTableManyToOne.faketable_id is not None
    assert 'faketable' in FakeTableManyToOne.__dict__

    class AClassForTesting(db.Model, FakeTableManyToOne):
        id = db.Column(db.Integer, primary_key=True)
        __tablename__ = 'aclassfortesting'

    assert AClassForTesting.__tablename__ == 'aclassfortesting'
    assert 'InstrumentedAttribute' in str(type(AClassForTesting.faketable))
