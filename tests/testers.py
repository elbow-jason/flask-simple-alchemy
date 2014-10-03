from testfixtures import LogCapture, log_capture
import logging


def capture(messenger, msg, level='DEBUG'):
    with LogCapture() as l:
        messenger()
        l.check( ('root', level, msg),)

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