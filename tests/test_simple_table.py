

from flask_simple_alchemy import SimpleAlchemy

from testers import db

this_table = SimpleAlchemy(db)


class WillItWorkQuestionMark(db.Model, this_table.IsASimpleTable):
    __tablename__ = 'willitworkquestionmark'
    strings = ['did', 'it', 'work']


def test_SimpleTable_string_setting():
    assert WillItWorkQuestionMark.did
    assert WillItWorkQuestionMark.it
    assert WillItWorkQuestionMark.work
