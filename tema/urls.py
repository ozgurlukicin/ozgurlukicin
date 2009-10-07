#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *
from oi.tema.feeds import *

feed_dict = {
             'rss': Tema_RSS,
             'atom': Tema_Atom,
            }

cat_feed_dict = {
             'rss': Category_Tema_Rss,
             'atom': Category_Tema_Atom,
            }

user_feed_dict = {
             'rss': User_Tema_Rss,
             'atom': User_Tema_Atom,
            }

urlpatterns = patterns ('oi.tema.views',
        #the first page listing
        (r'^$','themeitem_list'),
        #(r'^duzenle/(?P<item_id>[0-9]+)/$','themeitem_change'),
        (r'^kullanici/(?P<username>.+)/$','list_user'),
        #(r'^oyla/(?P<item_id>[0-9]+)/(?P<rating>[0-4])/$','vote'),
        (r'^ekle/$','themeitem_add'),
        (r'^raporla/(?P<item_id>\d+)/$', 'report_abuse'),
        (r'^oyla/(?P<item_id>\d+)/$', 'themeitem_rate'),
        (r'^sil/(?P<item_id>\d+)/$', 'themeitem_delete'),
        (r'^raporlanmis-temalar/$', 'list_abuse'),
        (r'^ekle/duvar-kagitlari/$','themeitem_add_wallpaper'),
        (r'^ekle/masaustu-goruntuleri/$','themeitem_add_desktopscreenshot'),
        (r'^ekle/yazitipleri/$','themeitem_add_font'),
        (r'^khotnewstuff/wallpaper-providers.xml$', 'ghns_wallpapers'),
        (r'^khotnewstuff/wallpaper/wallpaper.xml$', 'ghns_wallpaper'),
        (r'^khotnewstuff/wallpaper/wallpaper-score.xml$', 'ghns_wallpaper_score'),
        (r'^khotnewstuff/wallpaper/wallpaper-downloads.xml$', 'ghns_wallpaper_downloads'),
        (r'^yonetim/$', 'themeitem_queue'),
        #(r'^listele/(?P<category>[a-z0-9-_]+)/(?P<sort_type>[a-z0-9-_]+)/$','themeitem_sort'),
        (r'^yazitipleri/(?P<slug>[a-z0-9-_]+)/(?P<text>.{1,20})/$','font_image'),
        (r'^(?P<category>[a-z0-9-_]+)/$','themeitem_list'),
        (r'^(?P<category>[a-z0-9-_]+)/(?P<slug>[a-z0-9-_]+)/$','themeitem_detail'),
        (r'^(?P<category>[a-z0-9-_]+)/(?P<slug>[a-z0-9-_]+)/(?P<id>\d+)/$','themeitem_download'),
)
"""
urlpatterns+=patterns('',
        #the rss feeds
        #(r'^feed/(?P<url>.*)/yeni/$', 'django.contrib.syndication.views.feed', {'feed_dict': feed_dict}),
        (r'^feed/kategori/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': cat_feed_dict}),
        (r'^feed/kullanici/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': user_feed_dict}),
)
"""
