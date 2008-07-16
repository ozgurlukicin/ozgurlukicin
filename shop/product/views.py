#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404

from oi.st.wrappers import render_response
from oi.shop.product.models import Category, Product

# temp
from django.http import HttpResponse

#########################################################
#                                                       #
# A view that lists products inside given category slug #
#                                                       #
#########################################################

def get_category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.get_active_products()

    return render_response(request, "category/category_list.html", {"products": products})

def get_product(request, category_slug, product_slug):
    # filter by product and category slug together
    # becuase a product can have the same name but can be in different categories.

    product = get_object_or_404(Product, slug__exact=product_slug, category__slug__exact=category_slug)

    return render_response(request, "product/product_info.html", {"product": product})
