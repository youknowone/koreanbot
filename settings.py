
# NOTE: To set up, edit local_settings.py
CONNECTIONS = [
    {
        'name': 'localhost',
        'host': 'localhost',
        'port': 6667,
        'nick': 'easybot',
        'autojoins': ['#easybot'],
        'enabled': True,
        'admin': None,
        'invite': 'disallow',
    }
]

RAW_LOG = False

try:
    from local_settings import *
except ImportError:
    print '*** NO local_settings.py file set up. read README! ***'
    pass

