#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *
from django.contrib.auth.views import login
# Uncomment the next two lines to enable the admin:
urlpatterns = patterns('oi.beyin2.views',

    (r'^$', 'main'),
    url(r'^add/$','add_new', name='add_new'),
    #url(r'^(?P<blog_id>\d+)/$',"blog_goster",name="blog_goster"),
    #url(r'^(?P<blog_id>\d+)/(?P<yazi_id>\d+)/yorum_ekle/$',"yorum_ekle",name="yorum_ekle"),
)

