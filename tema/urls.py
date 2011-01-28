#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *
from oi.tema.feeds import *

urlpatterns = patterns ('oi.tema.views',
        #URL for Home Page
        (r'^$','themeitem_list'),

        #URLs for ACTIONS
        (r'^raporla/(?P<item_id>\d+)/$', 'report_abuse'),
        (r'^oyla/(?P<item_id>\d+)/$', 'themeitem_rate'),
        (r'^sil/(?P<item_id>\d+)/$', 'themeitem_delete'),

        #URLs for ADD Function
        (r'^ekle/$','themeitem_add'),
        (r'^ekle/duvar-kagitlari/$','themeitem_add_wallpaper'),
        (r'^ekle/masaustu-goruntuleri/$','themeitem_add_desktopscreenshot'),
        (r'^ekle/yazitipleri/$','themeitem_add_font'),
        (r'^ekle/open-office/$','themeitem_add_openofficetheme'),
        (r'^ekle/simge-seti/$','themeitem_add_iconset'),
        (r'^ekle/paket-goruntuleri/$', 'themeitem_add_packagescreenshot'),

        #URLs for CHANGE Function
        (r'^duzenle/duvar-kagitlari/(?P<item_id>[0-9]+)/$','themeitem_change_wallpaper'),
        (r'^duzenle/masaustu-goruntuleri/(?P<item_id>[0-9]+)/$','themeitem_change_desktopscreenshot'),
        (r'^duzenle/yazitipleri/(?P<item_id>[0-9]+)/$','themeitem_change_font'),
        (r'^duzenle/open-office/(?P<item_id>[0-9]+)/$','themeitem_change_openofficetheme'),
        (r'^duzenle/simge-seti/(?P<item_id>[0-9]+)/$','themeitem_change_iconset'),
        (r'^duzenle/paket-goruntuleri/(?P<item_id>[0-9]+)/$', 'themeitem_change_packagescreenshot'),

        #URLs for KHOTNEWSTUFF
        (r'^khotnewstuff/wallpaper-providers.xml$', 'ghns_wallpapers'),
        (r'^khotnewstuff/wallpaper/wallpaper.xml$', 'ghns_wallpaper'),
        (r'^khotnewstuff/wallpaper/wallpaper-score.xml$', 'ghns_wallpaper_score'),
        (r'^khotnewstuff/wallpaper/wallpaper-downloads.xml$', 'ghns_wallpaper_downloads'),

        #URLs for MODERATION
        (r'^yonetim/$', 'themeitem_queue'),
        (r'^raporlanmis-temalar/$', 'list_abuse'),

        #URL for PREVIEW function
        (r'^yazitipleri/detay/(?P<slug>[a-z0-9-_]+)/onizle/(?P<text>.{1,20})/$','font_image'),

        #URLs for FEEDs
        (r'^feed/rss/$', RSS()),
        (r'^feed/atom/$', Atom()),
        (r'^feed/rss/kullanici/(?P<username>.+)/$', User_RSS()),
        (r'^feed/atom/kullanici/(?P<username>.+)/$', User_Atom()),
        (r'^feed/rss/kategori/(?P<category>.+)/$', Category_RSS()),
        (r'^feed/atom/kategori/(?P<category>.+)/$', Category_Atom()),

        #URLs for LISTS
        (r'^([a-z0-9-_]+)?/$','themeitem_list'),
        (r'^([a-z0-9-_]+)/([a-z0-9-_]+)/$','themeitem_list'),
        (r'^kullanici/(?P<username>.+)/$','list_user'),

        #URLS for DETAIL and DOWNLOAD functions
        (r'^(?P<category>[a-z0-9-_]+)/detay/(?P<slug>[a-z0-9-_]+)/$','themeitem_detail'),
        (r'^(?P<category>[a-z0-9-_]+)/detay/(?P<slug>[a-z0-9-_]+)/(?P<id>\d+)/$','themeitem_download'),

        #URLs for Package Manager
        (r'^paket-goruntuleri/exists/(?P<package_name>[a-z0-9-_]+)/$', 'default_image_exists'),
        (r'^paket-goruntuleri/ontanimli/(?P<size>[a-z0-9-_]+)/(?P<package_name>[a-z0-9-_]+)/$', 'show_default_image'),
)
