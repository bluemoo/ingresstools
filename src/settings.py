CSRF_TOKEN = ''
SESSION_ID = ''
LOGFILE = 'actions.log'
STATEFILE = 'actions.state'


#### Import local machine/env specific settings ####
try:
    LOCAL_SETTINGS_ALREADY_IMPORTED
except NameError:
    try:
        LOCAL_SETTINGS_ALREADY_IMPORTED = True
        from site_settings import *
    except ImportError:
        print "To override any default settings, create a site_settings.py file with the correct values."