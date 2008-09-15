#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.shop.shopprofile.models import ShopProfile

class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address',)
    search_fields = ['address']

admin.site.register(ShopProfile, ShopProfileAdmin)
