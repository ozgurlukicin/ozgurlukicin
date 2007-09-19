#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    #(r'^feed/rss/$', 'rssfeed'),
    #(r'^feed/atom/$', 'atomfeed'),
    #(r'^feed/$', 'rssfeed'),

    #(r'^feed/atom/user/(?P<user>\d+)/$', 'atomfeed'),
    #(r'^feed/rss/user/(?P<user>\d+)/$', 'rssfeed'),

    (r'^$', 'oi.forum.views.main'),
    (r'^(?P<forum_slug>.*)/new/$', 'oi.forum.views.new_topic'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/quote/(?P<post_id>\d+)/$', 'oi.forum.views.reply'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/reply/$', 'oi.forum.views.reply'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/hide/(?P<post_id>\d+)/$', 'oi.forum.views.hide'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/hide/$', 'oi.forum.views.hide'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/delete/(?P<post_id>\d+)/$', 'oi.forum.views.delete'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/delete/$', 'oi.forum.views.delete'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/lock/$', 'oi.forum.views.lock'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/stick/$', 'oi.forum.views.stick'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/$', 'oi.forum.views.topic'),
    (r'^(?P<forum_slug>.*)/$', 'oi.forum.views.forum'),
)