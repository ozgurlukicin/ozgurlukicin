#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

from django.contrib.auth.models import User
from oi.settings import USER_PER_PAGE

user_dict = {
             'queryset': User.objects.all().order_by('name'),
             'template_name': 'user/user_list.html',
             'paginate_by': USER_PER_PAGE,
             'template_object_name': 'user'
            }

urlpatterns = patterns('',
    (r'^liste/$', 'django.views.generic.simple.redirect_to', {'url': "sayfa/1/"}),
    (r'^liste/sayfa/(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_list', dict(user_dict)),
    (r'^giris/$', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'}),
    (r'^cikis/$', 'django.contrib.auth.views.logout', {'template_name': 'user/logout.html'}),
    (r'^kayit/$', 'oi.profile.views.user_register'),
    (r'^onay/(?P<name>[\w-]+)/(?P<key>[\w-]+)/$', 'oi.profile.views.user_confirm'),
    (r'^duzenle/$', 'oi.profile.views.user_profile_edit'),
    (r'^sayfam/$', 'oi.profile.views.user_dashboard'),
    (r'^kayip/$', 'oi.profile.views.lost_password'),
    (r'^kayip/degistir/(?P<key>[\w-]+)/$', 'oi.profile.views.change_password'),
    #(r'^kullanici/(?P<name>[\w-]+)/yorumlar/$', 'oi.profile.views.user_comments'),
    (r'^(?P<name>[\w-]+)/$', 'oi.profile.views.user_profile'),
)