#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

urlpatterns = patterns('oi.shop',
        (r'^$', 'cart.views.get_cart'),
        (r'^ekle/$', 'cart.views.add_product_to_cart'),
        (r'^cikar/$', 'cart.views.remove_item_from_cart'),
        (r'^satinal/$', 'cart.views.buy'),
        )
