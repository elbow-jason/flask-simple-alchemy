#factory_helpers.py
import logging

def kwarg_corrector(**kwargs):
    if kwargs['one_to_one'] and kwargs['one_to_many']:
        raise Exception('relationship kwargs one_to_one and one_to_many'+\
                        'at the same time.\n That doesn\'t even make'+\
                        'sense. Choose one or the other not both.')

    if kwargs['one_to_one']:
        if kwargs['uselist'] == True:
            override_warning('uselist', 'one_to_one',
                                'True', 'uselist', 'False')

        if kwargs['lazy'] != 'select':
            override_warning('lazy', 'one_to_one',
                                 kwargs['lazy'], 'lazy','select')

        #set one_to_one kwargs
        kwargs['uselist'] = False
        kwargs['lazy'] = "select"
    
    if kwargs['one_to_many']:
        if kwargs['uselist'] == False:
            override_warning('uselist', 'one_to_one', 'False',
                                  'uselist', 'True')

        if kwargs['lazy'] == 'dynamic':
            logging.warning('lazy was unneccessarily specified.')
        #set one_to_many kwargs
        kwargs['uselist'] = True

    if kwargs['uselist'] == False and kwargs['lazy'] != 'select':
        override_warning('uselist', 'lazy', "not 'select'",
                            'lazy' 'select')
        kwargs['lazy'] = 'select'

    return kwargs

def warning():
    return "{} kwarg was specified with {} kwarg set as {}."+\
    " Overriding {} to {}."

def warn(one, two, three, four, five):
    msg = warning()
    return msg.format(one, two, three, four, five)
            

def override_warning(str1, str2, val2, changed, override):
    logging.warning(warn(str1, str2, val2, changed, override))

def default_relationship_kwargs():
    return {'uselist':True,
            'lazy':'dynamic',
            'one_to_one':False,
            'one_to_many':False}