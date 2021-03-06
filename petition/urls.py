#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^imzala/$', 'oi.petition.views.petition_sign'),
    (r'^liste/$', 'oi.petition.views.petitioner_list'),
    (r'^onay/(?P<pid>[\w-]+)/(?P<key>[\w-]+)/$', 'oi.petition.views.petitioner_confirm'),
)
