# -*- coding: utf-8 -*-
ADMINS = (
    ('Gardar Hauksson', 'gardarh@gmail.com'),
)

MEDIA_ROOT = '/home/gardarh/petit/media/'

TEMPLATE_DIRS = (
	'/home/gardarh/petit/bdjango/templates/'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gis_bebe',                      # Or path to database file if using sqlite3.
        'USER': 'gis_bebe',                      # Not used with sqlite3.
        'PASSWORD': 'litlaPrinsessa',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
SITE_TITLE = 'Litla Garðarsdóttir'
