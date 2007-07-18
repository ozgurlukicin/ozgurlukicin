#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

from oi.settings import WEB_URL, DOCUMENT_ROOT, PACKAGE_PER_PAGE, GAME_PER_PAGE, FS_PER_PAGE, NEWS_PER_PAGE, TAG_PER_PAGE
from oi.st.models import Package, Game, FS, News, Tag
from oi.seminar.models import Seminar
from oi.st.feeds import Main_RSS, Main_Atom, News_RSS, News_Atom, FS_RSS, FS_Atom, Game_RSS, Game_Atom, Package_RSS, Package_Atom

main_feed_dict = {
                  'rss': Main_RSS,
                  'atom': Main_Atom,
                 }

news_feed_dict = {
                  'rss': News_RSS,
                  'atom': News_Atom,
                 }

fs_feed_dict = {
                'rss': FS_RSS,
                'atom': FS_Atom,
               }

game_feed_dict = {
                  'rss': Game_RSS,
                  'atom': Game_Atom,
                 }

package_feed_dict = {
                     'rss': Package_RSS,
                     'atom': Package_Atom
                    }

package_dict = {
                'queryset': Package.objects.filter(status=1).order_by('title'),
                'template_name': 'package/package_main.html',
                'paginate_by': PACKAGE_PER_PAGE,
                'template_object_name': 'package'
               }

game_dict = {
             'queryset': Game.objects.filter(status=1).order_by('title'),
             'template_name': 'game/game_main.html',
             'paginate_by': GAME_PER_PAGE,
             'template_object_name': 'game'
            }

fs_dict = {
           'queryset': FS.objects.filter(status=1).order_by('title'),
           'template_name': 'fs/fs_main.html',
           'paginate_by': FS_PER_PAGE,
           'template_object_name': 'fs'
          }

news_dict = {
             'queryset': News.objects.filter(status=1).order_by('-date'),
             'template_name': 'news/news_main.html',
             'paginate_by': NEWS_PER_PAGE,
             'template_object_name': 'news',
             'extra_context': {'seminar': Seminar.objects.filter(status=1).order_by('date')}
            }

tag_dict = {
            'queryset': Tag.objects.all().order_by('name'),
            'template_name': 'tag/tag_main.html',
            'paginate_by': TAG_PER_PAGE,
            'template_object_name': 'tag'
           }

urlpatterns = patterns('',
    #News
    (r'^haber/$', 'django.views.generic.simple.redirect_to', {'url': "sayfa/1/"}),
    (r'^haber/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(news_dict)),
    (r'^haber/(?P<slug>.*)/yazdir/$', 'oi.st.views.news_printable'),
    (r'^haber/(?P<slug>.*)/$', 'oi.st.views.news_detail'),

    #Packages
    (r'^paket/$', 'django.views.generic.simple.redirect_to', {'url': "sayfa/1/"}),
    (r'^paket/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(package_dict)),
    (r'^paket/(?P<slug>.*)/yazdir/$', 'oi.st.views.pkg_printable'),
    (r'^paket/(?P<slug>.*)/$', 'oi.st.views.pkg_detail'),

    #User management
    (r'^kullanici/', include('oi.profile.urls')),

    #First Steps
    (r'^ia/$', 'django.views.generic.simple.redirect_to', {'url': "sayfa/1/"}),
    (r'^ia/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(fs_dict)),
    (r'^ia/(?P<slug>.*)/yazdir/$', 'oi.st.views.fs_printable'),
    (r'^ia/(?P<slug>.*)/$', 'oi.st.views.fs_detail'),

    #Games
    (r'^oyun/$', 'django.views.generic.simple.redirect_to', {'url': "sayfa/1/"}),
    (r'^oyun/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(game_dict)),
    (r'^oyun/(?P<slug>.*)/yazdir/$', 'oi.st.views.game_printable'),
    (r'^oyun/(?P<slug>.*)/$', 'oi.st.views.game_detail'),

    #Tags
    (r'^etiket/$', 'django.views.generic.simple.redirect_to', {'url': "sayfa/1/"}),
    (r'^etiket/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(tag_dict)),
    (r'^etiket/(?P<tag>.*)/$', 'oi.st.views.tag_detail'),

    #Download
    (r'^indir/$', 'oi.st.views.download'),
    (r'^indir/(?P<version>.*)/surum_notu/$', 'oi.st.views.download_detail_releasenotes'),

    #Video
    (r'^video/(?P<video>.*)/$', 'oi.st.views.videobox'),

    #Seminar
    (r'^seminer/', include('oi.seminar.urls')),

    #Forum
    (r'^forum/', include('oi.forum.urls')),

    #Bug tracker
    (r'^bocuk/', include('oi.bug.urls')),

    #Gezegen
    (r'^gezegen/', include('oi.feedjack.urls')),

    #FIXME: Delete this when development ends
    (r'^test/$', 'oi.st.views.test'),

    #Feeds
    (r'^(?P<url>.*)/haber/$', 'django.contrib.syndication.views.feed', {'feed_dict': news_feed_dict}),
    (r'^(?P<url>.*)/ia/$', 'django.contrib.syndication.views.feed', {'feed_dict': fs_feed_dict}),
    (r'^(?P<url>.*)/oyun/$', 'django.contrib.syndication.views.feed', {'feed_dict': game_feed_dict}),
    (r'^(?P<url>.*)/paket/$', 'django.contrib.syndication.views.feed', {'feed_dict': package_feed_dict}),
    (r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': main_feed_dict}),

    #Django
    (r'^$', 'oi.st.views.home'),
    (r'^admin/upload/image/add/$', 'oi.upload.views.image_upload'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),
)