#test_factory_helpers.py
import logging
from testfixtures import LogCapture, log_capture
from flask_simple_alchemy.factory_helpers import *




def default_kwargs():
    return {'uselist':True,
            'lazy':'dynamic',
            'one_to_one':False,
            'one_to_many':False}

def test_default_relationship_kwargs():
    assert default_kwargs() == default_relationship_kwargs()

def test_kwarg_corrector_one_to_one_conflicts_one_to_many_kwargs_true():
    
    kwargs = default_kwargs()
    kwargs['one_to_one']=True
    kwargs['one_to_many']=True
    try:
        kwarg_corrector(**kwargs)
    except Exception as e:
        pass
    else:
        raise Exception('relationship_kwarg_corrector did not throw error when\n'+\
            'presented with one_to_one=True and one_to_many=True')
    kwargs2 = default_kwargs()
    kwargs2['one_to_one']=True
    kwargs2['one_to_many']=True
    assert kwargs == kwargs2


def test_kwargs_corrector_one_to_one_true():
    kwargs = default_kwargs()
    kwargs['one_to_one']=True
    kwarg_corrector(**kwargs)

def test_warning():
    msg = warning()
    assert isinstance(msg, str)
    assert msg.count('{}') == 5

def test_log_capture():
    logger = logging.getLogger()
    with LogCapture() as l:
        logger.info('a message')
        l.check( ('root', 'INFO', 'a message'),)

def test_kwargs_corrector_one_to_one_and_uselist_true():
    one = 'uselist'
    two = 'one_to_one'
    three = 'True'
    four = 'uselist'
    five = 'False'
    msg = warn(one, two, three, four, five)

    kwargs = {}
    kwargs['uselist'] = True
    kwargs['one_to_one'] = True
    #l.check('root', 'WARNING', msg)


