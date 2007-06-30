#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ahmet AYGÜN
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

urlpatterns = patterns('oi.forum.views',
    (r'^feed/rss/$', 'rssfeed'),
    (r'^feed/atom/$', 'atomfeed'),
    (r'^feed/$', 'rssfeed'),

    (r'^feed/atom/user/(?P<user>\d+)/$', 'atomfeed'),
    (r'^feed/rss/user/(?P<user>\d+)/$', 'rssfeed'),

    (r'^$', 'main'),
)
