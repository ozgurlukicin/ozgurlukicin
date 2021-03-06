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
    (r'^gonderilecek/(?P<version_slug>[a-z0-9-_]+)/$', 'cdclient_list_to_send'),
    (r'^gonderildi/$', 'cdclient_list_sent'),
    (r'^gonderildi/(?P<version_slug>[a-z0-9-_]+)/$', 'cdclient_list_sent'),
    (r'^gonderilmedi/$', 'cdclient_list_not_sent'),
    (r'^gonderilmedi/(?P<version_slug>[a-z0-9-_]+)/$', 'cdclient_list_not_sent'),
    (r'^kargoda/$', 'cdclient_list_delivered'),
    (r'^sehirler/$', 'cdclient_list_cities'),
    (r'^liste/$', 'cdclient_list'),
    (r'^onay/(?P<id>\d+)/(?P<hash>[\w]{40})/$', 'confirm_cdclient'),
    (r'^duzenle/(?P<id>\d+)/$', 'change_cdclient'),
    (r'^detay/(?P<id>\d+)/$', 'cdclient_detail'),
    (r'^kargo/(?P<id>\d+)/$', 'cdclient_cargo'),
)
