#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns
from oi.forum.feeds import *
from oi.forum.models import Post

rss_dict = {
            'post': RSS,
            'topic': Topic_Rss,
            'forum': Forum_Rss,
            'tag': Tag_Rss,
            }

atom_dict = {
            'post': Atom,
            'topic': Topic_Atom,
            'forum': Forum_Atom,
            'tag': Tag_Atom,
            }

urlpatterns = patterns('',
    (r'^$', 'oi.forum.views.main'),
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': rss_dict}),
    (r'^atom/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': atom_dict}),

    #(r'^okunmamis_konular/$', 'oi.forum.views.unread_topics'),
    (r'^son-iletiler/$', 'oi.forum.views.latest_posts'),
    (r'^guncellenen-basliklar/$', 'oi.forum.views.latest_topics'),
    (r'^tumunu-okunmus-say/$', 'oi.forum.views.mark_all_as_read'),
    (r'^raporla/(?P<post_id>\d+)/$', 'oi.forum.views.report_abuse'),
    (r'^raporlanmis-iletiler/$', 'oi.forum.views.list_abuse'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/delete/(?P<post_id>\d+)/$','oi.forum.views.delete_post'),
    (r'^(?P<forum_slug>.*)/new/$', 'oi.forum.views.new_topic'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/quote/(?P<quote_id>\d+)/$', 'oi.forum.views.reply'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/reply/$', 'oi.forum.views.reply'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/follow/$', 'oi.forum.views.follow'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/hide/(?P<post_id>\d+)/$', 'oi.forum.views.hide'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/edit/(?P<post_id>\d+)/$', 'oi.forum.views.edit_post'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/hide/$', 'oi.forum.views.hide'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/lock/$', 'oi.forum.views.lock'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/stick/$', 'oi.forum.views.stick'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/merge/$', 'oi.forum.views.merge'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/move/$', 'oi.forum.views.move'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/edit/$', 'oi.forum.views.edit_topic'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/poll/create/$', 'oi.forum.views.create_poll'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/poll/change/$', 'oi.forum.views.change_poll'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/poll/delete/$', 'oi.forum.views.delete_poll'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/poll/vote/(?P<option_id>\d+)/$', 'oi.forum.views.vote_poll'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/togglegeneral/$', 'oi.forum.views.toggle_general_topic'),
    (r'^(?P<forum_slug>.*)/(?P<topic_id>\d+)/$', 'oi.forum.views.topic'),
    (r'^(?P<forum_slug>.*)/$', 'oi.forum.views.forum'),
)
