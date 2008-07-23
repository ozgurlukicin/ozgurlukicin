#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from oi.st.wrappers import render_response

from oi.shop.shopprofile.models import ShopProfile

def add_product_to_cart(request):
    # process POST
    from django.http import HttpResponse

    if request.method == "POST":
        return HttpResponse("Product ID: %s<br />Quantity: %s" % (request.POST.get("product_id"), request.POST.get("quantity")))
    else:
        return HttpResponseRedirect("/dukkan/")
