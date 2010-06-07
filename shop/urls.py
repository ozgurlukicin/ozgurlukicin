#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

urlpatterns = patterns('oi.shop',
        # Home page
        (r'^$', 'main.views.home'),
        # Profile
        #(r'^profil/', include('oi.shop.shopprofile.urls')),
        # Shopping Cart
        #(r'^sepet/', include('oi.shop.cart.urls')),
        # Category
        #(r'^kategori/(?P<slug>.*)/$', 'product.views.get_category_products'),
        # Product
        #(r'^urun/(?P<category_slug>.*)/(?P<product_slug>.*)/$', 'product.views.get_product'),
        )
