

from flask_simple_alchemy import SimpleAlchemy

from testers import db, app

import datetime

this_table = SimpleAlchemy(db)


class WillItWorkQuestionMark(db.Model, this_table.IsASimpleTable):
    __tablename__ = 'willitworkquestionmark'
    strings = ['did', 'it', 'work']


class ClarkKent(db.Model):
    __tablename__  = "clarkkent"
    id = db.Column(db.Integer, primary_key=True)
    height      = db.Column(db.String)
    weight      = db.Column(db.String)
    real_name   = db.Column(db.String)
    level       = db.Column(db.Integer)
    date_of_birth = db.Column(db.Date)

class Superman(db.Model, this_table.IsASimpleTable):
    __tablename__ = 'superman'
    integers = ['level']
    strings = ['height', 'weight', 'real_name']
    dates = ['date_of_birth']


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


def test_superman_vs_clark_kent():
    with app.app_context():
        db.drop_all()
        db.create_all()

        ck = ClarkKent()
        sm = Superman()

        ck.weight = '235 lbs'
        ck.height = "6ft 3in"
        ck.real_name = "Kal-El"
        ck.date_of_birth = datetime.date(1986, 10, 1)
        ck.level = 5


        db.session.add(ck)
        db.session.commit()

        saved_clark = ClarkKent.query.first()

        assert saved_clark.weight == '235 lbs'
        assert saved_clark.height == "6ft 3in"
        assert saved_clark.real_name == "Kal-El"
        assert saved_clark.date_of_birth == datetime.date(1986, 10, 1)
        assert saved_clark.level == 5

        sm.weight        = saved_clark.weight
        sm.height        = saved_clark.height
        sm.real_name     = saved_clark.real_name
        sm.date_of_birth = saved_clark.date_of_birth
        sm.level         = saved_clark.level

        db.session.add(sm)
        db.session.commit()

        saved_sup = Superman.query.first()

        assert saved_sup.weight        == saved_clark.weight
        assert saved_sup.height        == saved_clark.height
        assert saved_sup.real_name     == saved_clark.real_name
        assert saved_sup.date_of_birth == saved_clark.date_of_birth
        assert saved_sup.level         == saved_clark.level


