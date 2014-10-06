from flask_simple_alchemy import Relator
from testers import db, FakeTable, OtherTable


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


def test_Realtor_relationships():
    this_table = Relator(db)
    this_table.add('FakeTable')
    this_table.add('OtherTable', foreign_key='uuid')

    class ThirdTable(db.Model, this_table.HasOneToOneWith.FakeTable):
        __tablename__ = 'thirdtable'
        id = db.Column(db.Integer, primary_key=True)

    assert ThirdTable.faketable_id
    assert ThirdTable.faketable


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
