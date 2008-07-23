#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from oi.st.wrappers import render_response

from oi.shop.shopprofile.models import ShopProfile

@login_required
def main(request):
    profile = get_object_or_404(ShopProfile, user=request.user)

    return render_response(request, "shopprofile/shopprofile_main.html", locals())
