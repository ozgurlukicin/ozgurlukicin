#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from oi.st.wrappers import render_response

from oi.shop.shopprofile.models import ShopProfile
from oi.shop.cart.models import Cart, CartItem
from oi.shop.product.models import Product
from oi.shop.cart.forms import BuyForm

def get_cart_for_user(user):
    try:
        cart = Cart.objects.get(user=user)
    except ObjectDoesNotExist:
        cart = Cart(user=user)
        cart.save()
    return cart

@login_required
def add_product_to_cart(request):
    if request.method == "POST":
        #FIXME: check quantity, it can't be lower than 1
        cart = get_cart_for_user(request.user)
        product = Product.objects.get(id=request.POST.get("product_id"))
        item = CartItem(
                quantity=request.POST.get("quantity"),
                product=product,
                )
        item.save()
        cart.items.add(item)
        return HttpResponse("OK")
    else:
        return HttpResponseRedirect("/dukkan/")

@login_required
def remove_item_from_cart(request):
    if request.method == "POST":
        cart = get_cart_for_user(request.user)
        item = CartItem.objects.get(id=request.POST.get("item_id"),cart=cart)
        cart.items.remove(item)
        item.delete()
        return HttpResponse("OK")
    else:
        return HttpResponseRedirect("/dukkan/")

@login_required
def get_cart(request):
    cart = get_cart_for_user(request.user)
    cart_html = ''
    for item in cart.items.all():
        cart_html += '<div class="item%d"><div class="count">%d</div>' % (item.id, item.quantity) + '<div class="product">%s</div><div class="remove_form" ><form action="javascript:;" method="POST"><input type="submit" onclick="remove(%s)" value="Sepetten Çıkar" /></form></div></div>' % (item.product, item.id)
    return HttpResponse(cart_html)

@login_required
def buy(request):
    form = BuyForm()
    return render_response(request, "cart/buy.html", {"form": form})
