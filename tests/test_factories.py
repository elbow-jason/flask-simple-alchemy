from flask.ext.sqlalchemy import SQLAlchemy

from flask_simple_alchemy import RelationshipFactories


def test_RelationshipFactories_init():
    db = SQLAlchemy()
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