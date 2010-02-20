#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

urlpatterns = patterns('oi.podcast.views',
    (r'^$', 'main'),
    (r'^feed/$', 'feed'),
    (r'^feed/mp3/$', 'feed'),
    (r'^feed/ogg/$', 'feed_ogg'),
    (r'^bolum/(?P<slug>.*)/$', 'detail'),
)
