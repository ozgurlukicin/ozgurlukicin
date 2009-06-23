#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^(?P<id>\d+)/toggle/$', 'oi.paste.views.pastedtext_toggle_hidden'),
    (r'^(?P<id>\d+)/hide/$', 'oi.paste.views.pastedtext_hide'),
    (r'^(?P<id>\d+)/$', 'oi.paste.views.pastedtext_detail'),
    (r'^$', 'oi.paste.views.pastedtext_add'),
)
