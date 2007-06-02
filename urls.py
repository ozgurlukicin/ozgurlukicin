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
    (r'^haber/yazdir/(?P<sef_title>.*)\.html$', 'oi.st.views.news_printable'),
    (r'^haber/(?P<sef_title>.*)\.html$', 'oi.st.views.news_detail'),

    #Packages
    (r'^paket/$', 'oi.st.views.pkg_main'),
    (r'^paket/yazdir/(?P<name>.*)\.html$', 'oi.st.views.pkg_printable'),
    (r'^paket/(?P<name>.*)\.html$', 'oi.st.views.pkg_detail'),

    #First Steps
    (r'^ia/$', 'oi.st.views.fs_main'),
    (r'^ia/yazdir/(?P<sef_title>.*)\.html$', 'oi.st.views.fs_printable'),
    (r'^ia/(?P<sef_title>.*)\.html$', 'oi.st.views.fs_detail'),

    #Games
    (r'^oyun/$', 'oi.st.views.game_main'),
    (r'^oyun/yazdir/(?P<sef_title>.*)\.html$', 'oi.st.views.game_printable'),
    (r'^oyun/(?P<sef_title>.*)\.html$', 'oi.st.views.game_detail'),

    #Tags
    (r'^tag/$', 'oi.st.views.tag_main'),
    (r'^tag/(?P<tag>.*)\.html$', 'oi.st.views.tag_detail'),

    #Forum
    (r'^forum/$', 'django.views.generic.date_based.archive_index', {"queryset": News.objects.all(), "date_field": "date", "template_name": "forum.html", "allow_empty": True}),

    #(r"^%s/comments/" % root, include("django.contrib.comments.urls.comments")),

    #Django
    (r'^$', 'oi.st.views.home'),
    (r'^user/', include('oi.registration.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),
)