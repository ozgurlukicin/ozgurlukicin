#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from oi.st.wrappers import render_response
from oi.shop.shopprofile.models import ShopProfile
from oi.shop.shopprofile.forms import ShopProfileForm

@login_required
def change_shopprofile(request):
    profile = get_object_or_404(ShopProfile, user=request.user)
    profile_updated = False

    if request.method == 'POST':
        form = ShopProfileForm(request.POST.copy())
        if form.is_valid():
            profile.tcno = form.cleaned_data["tcno"]
            profile.phone = form.cleaned_data["phone"]
            profile.cellphone = form.cleaned_data["cellphone"]
            profile.address = form.cleaned_data["address"]
            profile.postcode = form.cleaned_data["postcode"]
            profile.town = form.cleaned_data["town"]
            profile.city = form.cleaned_data["city"]
            profile.billing_firstname = form.cleaned_data["billing_firstname"]
            profile.billing_lastname = form.cleaned_data["billing_lastname"]
            profile.billing_address = form.cleaned_data["billing_address"]
            profile.billing_postcode = form.cleaned_data["billing_postcode"]
            profile.billing_town = form.cleaned_data["billing_town"]
            profile.billing_city = form.cleaned_data["billing_city"]
            profile.billing_office = form.cleaned_data["billing_office"]
            profile.billing_no = form.cleaned_data["billing_no"]
            profile.save()
            profile_updated = True
    else:
        default_data = {
                "tcno": profile.tcno,
                "phone": profile.phone,
                "cellphone": profile.cellphone,
                "address": profile.address,
                "postcode": profile.postcode,
                "town": profile.town,
                "city": profile.city,
                "billing_firstname": profile.billing_firstname,
                "billing_lastname": profile.billing_lastname,
                "billing_address": profile.billing_address,
                "billing_postcode": profile.billing_postcode,
                "billing_town": profile.billing_town,
                "billing_city": profile.billing_city,
                "billing_office": profile.billing_office,
                "billing_no": profile.billing_no,
                }
        form = ShopProfileForm(default_data)

    return render_response(request, "shopprofile/shopprofile_main.html", locals())

@login_required
def create_shopprofile(request):
    if request.user.shopprofile_set.count() > 0:
        return HttpResponse("Zaten profiliniz var")
    if request.method == 'POST':
        form = ShopProfileForm(request.POST.copy())
        if form.is_valid():
            shopProfile = ShopProfile(
                    user = request.user,
                    tcno = form.cleaned_data["tcno"],
                    phone = form.cleaned_data["phone"],
                    cellphone = form.cleaned_data["cellphone"],
                    address = form.cleaned_data["address"],
                    postcode = form.cleaned_data["postcode"],
                    town = form.cleaned_data["town"],
                    city = form.cleaned_data["city"],
                    billing_firstname = form.cleaned_data["billing_firstname"],
                    billing_lastname = form.cleaned_data["billing_lastname"],
                    billing_address = form.cleaned_data["billing_address"],
                    billing_postcode = form.cleaned_data["billing_postcode"],
                    billing_town = form.cleaned_data["billing_town"],
                    billing_city = form.cleaned_data["billing_city"],
                    billing_office = form.cleaned_data["billing_office"],
                    billing_no = form.cleaned_data["billing_no"],
                    )
            shopProfile.save()
            return render_response(request, "shopprofile/shopprofile_main.html", {"profile":shopProfile})
    else:
        form = ShopProfileForm()
    return render_response(request, "shopprofile/shopprofile_create.html", {"form":form})
