
#import sqlalchemy
#from sqlalchemy.ext.declarative import declared_attr

from flask_simple_alchemy import RelationshipFactories
from testers import *


FakeTableFK = fact.foreign_key_factory('faketable')
FakeTableOneToOne = fact.one_to_one_factory('FakeTable', FakeTableFK)
FakeTableManyToOne = fact.many_to_one_factory('FakeTable', FakeTableFK)



class YetAnotherFakeTable(db.Model, FakeTableOneToOne):
    __tablename__ = 'yetanotherfaketable'
    id = db.Column(db.Integer, primary_key=True)
    unique_name = db.Column(db.String, unique=True)


class AClassForTesting(db.Model, FakeTableManyToOne):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'aclassfortesting'


class YetAnotherFakeTableAgain(db.Model, FakeTableManyToOne):
    __tablename__ = 'yetanotherfaketableagain'
    id = db.Column(db.Integer, primary_key=True)
    unique_name = db.Column(db.String, unique=True)


class AnotherFakeTable(db.Model, FakeTableFK):
    __tablename__ = 'anotherfaketable'
    id = db.Column(db.Integer, primary_key=True)
    unique_name = db.Column(db.String, unique=True)


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
    print FakeTableFK.faketable_id.__dict__
    assert isinstance(FakeTableFK.faketable_id, db.Column)
    testInt = db.Integer()
    assert FakeTableFK.faketable_id.type.__dict__ == testInt.__dict__
    FakeTableFK2 = fact.foreign_key_factory('faketable',
                                                    foreign_key='unique_name')
    assert str(FakeTableFK2.faketable_unique_name.foreign_keys)\
        == "set([ForeignKey('faketable.unique_name')])"
    assert str(FakeTableFK2.faketable_unique_name.type)\
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


def test_database_build():
    db.drop_all()
    db.create_all()


def test_many_to_one_factory():
    assert FakeTableManyToOne.faketable_id is not None
    assert 'faketable' in FakeTableManyToOne.__dict__

    assert AClassForTesting.__tablename__ == 'aclassfortesting'
    assert 'InstrumentedAttribute' in str(type(AClassForTesting.faketable))

    aclass = AClassForTesting()
    db.session.add(aclass)
    db.session.commit()


def test_ForeignKeyMixin():
    FakeTableFK = fact.foreign_key_factory('faketable')



    assert 'faketable_id' in AnotherFakeTable.__dict__
    fk_obj = AnotherFakeTable.faketable_id
    assert fk_obj
    assert "InstrumentedAttribute" in str(type(fk_obj))


def test_OneToOneMixin():

    db.drop_all()
    db.create_all()

    new_fake = FakeTable()
    new_fake.non_unique_col = 'wwooo'
    new_fake.unique_name = 'ft1'
    db.session.add(new_fake)
    db.session.commit()

    ft1 = FakeTable.query.filter_by(unique_name='ft1').first()

    yaft1 = YetAnotherFakeTable()
    yaft1.unique_name = 'yaft1'
    yaft1.faketable_id = ft1.id
    db.session.add(yaft1)
    db.session.commit()

    ft1 = FakeTable.query.filter_by(unique_name='ft1').first()
    yaft1 = YetAnotherFakeTable.query.filter_by(unique_name='yaft1').first()

    assert YetAnotherFakeTable.faketable
    assert YetAnotherFakeTable
    assert yaft1.faketable == ft1
    assert ft1.yetanotherfaketable == yaft1

    yaft2 = YetAnotherFakeTable()
    yaft2.unique_name = 'yaft2'
    yaft2.faketable_id = ft1.id
    db.session.add(yaft2)
    db.session.commit()

    assert ft1.yetanotherfaketable == yaft1

    #assert ft1.yetanotherfaketable[1] == yaft2

    db.drop_all()


def test_ManyToOneMixin():
    FakeTableFK = fact.foreign_key_factory('faketable')
    FakeTableManyToOne = fact.many_to_one_factory('FakeTable', FakeTableFK)

    db.drop_all()
    db.create_all()

    assert YetAnotherFakeTableAgain
    assert YetAnotherFakeTableAgain.faketable

    new_fake = FakeTable()
    new_fake.non_unique_col = 'wwooo'
    new_fake.unique_name = 'ft1'
    db.session.add(new_fake)
    db.session.commit()
    new_fake_saved = FakeTable.query.filter_by(unique_name='ft1').first()

    assert new_fake_saved

    newb1 = YetAnotherFakeTableAgain()
    newb1.unique_name = 'yafta1'
    newb1.faketable_id = new_fake_saved.id
    db.session.add(newb1)
    db.session.commit()

    newb2 = YetAnotherFakeTableAgain()
    newb2.unique_name = 'yafta2'
    newb2.faketable_id = new_fake_saved.id
    db.session.add(newb2)
    db.session.commit()

    count = YetAnotherFakeTableAgain.query.count()
    assert count == 2

    all_yafta = YetAnotherFakeTableAgain.query.all()
    assert len(all_yafta) == 2
    assert all_yafta[0].unique_name == 'yafta1'
    assert all_yafta[0].faketable_id == 1
    assert all_yafta[1].unique_name == 'yafta2'
    assert all_yafta[1].faketable_id == 1

    reloaded_fake_saved = FakeTable.query.filter_by(unique_name='ft1').first()
    yafta1 = reloaded_fake_saved.yetanotherfaketableagain[0]
    yafta2 = reloaded_fake_saved.yetanotherfaketableagain[1]

    assert yafta1.unique_name == 'yafta1'
    assert yafta2.unique_name == 'yafta2'

    #assert one
    #assert two

