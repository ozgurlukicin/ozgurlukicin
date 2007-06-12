#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^ekle/$', 'oi.bug.views.add_bug'),
    (r'^(?P<id>\d+)/$', 'oi.bug.views.detail'),
    (r'^$', 'oi.bug.views.main'),
)