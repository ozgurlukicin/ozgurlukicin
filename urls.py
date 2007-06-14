#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *
from django.contrib.auth.models import User

from oi.settings import WEB_URL, DOCUMENT_ROOT, USER_PER_PAGE
from oi.st.models import News

root = "/".join(WEB_URL.split("/")[3:])

user_dict = {
             'queryset': User.objects.all(),
             'template_name': 'user_list.html',
             'paginate_by': USER_PER_PAGE
            }

urlpatterns = patterns('',
    #Home/News
    (r'^haber/$', 'oi.st.views.news_main'),
    (r'^haber/(?P<sef_title>.*)/yazdir/$', 'oi.st.views.news_printable'),
    (r'^haber/(?P<sef_title>.*)/$', 'oi.st.views.news_detail'),

    #Packages
    (r'^paket/$', 'oi.st.views.pkg_main'),
    (r'^paket/(?P<name>.*)/yazdir/$', 'oi.st.views.pkg_printable'),
    (r'^paket/(?P<name>.*)/$', 'oi.st.views.pkg_detail'),

    #User management
    (r'^user/login/$', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'}),
    (r'^user/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'user/logout.html'}),
    (r'^user/register/$', 'oi.st.views.user_register'),
    (r'^confirm/(?P<name>[\w-]+)/(?P<key>[\w-]+)/$', 'oi.st.views.user_confirm'),
    (r'^user/dashboard/$', 'oi.st.views.user_dashboard'),
    (r'^user/page/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(user_dict)),
    (r'^user/(?P<name>[\w-]+)/$', 'oi.st.views.user_profile'),

    #First Steps
    (r'^ia/$', 'oi.st.views.fs_main'),
    (r'^ia/(?P<sef_title>.*)/yazdir/$', 'oi.st.views.fs_printable'),
    (r'^ia/(?P<sef_title>.*)/$', 'oi.st.views.fs_detail'),

    #Games
    (r'^oyun/$', 'oi.st.views.game_main'),
    (r'^oyun/(?P<sef_title>.*)/yazdir/$', 'oi.st.views.game_printable'),
    (r'^oyun/(?P<sef_title>.*)/$', 'oi.st.views.game_detail'),

    #Tags
    (r'^tag/$', 'oi.st.views.tag_main'),
    (r'^tag/(?P<tag>.*)/$', 'oi.st.views.tag_detail'),

    #Forum
    (r'^forum/$', 'django.views.generic.date_based.archive_index', {"queryset": News.objects.all(), "date_field": "date", "template_name": "forum/forum_main.html", "allow_empty": True}),

    #Bug tracker
    (r'^bocuk/$', include('oi.bug.urls')),

    #Django
    (r'^$', 'oi.st.views.home'),
    (r'^admin/upload/image/$', 'oi.upload.views.upload'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),
)
