#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

urlpatterns = patterns('oi.beyin2.views',
    url(r'^(?P<idea_id>\d+)/detail/$','idea_detail', name='idea_detail'),
    url(r'^order/(?P<order>.*)/filter/(?P<filter_by>.*)/(?P<filter>.*)/(?P<page_number>\d+)/$', 'main',name='main_page'),
    url(r'^filter/(?P<filter_by>.*)/(?P<filter>.*)/$', 'main',name='main_filter'),
    url(r'^order/(?P<order>.*)/$', 'main',name='main_order'),
    url(r'^edited/(?P<idea_id>\d+)/$', 'main',name='main_post'),
    url(r'^add(?P<phase>\d+)/$','add_new', name='add_new'),
    url(r'^select/$','select_tags', name='select_tags'),
    url(r'^(?P<idea_id>\d+)/edit/$','edit_idea', name='edit_idea'),
    url(r'^(?P<idea_id>\d+)/edit/add_image/$','edit_idea_add_image', name='edit_idea_add_image'),
    url(r'^(?P<idea_id>\d+)/delete/$','delete_idea', name='delete_idea'),
    url(r'^(?P<idea_id>\d+)/undelete/$','undelete_idea', name='undelete_idea'),
    url(r'^(?P<idea_id>\d+)/duplicate/$',"mark_duplicate",name="mark_duplicate"),
    url(r'^(?P<idea_id>\d+)/vote-(?P<vote>\d+)/from_(?P<come_from>\w+)/$',"vote",name="vote"),
    url(r'^is_favorite/(?P<idea_id>\d+)/$','is_favorite', name='is_favorite'),
    url(r'^add_remove_favorite/(?P<idea_id>\d+)/$','add_remove_favorite', name='add_remove_favorite'),
    url(r'^(?P<idea_id>\d+)/report/$','vote_values_report', name='vote_values_report'),
    url(r'^(?P<image_id>\d+)/remove_image/$','image_remove', name='image_remove'),
    (r'^$', 'main'),
)

