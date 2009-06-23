#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.seminar.models import Place, Attender, Seminar

class PlaceAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Genel", {"fields": ("name", "description", "phone")}),
        ("Koordinatlar", {"fields": ("latitude", "longitude"), "classes": ("collapse",)}),
    )
    list_display = ("name", "phone")
    ordering = ['-name']
    search_fields = ['name']

class AttenderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['-name']
    search_fields = ['name']

class SeminarAdmin(admin.ModelAdmin):
    list_display = ('description', 'start_date', "end_date")
    ordering = ['-start_date']
    search_fields = ['description']

admin.site.register(Place, PlaceAdmin)
admin.site.register(Attender, AttenderAdmin)
admin.site.register(Seminar, SeminarAdmin)
