#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

urlpatterns = patterns('oi.shop',
        (r'^$', 'shopprofile.views.main'),
        (r'^olustur/$', 'shopprofile.views.create_shopprofile'),
        (r'^olustur/kisisel_fatura/$', 'shopprofile.views.create_personal_bill'),
        (r'^olustur/kurumsal_fatura/$', 'shopprofile.views.create_corporate_bill'),
        )
