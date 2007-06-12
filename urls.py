#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

from oi.settings import WEB_URL, DOCUMENT_ROOT
from oi.st.models import News

root = "/".join(WEB_URL.split("/")[3:])

urlpatterns = patterns('',
    #Home/News
    (r'^haber/$', 'oi.st.views.news_main'),
    (r'^haber/(?P<sef_title>.*)/yazdir/$', 'oi.st.views.news_printable'),
    (r'^haber/(?P<sef_title>.*)/$', 'oi.st.views.news_detail'),

    #Packages
    (r'^paket/$', 'oi.st.views.pkg_main'),
    (r'^paket/(?P<name>.*)/yazdir/$', 'oi.st.views.pkg_printable'),
    (r'^paket/(?P<name>.*)/$', 'oi.st.views.pkg_detail'),

    # Authentication
    (r'^user/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^user/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    (r'^user/dashboard/$', 'oi.st.views.user_dashboard'),
    (r'^user/page/(?P<page>\d+)/$', 'oi.st.views.user_list'),
    (r'^user/$', 'oi.st.views.user_list'),
    (r'^user/(?P<name>.*)/$', 'oi.st.views.user_profile'),
    (r'^user/(?P<name>.*)/edit/$', 'oi.st.views.edit_profile'),

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
    (r'^forum/$', 'django.views.generic.date_based.archive_index', {"queryset": News.objects.all(), "date_field": "date", "template_name": "forum.html", "allow_empty": True}),

    #Bug tracker
    (r'^bocuk/$', include('oi.bug.urls')),

    #Django
    (r'^$', 'oi.st.views.home'),
    (r'^admin/upload/image/$', 'oi.upload.views.upload'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),
)
