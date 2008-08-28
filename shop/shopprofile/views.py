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
from oi.shop.shopprofile.forms import ShopProfileForm, PersonalBillForm, CorporateBillForm

@login_required
def main(request):
    profile = get_object_or_404(ShopProfile, user=request.user)

    return render_response(request, "shopprofile/shopprofile_main.html", locals())

@login_required
def create_shopprofile(request):
    if request.user.shopprofile_set.count() > 0:
        return HttpResponse("Zaten profiliniz var")
    if request.method == 'POST':
        form = ShopProfileForm(request.POST.copy())
        if form.is_valid():
            shop_profile = ShopProfile(
                    user = request.user,
                    phone = form.cleaned_data["phone"],
                    cellphone = form.cleaned_data["cellphone"],
                    address = form.cleaned_data["address"],
                    second_address = form.cleaned_data["second_address"],
                    )
            shop_profile.save()
            HttpResponseRedirect("/dukkan/profil/")
    else:
        form = ShopProfileForm()
    return render_response(request, "shopprofile/shopprofile_create.html", {"form":form})

@login_required
def create_personal_bill(request):
    form = PersonalBillForm()
    return render_response(request, "shopprofile/bill_create.html", {"form":form})

@login_required
def create_corporate_bill(request):
    form = CorporateBillForm()
    return render_response(request, "shopprofile/bill_create.html", {"form":form})
