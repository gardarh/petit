import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'bdjango.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

sys.path.append('/srv/petit-website.example.com/')
sys.path.append('/srv/petit-website.example.com/bdjango/')
