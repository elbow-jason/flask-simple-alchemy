#test_factory_helpers.py

from flask_simple_alchemy.factory_helpers import *

from testers import *


def default_kwargs():
    return {'uselist': True,
            'lazy': 'dynamic',
            'one_to_one': False,
            'many_to_one': False}


def test_default_relationship_kwargs():
    assert default_kwargs() == default_relationship_kwargs()


def test_kwarg_corrector_one_to_one_conflicts_many_to_one_kwargs_true():
    kwargs = default_kwargs()
    kwargs['one_to_one'] = True
    kwargs['many_to_one'] = True
    try:
        kwarg_corrector(**kwargs)
    except Exception as e:
        print e
    else:
        raise Exception('relationship_kwarg_corrector did not throw'
                        'error when\n presented with one_to_one=True'
                        ' and many_to_one=True')

    kwargs2 = default_kwargs()
    kwargs2['one_to_one']=True
    kwargs2['many_to_one']=True
    assert kwargs == kwargs2

def test_kwargs_corrector_one_to_one_true():
    kwargs = default_kwargs()
    kwargs['one_to_one']=True
    kwarg_corrector(**kwargs)

def test_warning():
    msg = warning()
    assert isinstance(msg, str)
    assert msg.count('{}') == 5


def test_kwargs_corrector_one_to_one_and_uselist_true():
    one = 'uselist'
    two = 'one_to_one'
    three = 'True'
    four = 'uselist'
    five = 'False'
    msg = warn(one, two, three, four, five)

    kwargs = default_kwargs()
    kwargs['uselist'] = True
    kwargs['one_to_one'] = True
    kwargs['lazy'] = 'select'

    l = LogCapture()
    new_kwargs = kwarg_corrector(**kwargs)
    l.check( ('root', 'WARNING', msg),)
    del l
    assert new_kwargs['lazy'] == 'select'
    assert new_kwargs['uselist'] == False



