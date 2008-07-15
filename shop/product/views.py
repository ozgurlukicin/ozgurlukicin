#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404

from oi.st.wrappers import render_response
from oi.shop.product.models import Category

# temp
from django.http import HttpResponse

#########################################################
#                                                       #
# A view that lists products inside given category slug #
#                                                       #
#########################################################

def get_category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.product_set.all()

    return render_response(request, "category/category_list.html", {"products": products})
