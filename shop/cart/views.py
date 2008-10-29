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
from django import forms

from oi.st.wrappers import render_response

from oi.shop.shopprofile.models import ShopProfile
from oi.shop.cart.models import Cart, CartItem
from oi.shop.product.models import Product
from oi.shop.cart.forms import BuyForm

def get_cart_for_user(user):
    get_object_or_404(ShopProfile, user=user)
    try:
        cart = Cart.objects.get(user=user)
    except ObjectDoesNotExist:
        cart = Cart(user=user)
        cart.save()
    return cart

@login_required
def add_product_to_cart(request):
    if request.method == "POST":
        cart = get_cart_for_user(request.user)
        product = Product.objects.get(id=request.POST.get("product_id"))
        item = CartItem(
                quantity=request.POST.get("quantity"),
                product=product,
                )
        if int(item.quantity) < 1:
            return HttpResponse("NACK")
        item.save()
        cart.items.add(item)
        return HttpResponse("OK")
    else:
        return HttpResponse("NACK")

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

def get_cart_html(cart):
    cart_html = ''
    for item in cart.items.all():
        cart_html += '<div class="cart_item"><div class="count">%d</div><div class="cart_item_info"><div class="cart_product">%s</div><div class="type">%s</div><div class="remove_button"><a href="#" onclick="remove(%s)"><img src="/media/img/new/button_remove_cart_item.png" alt="Sepetten Çıkar" /></a></div></div></div>' % (item.quantity, item.product.parent.name, item.product.name, item.id)
    if cart.items.count():
        cart_html += '<div class="buy_cart"><a href="/dukkan/sepet/satinal/"><img src="/media/img/new/shop/button_buy.png" alt="Sepettekileri Satın Al" /></a></div>'
    return cart_html

@login_required
def get_cart(request):
    cart = get_cart_for_user(request.user)
    return HttpResponse(get_cart_html(cart))

@login_required
def buy(request):
    user = request.user
    shopProfile = get_object_or_404(ShopProfile, user=user)
    cart = get_object_or_404(Cart, user=user)
    initial = {
        "productcount": cart.items.count(),
        "name": user.first_name,
        "lastname": user.last_name,
        "email": user.email,
        "telephone": shopProfile.phone,
        "telephonegsm": shopProfile.cellphone,
        "address": shopProfile.address,
        "postcode": shopProfile.postcode,
        "ilce": shopProfile.town,
        "city": shopProfile.get_city_display(),
        "country": "Türkiye",
        "taxname": shopProfile.billing_firstname,
        "taxlastname": shopProfile.billing_lastname,
        "taxadress": shopProfile.billing_address,
        "taxpostcode": shopProfile.billing_postcode,
        "taxilce": shopProfile.billing_town,
        "taxcity": shopProfile.get_billing_city_display(),
        "taxcountry": "Türkiye",
        "taxvergidairesi": shopProfile.billing_office,
        "taxvergino": shopProfile.billing_no,
        "tckimlikno": shopProfile.tcno,
        }
    form = BuyForm(initial=initial)
    return render_response(request, "cart/buy.html", {"form": form, "cartItems": cart.items.all()})
