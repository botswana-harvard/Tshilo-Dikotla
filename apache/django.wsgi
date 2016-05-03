############################################
# apache2 needs permission to access this file
# sudo chgrp www-data apache/django.wsgi
# chmod g+x apache/django.wsgi
############################################

import os
import sys

VIRTUALENV_PATH = '/home/django/.virtualenvs/tshilo_dikotla/'
SOURCE_ROOT_PATH = '/home/django/source/'
LOCAL_PROJECT_RELPATH = 'bhp085/'

# Add the site-packages of the chosen virtualenv to work with
activate_env=os.path.join(VIRTUALENV_PATH, 'bin/activate_this.py')
execfile(activate_env, dict(__file__=activate_env))

# update path
sys.path.insert(0, os.path.join(VIRTUALENV_PATH, 'lib/python3.4/site-packages/'))
sys.path.insert(0, os.path.join(SOURCE_ROOT_PATH, LOCAL_PROJECT_RELPATH))
os.environ['DJANGO_SETTINGS_MODULE'] = 'tshilo_dikotla.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
