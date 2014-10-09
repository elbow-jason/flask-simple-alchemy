

from flask_simple_alchemy import SimpleAlchemy

from testers import db

this_table = SimpleAlchemy(db)


class WillItWorkQuestionMark(db.Model, this_table.IsASimpleTable):
    __tablename__ = 'willitworkquestionmark'
    strings = ['did', 'it', 'work']


def test_SimpleTable_automatic_id_attribute():
    assert WillItWorkQuestionMark.id is not None
    assert WillItWorkQuestionMark.id.primary_key == True

def test_SimpleTable_strings_property():
    assert WillItWorkQuestionMark.did is not None
    assert WillItWorkQuestionMark.it is not None
    assert WillItWorkQuestionMark.work is not None
    try:
        assert WillItWorkQuestionMark.doesnt_exist is None
    except:
        assert True
    else:
        assert False


def test_simple_table_object():
    pass
