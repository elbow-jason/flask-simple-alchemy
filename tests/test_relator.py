from flask_simple_alchemy import Relator
from testers import db, app, FakeTable, OtherTable

this_table = Relator(db)
this_table.add('FakeTable')
this_table.add('OtherTable', foreign_key='uuid')

class ThirdTable(db.Model, this_table.HasOneToOneWith.FakeTable):
    __tablename__ = 'thirdtable'
    id = db.Column(db.Integer, primary_key=True)
    elf = db.Column(db.Boolean(False))
    monkey = db.Column(db.String, default='yep')

def test_Relator_setattrs():
    this_table = Relator(db)
    this_table.add('FakeTable')
    this_table.add('OtherTable', foreign_key='uuid')

    assert this_table.HasForeignKeyOf
    assert this_table.HasOneToOneWith
    assert this_table.HasManyToOneWith

    assert this_table.HasForeignKeyOf.FakeTable
    assert this_table.HasOneToOneWith.FakeTable
    assert this_table.HasManyToOneWith.FakeTable

    assert this_table.HasForeignKeyOf.OtherTable
    assert this_table.HasOneToOneWith.OtherTable
    assert this_table.HasManyToOneWith.OtherTable


def test_Realtor_relationship():


    assert ThirdTable.faketable_id
    assert ThirdTable.faketable

    with app.app_context():
        fk = FakeTable()
        fk.unique_name = 'gggg'
        db.session.add(fk)
        db.session.commit()
        saved = FakeTable.query.filter_by(unique_name='gggg').first()
        tt = ThirdTable()

        tt.faketable_id = saved.id
        db.session.add(tt)
        db.session.commit()

        saved2 = ThirdTable.query.filter_by(monkey='yep').first()
    assert saved
    assert tt
    assert saved2




def test_Realtor_relationship_again():
    this_table = Relator(db)
    this_table.add('FakeTable')
    this_table.add('OtherTable', foreign_key='uuid', relation_name='OtherTableUUID1')

    class FourthTable(db.Model, this_table.HasManyToOneWith.OtherTableUUID1):
        __tablename__ = 'fourthtable'
        id = db.Column(db.Integer, primary_key=True)

    assert FourthTable.othertable_uuid
    assert FourthTable.othertable

def test_Realtor_relation_name():
    this_table = Relator(db)
    this_table.add('FakeTable')
    this_table.add('OtherTable')
    this_table.add('OtherTable', foreign_key='uuid', relation_name="OtherTableUUID")

    class SixthTable(db.Model, this_table.HasManyToOneWith.OtherTable):
        __tablename__ = 'sixthtable'
        id = db.Column(db.Integer, primary_key=True)

    class FifthTable(db.Model, this_table.HasManyToOneWith.OtherTableUUID):
        __tablename__ = 'fifthtable'
        id = db.Column(db.Integer, primary_key=True)
    

    assert SixthTable.othertable_id
    assert SixthTable.othertable

    assert FifthTable.othertable_uuid
    assert FifthTable.othertable


def test_database_creation():
    this_table = Relator(db)
    this_table.add('FakeTable')
    this_table.add('OtherTable', foreign_key='uuid')

    #class ThirdTable(db.Model, this_table.HasOneToOneWith.FakeTable):
    #    __tablename__ = 'thirdtable'
    #    id = db.Column(db.Integer, primary_key=True)

    db.drop_all()
    db.create_all()
    db.drop_all()

