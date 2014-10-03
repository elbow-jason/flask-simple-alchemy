
from flask_simple_alchemy import RelationshipFactories

def test_RelationshipFactories_init():
    pass



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