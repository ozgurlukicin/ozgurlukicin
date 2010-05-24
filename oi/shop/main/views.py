#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

# our wrapper script for render_response
from oi.st.wrappers import render_response
from oi.shop.product.models import Product

def home(request):
    products = Product.objects.filter(active=True)
    return render_response(request, 'shop_main.html', {"products":products})
