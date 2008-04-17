#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns
from oi.forum.feeds import *
from oi.forum.models import Post

rss_dict = {
            'post': RSS,
            'topic': Topic_Rss,
            'tag': Tag_Rss,
            }

atom_dict = {
            'post': Atom,
            'topic': Topic_Atom,
            'tag': Tag_Atom,
            }

urlpatterns = patterns('',
    (r'^$', 'oi.forum.views.main'),
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': rss_dict}),
    (r'^atom/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': atom_dict}),

    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/delete/(?P<post_id>\d+)/$','oi.forum.views.delete_post'),
    (r'^(?P<forum_slug>.*)/new/$', 'oi.forum.views.new_topic'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/quote/(?P<post_id>\d+)/$', 'oi.forum.views.reply'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/reply/$', 'oi.forum.views.reply'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/hide/(?P<post_id>\d+)/$', 'oi.forum.views.hide'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/edit/(?P<post_id>\d+)/$', 'oi.forum.views.edit_post'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/hide/$', 'oi.forum.views.hide'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/lock/$', 'oi.forum.views.lock'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/stick/$', 'oi.forum.views.stick'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/merge/$', 'oi.forum.views.merge'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/move/$', 'oi.forum.views.move'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/edit/$', 'oi.forum.views.edit_topic'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/$', 'oi.forum.views.topic'),
    (r'^(?P<forum_slug>.*)/$', 'oi.forum.views.forum'),
)
