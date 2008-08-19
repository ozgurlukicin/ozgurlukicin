#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import re

from django import newforms as forms

from oi.shop.shopprofile.models import ShopProfile

class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = ShopProfile
        exclude = ("user", "bill")
