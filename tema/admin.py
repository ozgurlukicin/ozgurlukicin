#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin
from oi.tema.models import *

class ThemeItemAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {
                "fields": ("title", "slug", "text", "changelog", "status", "tags")
                }),
            ("Diğer", {
                "classes": "collapse",
                "fields": ("author", "license", "rating", "download_count", "submit", "update", "comment_enabled")
                })
            )
    list_display = ("title", "license", "status")
    list_display_links = ("title",)
    list_filter = ("status", "comment_enabled")
    search_fields = ["title", "text", "changelog"]

class WallpaperAdmin(ThemeItemAdmin):
    fieldsets = (
            (None, {
                "fields": ("title", "slug", "text", "changelog", "papers", "status", "tags")
                }),
            ("Diğer", {
                "classes": "collapse",
                "fields": ("author", "license", "rating", "download_count", "submit", "update", "comment_enabled")
                })
            )

admin.site.register(ThemeItem, ThemeItemAdmin)
admin.site.register(Wallpaper, WallpaperAdmin)
admin.site.register(WallpaperFile, admin.ModelAdmin)
admin.site.register(License, admin.ModelAdmin)
