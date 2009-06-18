#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin
from oi.tema.models import *

class ThemeItemAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {
                "fields": ("name", "category", "description", "changelog", "approved")
                }),
            ("Diğer", {
                "classes": "collapse",
                "fields": ("author", "license", "rating", "download_count", "submit_date", "edit_date", "comment_enabled")
                })
            )
    list_display = ("name", "license", "category", "approved")
    list_display_links = ("name",)
    list_filter = ("approved", "comment_enabled")
    search_fields = ["name", "description", "changelog"]

admin.site.register(ThemeItem, ThemeItemAdmin)
admin.site.register(License, admin.ModelAdmin)
