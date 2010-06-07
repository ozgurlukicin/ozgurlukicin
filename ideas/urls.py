#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *
from oi.ideas.feeds import RSS, Atom

rss_dict = { "ideafeed": RSS }
atom_dict = { "ideafeed": Atom }

urlpatterns = patterns('oi.ideas.views',
        (r'^$', 'list'),
        (r'^ekle/$', 'add'),
        (r'^duzenle/(?P<idea_id>.*)/$', 'edit_idea'),
        (r'^sil/(?P<idea_id>.*)/$', 'delete_idea'),
        (r'^oyla/$', 'vote'),
        (r'^ayrinti/(?P<idea_id>.*)/$', 'detail'),
        (r'^ayrinti/(?P<idea_id>.*)/favori/ekle$', 'add_favorite'),
        (r'^ayrinti/(?P<idea_id>.*)/favori/cikar$', 'del_favorite'),
        (r'^listele/(?P<field>.*)/(?P<filter_slug>.*)/$', 'list'),
        (r'^tekrar/(?P<idea_id>.*)/(?P<duplicate_id>.*)/$', 'duplicate'),
        (r'^durumdegistir/((?P<idea_id>.*))/(?P<new_status>.*)/$', 'change_status'),
)
urlpatterns += patterns('',
        (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': rss_dict}),
        (r'^atom/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': atom_dict}),
)
