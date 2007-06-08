#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

SITE_NAME = 'Özgürlük için...'
WEB_URL = 'http://django'
DOCUMENT_ROOT = '/home/ahmet/public_html/oi'

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '%s/db/oi.db' % DOCUMENT_ROOT
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

# For extending User class
AUTH_PROFILE_MODULE = 'st.UserProfile'

TIME_ZONE = 'Europe/Istanbul'
LANGUAGE_CODE = 'tr'
SITE_ID = 1

# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/media/' % DOCUMENT_ROOT

# Example: "http://media.lawrence.com"
MEDIA_URL = '%s/media/' % WEB_URL

# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '%s/media/' % WEB_URL

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n9-*x3!&!(x*z_!13)cyxil4fh+ov_+3!y($&4t7iit=)d)=93'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'oi.flatpages.middleware.FlatpageFallbackMiddleware',
    'oi.middleware.threadlocals.ThreadLocals',
)

ROOT_URLCONF = 'oi.urls'

TEMPLATE_DIRS = (
    '%s/templates' % DOCUMENT_ROOT,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.humanize',
    'oi.flatpages',
    'oi.st',
)
