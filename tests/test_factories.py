from flask.ext.sqlalchemy import SQLAlchemy

from flask_simple_alchemy import RelationshipFactories

from sqlalchemy.ext.declarative import declared_attr

db = SQLAlchemy()

class FakeTable(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    unique_name = db.Column(db.String, unique=True)
    non_unique_col = db.Column(db.String)


def test_RelationshipFactories_init():
    #db = SQLAlchemy()
    try:
        fact = RelationshipFactories(db)
    except:
        assert "initialization errored" is "Yes"
    assert isinstance(fact, RelationshipFactories)
    assert fact.db



def test_RelationshipFactories_init_not_passed_SQLAlchemy_db_object():
    class BlankClass(object):
        pass

    not_db = BlankClass()
    errored = False
    try:
        fact = RelationshipFactories(not_db)
        errored = True
    except:
        errored = False

    assert not errored

def test_foreign_key_func():
    #db = SQLAlchemy()
    fact = RelationshipFactories(db)
    fk = fact.foreign_key('jason')
    assert isinstance(fk, db.ForeignKey)
    assert fk._colspec == 'jason'
    def print_update():
        print "update!!"
    fk2 = fact.foreign_key('rahul', onupdate=print_update)
    assert fk2._colspec == 'rahul'
    assert fk2.onupdate == print_update

def test_foreign_key_factory():
    fact = RelationshipFactories(db)
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
def test_one_to_one_factory():
    #db = SQLAlchemy()
    fact = RelationshipFactories(db)
    FakeTableFKRelation = fact.foreign_key_factory('faketable')
