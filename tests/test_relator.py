from flask_simple_alchemy import Relator
from testers import db, FakeTable, OtherTable


def test_Relator():
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
