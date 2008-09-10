#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.seminar.models import Place, Attender, Seminar

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['-name']
    search_fields = ['name', 'direction']

class AttenderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['-name']
    search_fields = ['name']

class SeminarAdmin(admin.ModelAdmin):
    list_display = ('description', 'date')
    ordering = ['-date']
    search_fields = ['description']

admin.site.register(Place, PlaceAdmin)
admin.site.register(Attender, AttenderAdmin)
admin.site.register(Seminar, SeminarAdmin)
