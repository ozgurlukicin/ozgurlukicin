#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

urlpatterns = patterns('oi.bug.views',
    (r'^ekle/$', 'add_bug'),
    (r'^degistir/(?P<id>\d+)/$', 'change_bug'),
    (r'^sil/(?P<id>\d+)/$', 'delete_bug'),
    (r'^(?P<id>\d+)/$', 'detail'),
    (r'^$', 'main'),
)
