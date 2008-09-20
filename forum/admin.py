#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Artistanbul
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from oi.forum.models import Forum, Category

class ForumAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    prepopulated_fields = {'slug': ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ['-name']
    search_fields = ['name']

admin.site.register(Forum, ForumAdmin)
admin.site.register(Category, CategoryAdmin)
