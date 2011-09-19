# -*- coding: utf-8 -*-
ADMINS = (
    ('You', 'you@example.com'),
)

PROJECT_ROOT = '/srv/petit-website.example.com/'

MEDIA_ROOT = '%smedia/' % (PROJECT_ROOT,)
STATIC_ROOT = '%sstatic/' % (PROJECT_ROOT,)
TEMPLATE_DIRS = ('%sbdjango/templates/' % (PROJECT_ROOT,),)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dbname',                      # Or path to database file if using sqlite3.
        'USER': 'dbuser',                      # Not used with sqlite3.
        'PASSWORD': 'you password',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
# Change this once you're up and running
DEBUG=True
