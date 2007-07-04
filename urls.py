#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *
from django.contrib.auth.models import User

from oi.settings import WEB_URL, DOCUMENT_ROOT, USER_PER_PAGE, PACKAGE_PER_PAGE, GAME_PER_PAGE, FS_PER_PAGE, NEWS_PER_PAGE, TAG_PER_PAGE
from oi.st.models import Package, Game, FS, News, Tag
from oi.seminar.models import Seminar

user_dict = {
             'queryset': User.objects.all().order_by('name'),
             'template_name': 'user/user_list.html',
             'paginate_by': USER_PER_PAGE,
             'template_object_name': 'user'
            }

package_dict = {
                'queryset': Package.objects.filter(status=1).order_by('name'),
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
    (r'^haber/$', 'django.views.generic.list_detail.object_list', dict(news_dict, page=1)),
    (r'^haber/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(news_dict)),
    (r'^haber/(?P<slug>.*)/yazdir/$', 'oi.st.views.news_printable'),
    (r'^haber/(?P<slug>.*)/$', 'oi.st.views.news_detail'),

    #Packages
    (r'^paket/$', 'django.views.generic.list_detail.object_list', dict(package_dict, page=1)),
    (r'^paket/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(package_dict)),
    (r'^paket/(?P<name>.*)/yazdir/$', 'oi.st.views.pkg_printable'),
    (r'^paket/(?P<name>.*)/$', 'oi.st.views.pkg_detail'),

    #User management
    (r'^kullanici/liste/$', 'django.views.generic.list_detail.object_list', dict(user_dict, page=1)),
    (r'^kullanici/liste/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(user_dict)),
    (r'^kullanici/giris/$', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'}),
    (r'^kullanici/cikis/$', 'django.contrib.auth.views.logout', {'template_name': 'user/logout.html'}),
    (r'^kullanici/kayit/$', 'oi.profile.views.user_register'),
    (r'^kullanici/onay/(?P<name>[\w-]+)/(?P<key>[\w-]+)/$', 'oi.profile.views.user_confirm'),
    (r'^kullanici/duzenle/$', 'oi.profile.views.user_profile_edit'),
    (r'^kullanici/dashboard/$', 'oi.profile.views.user_dashboard'),
    #(r'^kullanici/(?P<name>[\w-]+)/yorumlar/$', 'oi.profile.views.user_comments'),
    (r'^kullanici/(?P<name>[\w-]+)/$', 'oi.profile.views.user_profile'),

    #First Steps
    (r'^ia/$', 'django.views.generic.list_detail.object_list', dict(fs_dict, page=1)),
    (r'^ia/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(fs_dict)),
    (r'^ia/(?P<slug>.*)/yazdir/$', 'oi.st.views.fs_printable'),
    (r'^ia/(?P<slug>.*)/$', 'oi.st.views.fs_detail'),

    #Games
    (r'^oyun/$', 'django.views.generic.list_detail.object_list', dict(game_dict, page=1)),
    (r'^oyun/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(game_dict)),
    (r'^oyun/(?P<slug>.*)/yazdir/$', 'oi.st.views.game_printable'),
    (r'^oyun/(?P<slug>.*)/$', 'oi.st.views.game_detail'),

    #Tags
    (r'^etiket/$', 'django.views.generic.list_detail.object_list', dict(tag_dict, page=1)),
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

    #Django
    (r'^$', 'oi.st.views.home'),
    (r'^admin/upload/image/add/$', 'oi.upload.views.image_upload'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),
)