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
    url(r'^edited_(?P<idea_id>\d+)/$', 'main',name='main_post'),
    url(r'^add/$','add_new', name='add_new'),
    url(r'^idea_(?P<idea_id>\d+)/edit/$','edit_idea', name='edit_idea'),
    url(r'^idea_(?P<idea_id>\d+)/delete/$','delete_idea', name='delete_idea'),
    url(r'^idea_(?P<idea_id>\d+)/duplicate/$',"mark_duplicate",name="mark_duplicate"),
    url(r'^idea_(?P<idea_id>\d+)/vote-(?P<vote>\d+)/$',"vote",name="vote"),
    #url(r'^(?P<blog_id>\d+)/$',"blog_goster",name="blog_goster"),
    #url(r'^(?P<blog_id>\d+)/(?P<yazi_id>\d+)/yorum_ekle/$',"yorum_ekle",name="yorum_ekle"),
)

