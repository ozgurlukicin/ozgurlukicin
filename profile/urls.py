#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

from django.contrib.auth.models import User
from oi.settings import USER_PER_PAGE

urlpatterns = patterns('',
    (r'^liste/$', 'oi.profile.views.user_list'),
    #the tested ones
    (r'^takip-edilen-konular/$', 'oi.profile.views.followed_topics'),
    (r'^giris/$', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'}),
    (r'^cikis/$', 'django.contrib.auth.views.logout', {'template_name': 'user/logout.html',"next_page":"/"}),
    (r'^kayit/$', 'oi.profile.views.user_register'),
    (r'^onay/(?P<name>[\w-]+)/(?P<key>[\w-]+)/$', 'oi.profile.views.user_confirm'),
    (r'^duzenle/$', 'oi.profile.views.user_profile_edit'),
    (r'^sayfam/$', 'oi.profile.views.user_dashboard'),
    (r'^parola-degistir/$', 'oi.profile.views.change_password'),
    (r'^kayip/$', 'oi.profile.views.lost_password'),
    (r'^kayip/degistir/(?P<key>[\w-]+)/$', 'oi.profile.views.reset_password'),
    #(r'^kullanici/(?P<name>[\w-]+)/yorumlar/$', 'oi.profile.views.user_comments'),
    (r'^profil/(?P<name>[\w-]+)/$', 'oi.profile.views.user_profile'),
    (r'^iletiler/(?P<name>[\w-]+)/$', 'oi.profile.views.posts_for_user'),
)
