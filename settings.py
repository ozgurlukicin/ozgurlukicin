#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import platform

DEVELOPMENT_MODE = ("pardus" not in platform.node())

ADMINS = ()
MANAGERS = ADMINS

# Site configuration
SITE_NAME = 'Özgürlük için...'
SITE_DESC = 'Pardus için bir numaralı bilgi kaynağı'

if DEVELOPMENT_MODE:
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    WEB_URL = 'http://django'
    DOCUMENT_ROOT = '/home/ahmet/public_html/oi'
    DATABASE_ENGINE = 'mysql'
    DATABASE_NAME = 'oi'
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = 'root'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = ''
else:
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    WEB_URL = 'http://www.ozgurlukicin.com'
    DOCUMENT_ROOT = '/var/www/ozgurlukicin.com/oi'
    DATABASE_ENGINE = 'mysql'
    DATABASE_NAME = 'ozgur_oi'
    DATABASE_USER = 'ozgur'
    DATABASE_PASSWORD = ''
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = ''

# Email
DEFAULT_FROM_EMAIL = 'accounts@ozgurlukicin.com'
EMAIL_HOST = 'mail.ozgurlukicin.com'

# Pagination
USER_PER_PAGE = 10
PACKAGE_PER_PAGE = 10
FS_PER_PAGE = 10
GAME_PER_PAGE = 10
NEWS_PER_PAGE = 10
TAG_PER_PAGE = 10
SEMINAR_PER_PAGE = 10

# News in homepage
NEWS_IN_HOMEPAGE = 2
PACKAGES_IN_HOMEPAGE = 2
GAMES_IN_HOMEPAGE = 2
FS_IN_HOMEPAGE = 2

# For extending User class
AUTH_PROFILE_MODULE = 'profile.Profile'

# Login stuff, we use different urls for authentication.
LOGIN_URL = '/kullanici/giris/'
LOGIN_REDIRECT_URL = '/kullanici/dashboard/'
LOGOUT_URL = '/kullanici/cikis/'
PROFILE_EDIT_URL = '/kullanici/duzenle/'

# Feedjack Settings for resizing images
FEEDJACK_RESIZE_IMAGE = True
FEEDJACK_MAX_IMAGE_Y = False
FEEDJACK_MAX_IMAGE_X = 550
FEEDJACK_UPLOAD_DIR = "%s/media/feedjack" % DOCUMENT_ROOT
FEEDJACK_UPLOAD_URL = "%s/media/feedjack" % WEB_URL

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
    'oi.upload',
    'oi.bug',
    'oi.feedjack',
    'oi.seminar',
    'oi.profile',
    'oi.forum',
)

CITY_LIST = (
    ('adana','Adana'),
    ('adiyaman','Adıyaman'),
    ('afyon','Afyon'),
    ('agri','Ağrı'),
    ('aksaray','Aksaray'),
    ('amasya','Amasya'),
    ('ankara','Ankara'),
    ('antalya','Antalya'),
    ('ardahan','Ardahan'),
    ('artvin','Artvin'),
    ('aydin','Aydın'),
    ('balikesir','Balikesir'),
    ('bartin','Bartın'),
    ('batman','Batman'),
    ('bayburt','Bayburt'),
    ('bilecik','Bilecik'),
    ('bingol','Bingöl'),
    ('bitlis','Bitlis'),
    ('bolu','Bolu'),
    ('burdur','Burdur'),
    ('bursa','Bursa'),
    ('canakkale','Çanakkale'),
    ('cankiri','Çankırı'),
    ('corum','Çorum'),
    ('denizli','Denizli'),
    ('diyarbakir','Diyarbakır'),
    ('duzce','Düzce'),
    ('edirne','Edirne'),
    ('elazig','Elazığ'),
    ('erzincan','Erzincan'),
    ('erzurum','Erzurum'),
    ('eskisehir','Eskişehir'),
    ('gaziantep','Gaziantep'),
    ('giresun','Giresun'),
    ('gumushane','Gümüşhane'),
    ('hakkari','Hakkari'),
    ('hatay','Hatay'),
    ('igdir','Iğdır'),
    ('isparta','Isparta'),
    ('istanbul_anadolu','İstanbul (Anadolu)'),
    ('istanbul_avrupa','İstanbul (Avrupa)'),
    ('izmir','İzmir'),
    ('kahramanmaras','KahramanMaraş'),
    ('karabuk', 'Karabük'),
    ('karaman','Karaman'),
    ('kars','Kars'),
    ('kastamonu','Kastamonu'),
    ('kayseri','Kayseri'),
    ('kilis', 'Kilis'),
    ('kirikkale','Kırıkkale'),
    ('kirklareli','Kırklareli'),
    ('kirsehir','Kırşehir'),
    ('kocaeli','Kocaeli'),
    ('konya','Konya'),
    ('kutahya','Kütahya'),
    ('malatya','Malatya'),
    ('manisa','Manisa'),
    ('mardin','Mardin'),
    ('mersin','Mersin'),
    ('mugla','Muğla'),
    ('mus','Muş'),
    ('nevsehir','Nevşehir'),
    ('nigde','Niğde'),
    ('ordu','Ordu'),
    ('osmaniye', 'Osmaniye'),
    ('rize','Rize'),
    ('sakarya','Sakarya'),
    ('samsun','Samsun'),
    ('siirt','Siirt'),
    ('sinop','Sinop'),
    ('sivas','Sivas'),
    ('sirnak','Şırnak'),
    ('tekirdag','Tekirdag'),
    ('tokat','Tokat'),
    ('trabzon','Trabzon'),
    ('tunceli','Tunceli'),
    ('urfa','Urfa'),
    ('usak','Uşak'),
    ('van','Van'),
    ('yozgat','Yozgat'),
    ('yalova', 'Yalova'),
    ('zonguldak','Zonguldak')
)
