#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

urlpatterns = patterns('oi.shipit.views',
    (r'^$', 'create_cdclient'),
    (r'^gonderilecek/$', 'cdclient_list_to_send'),
    (r'^gonderildi/$', 'cdclient_list_sent'),
    (r'^liste/$', 'cdclient_list'),
    (r'^onay/(?P<id>\d+)/(?P<hash>[\w]{40})/$', 'confirm_cdclient'),
    (r'^duzenle/(?P<id>\d+)/$', 'change_cdclient'),
    (r'^detay/(?P<id>\d+)/$', 'cdclient_detail'),
    (r'^kargo/(?P<id>\d+)/$', 'cdclient_cargo'),
)
