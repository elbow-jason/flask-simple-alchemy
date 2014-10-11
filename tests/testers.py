from testfixtures import LogCapture, log_capture
import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_simple_alchemy import RelationshipFactories

app = Flask(__name__)
app.config.update(dict(SECRET_KEY="nonono",
                       SQLALCHEMY_DATABASE_URI='sqlite://')
                  )

db = SQLAlchemy(app)
fact = RelationshipFactories(db)



def capture(messenger, msg, level='DEBUG'):
    with LogCapture() as l:
        messenger()
        l.check( ('root', level, msg),)
    LogCapture.instances = set()

def capture_any_log(messenger, msg):
    one_of_them_worked = False
    level = False
    logger = logging.getLogger()

    try:
        capture(messenger, msg, level='DEBUG')
        one_of_them_worked = True
        level='DEBUG'
    except:
        pass

    try:
        capture(messenger, msg, level='INFO')
        one_of_them_worked = True
        level='INFO'
    except:
        pass

    try:
        capture(messenger, msg, level='WARNING')
        one_of_them_worked = True
        level='WARNING'
    except:
        pass

    try:
        capture(messenger, msg, level='ERROR')
        one_of_them_worked = True
        level='ERROR'
    except:
        pass

    try:
        capture(messenger, msg, level='CRITICAL')
        one_of_them_worked = True
        level='CRITICAL'
    except:
        pass

    assert one_of_them_worked


def capture_warning(messenger, msg):
    capture(messenger, msg, level='WARNING')



class FakeTable(db.Model):
    __tablename__ = 'faketable'
    id = db.Column(db.Integer, primary_key=True)
    unique_name = db.Column(db.String, unique=True)
    non_unique_col = db.Column(db.String)


class OtherTable(db.Model):
    __tablename__ = 'othertable'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    event_count = db.Column(db.Integer)


