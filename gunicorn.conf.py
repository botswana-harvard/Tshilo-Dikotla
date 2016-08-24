# http://cheng.logdown.com/posts/2015/01/29/deploy-django-nginx-gunicorn-on-mac-osx-part-2
# cd /home/django/source/bhp085/
# gunicorn -c gunicorn.conf.py tshilo_dikotla.wsgi --pid /home/django/source/bhp085/gunicorn.pid --daemon
#

import os
from unipath import Path

SOURCE_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1)

bind = "127.0.0.1:9000"  # Don't use port 80 because nginx occupied it already.
errorlog = os.path.join(SOURCE_ROOT, 'tshilo-dikotla/logs/gunicorn-error.log')  # Make sure you have the log folder create
accesslog = os.path.join(SOURCE_ROOT, 'tshilo-dikotla/logs/gunicorn-access.log')
loglevel = 'debug'
workers = 10 # the number of recommended workers is '2 * number of CPUs + 1'