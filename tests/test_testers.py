from testers import *

def test_log_capture():
    logger = logging.getLogger()
    with LogCapture() as l:
        logger.info('a message')
        l.check( ('root', 'INFO', 'a message'),)

def test_capture():
    logger = logging.getLogger()
    message = 'TESTING'

    def message_maker(level):
        def m():
            logging.__dict__[level](message)
        return m
    cb_DEBUG    = message_maker('debug')
    cb_INFO     = message_maker('info')
    cb_WARNING  = message_maker('warning')
    cb_ERROR    = message_maker('error')
    cb_CRITICAL = message_maker('critical')
    capture(cb_DEBUG,       message,    level='DEBUG')
    capture(cb_INFO,        message,    level='INFO')
    capture(cb_WARNING,     message,    level='WARNING')
    capture(cb_ERROR,       message,    level='ERROR')
    capture(cb_CRITICAL,    message,    level='CRITICAL')


def test_capture_warning():
    #messenger, msg
    pass