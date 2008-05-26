#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *
from django.contrib.comments.models import FreeComment

from oi.settings import WEB_URL, DOCUMENT_ROOT, PACKAGE_PER_PAGE, GAME_PER_PAGE, FS_PER_PAGE, NEWS_PER_PAGE, TAG_PER_PAGE, HOWTO_PER_PAGE
from oi.st.models import Package, Game, FS, News, Tag, HowTo
from oi.seminar.models import Seminar
from oi.st.feeds import *

rss_dict = {
            '': Main_RSS,
            'haber': News_RSS,
            'ia': FS_RSS,
            'oyun': Game_RSS,
            'paket': Package_RSS,
            'nasil': HowTo_RSS,
           }

atom_dict = {
             '': Main_Atom,
             'haber': News_Atom,
             'ia': FS_Atom,
             'oyun': Game_Atom,
             'paket': Package_Atom,
             'nasil': HowTo_Atom,
            }

package_dict = {
                'queryset': Package.objects.filter(status=1).order_by('title'),
                'template_name': 'package/package_main.html',
                'paginate_by': PACKAGE_PER_PAGE,
                'template_object_name': 'package',
               }

game_dict = {
             'queryset': Game.objects.filter(status=1).order_by('title'),
             'template_name': 'game/game_main.html',
             'paginate_by': GAME_PER_PAGE,
             'template_object_name': 'game',
            }

fs_dict = {
           'queryset': FS.objects.filter(status=1).order_by('order'),
           'template_name': 'fs/fs_main.html',
           'paginate_by': FS_PER_PAGE,
           'template_object_name': 'fs',
          }

howto_dict = {
              'queryset': HowTo.objects.filter(status=1).order_by('title'),
              'template_name': 'howto/howto_main.html',
              'paginate_by': HOWTO_PER_PAGE,
              'template_object_name': 'howto',
              'extra_context': {
                  'firststep': FS.objects.filter(status=1).order_by('order')[:10],
                  },
             }

news_dict = {
             'queryset': News.objects.filter(status=1).order_by('-update'),
             'template_name': 'news/news_main.html',
             'paginate_by': NEWS_PER_PAGE,
             'template_object_name': 'news',
             'extra_context': {
                 'seminar': Seminar.objects.filter(status=1).order_by('-date'),
                 }
            }

tag_dict = {
            'queryset': Tag.objects.all().order_by('name'),
            'template_name': 'tag/tag_main.html',
            'paginate_by': TAG_PER_PAGE,
            'template_object_name': 'tag'
           }

urlpatterns = patterns('',

    (r'^robots.txt$', 'oi.st.views.robots'),

    #comments
    (r'^comments/post/$', 'oi.comments.views.post_comment'),
    (r'^comments/posted/$', 'oi.comments.views.comment_was_posted'),

    #News
    #(r'^haber/yorum/(?P<id>\d+)/$', 'oi.st.views.comment_news'),
    (r'^haber/yorum/(?P<slug>.*)/$', 'oi.st.views.comment_news'),
    (r'^haber/$', 'django.views.generic.list_detail.object_list', dict(news_dict)),
    (r'^haber/(?P<slug>.*)/yazdir/$', 'oi.st.views.news_printable'),
    (r'^haber/(?P<slug>.*)/$', 'oi.st.views.news_detail'),

    #Packages
    (r'^paket/yorum/(?P<slug>.*)/$', 'oi.st.views.comment_package'),
    (r'^paket/$', 'django.views.generic.list_detail.object_list', dict(package_dict)),
    (r'^paket/(?P<slug>.*)/yazdir/$', 'oi.st.views.pkg_printable'),
    (r'^paket/(?P<slug>.*)/$', 'oi.st.views.pkg_detail'),

    #User management
    (r'^kullanici/', include('oi.profile.urls')),
    (r'^accounts/login/$', 'django.views.generic.simple.redirect_to', {'url': "/kullanici/giris/"}),
    (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': "/kullanici/duzenle/"}),

    #First Steps
    (r'^ia/$', 'django.views.generic.list_detail.object_list', dict(fs_dict)),
    (r'^ia/(?P<slug>.*)/yazdir/$', 'oi.st.views.fs_printable'),
    (r'^ia/(?P<slug>.*)/$', 'oi.st.views.fs_detail'),

    #How to
    (r'^nasil/yorum/(?P<slug>.*)/$', 'oi.st.views.comment_howto'),
    (r'^nasil/$', 'django.views.generic.list_detail.object_list', dict(howto_dict)),
    (r'^nasil/(?P<slug>.*)/yazdir/$', 'oi.st.views.howto_printable'),
    (r'^nasil/(?P<slug>.*)/$', 'oi.st.views.howto_detail'),

    #Games
    (r'^oyun/yorum/(?P<slug>.*)/$', 'oi.st.views.comment_game'),
    (r'^oyun/$', 'django.views.generic.list_detail.object_list', dict(game_dict)),
    (r'^oyun/(?P<slug>.*)/yazdir/$', 'oi.st.views.game_printable'),
    (r'^oyun/(?P<slug>.*)/$', 'oi.st.views.game_detail'),

    #Tags
    (r'^etiket/$', 'django.views.generic.list_detail.object_list', dict(tag_dict)),
    (r'^etiket/(?P<tag>.*)/$', 'oi.st.views.tag_detail'),

    #Search
    (r'^arama/$', 'oi.st.views.search'),

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
    (r'^hata/', include('oi.bug.urls')),

    #Planet
    (r'^gezegen/', include('oi.feedjack.urls')),

    #Tema
    (r'^tema/', include('oi.tema.urls')),

    #Petition
    (r'^petition/', include('oi.petition.urls')),
    (r'^ooxml/', 'oi.petition.views.petition_sign'),

    #Django
    (r'^$', 'oi.st.views.home'),
    (r'^admin/upload/image/add/$', 'oi.upload.views.image_upload'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),

    #Feeds
    (r'^rss/gezegen/$', 'oi.feedjack.views.rssfeed'),
    (r'^rss/gezegen/kullanici/(?P<user>\d+)/etiket/(?P<tag>.*)/$', 'oi.feedjack.views.rssfeed'),
    (r'^rss/gezegen/kullanici/(?P<user>\d+)/$', 'oi.feedjack.views.rssfeed'),
    (r'^rss/gezegen/etiket/(?P<tag>.*)/$', 'oi.feedjack.views.rssfeed'),
    (r'^atom/gezegen/$', 'oi.feedjack.views.atomfeed'),
    (r'^atom/gezegen/kullanici/(?P<user>\d+)/etiket/(?P<tag>.*)/$', 'oi.feedjack.views.atomfeed'),
    (r'^atom/gezegen/kullanici/(?P<user>\d+)/$', 'oi.feedjack.views.atomfeed'),
    (r'^atom/gezegen/etiket/(?P<tag>.*)/$', 'oi.feedjack.views.atomfeed'),

    (r'^rss/(?P<url>.*)$', 'django.contrib.syndication.views.feed', {'feed_dict': rss_dict}),
    (r'^atom/(?P<url>.*)$', 'django.contrib.syndication.views.feed', {'feed_dict': atom_dict}),
)
