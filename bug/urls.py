#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

urlpatterns = patterns('oi.bug.views',
    (r'^ekle/$', 'add_bug'),
    (r'^(?P<id>\d+)/$', 'detail'),
    (r'^$', 'main'),
)